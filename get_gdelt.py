import requests
import csv
import os
import time

# DANGER
import warnings
warnings.filterwarnings("ignore")

def make_dates():
    '''Create start and end date ranges for data collection'''
    years = ["2020", "2021", "2022"]
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
            try:
                articles += response["articles"]
            except KeyError:
                print("key error for", url)
                with open("skipped-articles.txt", "a") as myfile:
                    myfile.write(url + '\n')

        if end[6:8] == "01": # reset after each month
            print("Found", len(articles), "articles for", state_abrv, start[0:6])
            
            file_code = start[0:6] + "_" + end[0:6]
            file_name = f"gdelt_results/{state_abrv}/{state_abrv}_" + file_code + ".csv"
            write_results(articles, file_name)
            
            articles = []
            time.sleep(5)

def main():
    
    dates = make_dates()
    # [d for d in dates if int(d[:6]) > 202101]
    states = [#("Alabama", "AL"), ("Alaska", "AK"), ("Arizona", "AZ"), ("Arkansas", "AK"),
              #("California", "CA"), ("Colorado", "CO"),
              ("Connecticut", "CT"),
              ("Delaware", "DE"), ("Florida", "FL"), ("Georgia", "GA"), ("Hawaii", "HI"),
              ("Idaho", "ID"), ("Illinois", "IL"), ("Indiana", "IN"), ("Iowa", "IA"),
              ("Kansas", "KS"), ("Kentucky", "KY"), ("Louisiana", "LA"), ("Maine", "ME"),
              ("Maryland", "MD"), ("Massachusetts", "MA"), ("Michigan", "MI"), ("Minnesota", "MN"),
              ("Mississippi", "MS"), ("Missouri", "MO"), ("Montana", "MT"), ("Nebraska", "NB"),
              ("Nevada", "NV"), ("New%20Hampshire", "NH"), ("New%20Jersey", "NJ"),
              ("New%20Mexico", "NM"), ("New%20York", "NY"), ("North%20Carolina", "NC"),
              ("North%20Dakota", "ND"), ("Ohio", "OH"), ("Oklahoma", "OK"), ("Oregon", "OR"),
              ("Pennsylvania", "PA"), ("Rhode%20Island", "RI"), ("South%20Carolina", "SC"),
              ("South%20Dakota", "SD"), ("Tennessee", "TN"), ("Texas", "TX"), ("Utah", "UT"),
              ("Vermont", "VT"), ("Virginia", "VA"), ("West%20Virginia", "WV"), ("Wisconsin", "WI"),
              ("Wyoming", "WY"), ("GET_ALL_RELEV", "ALL_RELEV")]

    for state, abrv in states:
        get_state_results([d for d in dates if (int(d[:6]) > 202007 and int(d[:4]) < 2021)] + ["20210101010101"],
                          state, abrv)

    # done:
    # alaska
    # alabama
    # arkansas
    # arizona
    # california
    

    # MISSING DATA FOR SOME MONTHS
    # list of urls with errors is available in skipped-articles.txt

    # Washington - did not collect articles due to validity concerns
    

main() 
