import requests
import csv
import os
import time

# DANGER
import warnings
warnings.filterwarnings("ignore")

def make_dates():
    '''Create start and end date ranges for data collection'''
    years = ["2021", "2022"]
    months = [("01", 31), ("02", 28), ("03", 31), ("04", 30),
              ("05", 31), ("06", 30), ("07", 31), ("08", 31),
              ("09", 30), ("10", 31), ("11", 30), ("12", 31)]
    days = [ "0" + x for x in map(str, list(range(1, 10)))]
    days = days + list(map(str, list(range(10, 32))))

    dates = []
    for y in years:
        for m in months:
            for d in days[0:m[1]]:
                dates.append(y + m[0] + d + "010101")

    dates.append("20230101010101")
    return dates

def get_gdelt(url):
    '''Make request to GDELT API'''
    try: 
        resp = requests.get(url, verify=False)
        if resp.status_code != 200: 
            print("error: ", resp.status_code)
            if resp.status_code == 429:
                print("Rate limit reached. Sleeping for 30 secs before resuming.")
                time.sleep(30)
                return get_gdelt(url)
            else:
                return None
        else: 
            return resp.json()
    except Exception as e:
        print("ERROR for", url, "[skipped file]")
        print("Exception:", e)
        with open("skipped-articles.txt", "a") as myfile:
            myfile.write(url + '\n')
        return None

def make_url(state, start, end, maxn=250):
    '''Create URL for GDELT API requests'''
    url = ("https://api.gdeltproject.org/api/v2/doc/doc?"
           f"query={state}%20school"
           "%20sourcecountry:us%20sourcelang:english"
           "&sort=HybridRel"
           f"&startdatetime={start}&enddatetime={end}"
           f"&mode=artlist&maxrecords={maxn}&format=json")
    if state == "GET_ALL_RELEV":
        url = ("https://api.gdeltproject.org/api/v2/doc/doc?"
           f"query=(%22critical%20race%20theory%22%20OR%20crt)"
           "%20sourcecountry:us%20sourcelang:english"
           "&sort=HybridRel"
           f"&startdatetime={start}&enddatetime={end}"
           f"&mode=artlist&maxrecords={maxn}&format=json")
    if state is None:
        url = ("https://api.gdeltproject.org/api/v2/doc/doc?"
           f"query=school"
           "%20sourcecountry:us%20sourcelang:english"
           "&sort=HybridRel"
           f"&startdatetime={start}&enddatetime={end}"
           f"&mode=artlist&maxrecords={maxn}&format=json")
    return url

def write_results(results, outFName):
    with open(outFName, 'w') as outF:
        writer = csv.DictWriter(outF, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

def get_state_results(dates, state, state_abrv):
    '''Retrieve articles for the given state in the given date range and write
    output to file. Note: State should be full state name, state_abrv can be
    two-letter state code, ie. state="virginia" and state_abrv="VA" '''

    # os.mkdir(f"gdelt_results/{state_abrv}")

    articles = []
    for i in range(len(dates) - 1):
        start = dates[i]
        end = dates[i + 1]
        url = make_url(state, start, end, maxn=250)
        # get 100 results per day, or 250 in the case of ALL_RELEV
        response = get_gdelt(url)
        if response is not None: # in case get_gdelt fails
            articles += response["articles"]

        if end[6:8] == "01": # reset after each month
            print("Found", len(articles), "articles for", start[0:6])
            
            file_code = start[0:6] + "_" + end[0:6]
            file_name = f"gdelt_results/{state_abrv}/{state_abrv}_" + file_code + ".csv"
            write_results(articles, file_name)
            
            articles = []
            time.sleep(5)

def main():
    #!/usr/bin/python3.12
    dates = make_dates()
    # [d for d in dates if int(d[:6]) > 202101]
    get_state_results([d for d in dates if int(d[:6]) > 202209], "GET_ALL_RELEV", "ALL_RELEV")

    # MISSING DATA FOR SOME MONTHS
    # list of urls with errors is available in skipped-articles.txt

    # Washington - did not collect articles due to validity concerns
    

main() 
