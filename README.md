### Analysis of online CRT news coverage
#### Anna Lieb's Senior Thesis, Fall 2023

**1. Data collection**

* `get_gdelt.py` gathers article headlines and URLs from the GDELT API based on the keywords "school" and the state name (keyword can appear in headline OR article body text) 
	* creates `gdelt_results` folder with subfolders for each state (excluding Washington) and for the USA overall. Each state subfolder contains 24 files, one for each month of 2021 and 2022. 
	* Notes: 
		* `USA` contains results for a query without a state name keyword. For this folder, I searched just for "school" in any articles published in English in the US. 
		* `ALL_RELEV` contains results for a US English query without keywords for state name or school, but instead with the  criteria "critical race theory" or "CRT". 
		* Each day for each state has a 100-article cap, except for `ALL_RELEV` has a 250-article cap
* `relevant_filter.py` generates labels for headline relevance: 1 if it contains ("race" and ("critical" or "theory") or "crt", 0 otherwise
	* Creates `relevant_results` folder, with a file for each state that includes the relevant label to identify CRT-relevant headlines. 
* `select_relevant.py` takes all files from the `relevant_results` folder and generates a dataframe with rows corresponding to each unique headline. Each headline has a column to count the number of occurrences of the headline in each state's results. 
	* Creates `all_relevant.csv`, which contains headlines and their occurrence by state for all unique headlines that are relevant to CRT. 