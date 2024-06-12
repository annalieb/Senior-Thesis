## A Computational Analysis of Critical Race Theory Controversies and Political Issue Framing in U.S. News
#### Anna Lieb's Senior Thesis (May 2024)

### Highlights
The main motivations, uses, and features of this dataset are described in my Senior Honors Thesis manuscript, entiled [The "Perfect Villain": A Computational Analysis of Critical Race Theory Controversies and Political Issue Framing in U.S. News](https://repository.wellesley.edu/node/49380). The main datasets used in this analysis are `coverage_by_unique_headline.xlsx` and `coverage_by_unique_URL.json`, which include headlines, URLs, and related metrics related to online news coverage of critical race theory controversy in the United States. 

### Replication data and code

Data files and code required for replication are explained below. The following are not included in this repository due to redundancy, but can still be generated using the included python scripts: 

* `gdelt_results` folder (redundant with the `relevant_results` folder)
* `all_relevant.csv` (redundant with `coverage_by_unique_headline.xlsx`)
* `all_relevant_with_URL.csv` (redundant with `coverage_by_unique_URL.json`)
* `GPT_actors.csv` and `GPT_stances.csv` (redundant with `coverage_by_unique_headline.xlsx`)
* `reddit_post_data` (redundant with `coverage_by_unique_URL.json`)

**1. Data collection**

* `get_gdelt.py` gathers article headlines and URLs from the GDELT API based on the keywords "school" and the state name (keyword can appear in headline OR article body text) 
	* creates `gdelt_results` folder with subfolders for each state (excluding Washington) and for the USA overall. Each state subfolder contains 24 files, one for each month of 2021 and 2022. 
	* Notes: 
		* `USA` contains results for a query without a state name keyword. For this folder, I searched just for "school" in any articles published in English in the US. 
		* `ALL_RELEV` contains results for a US English query without keywords for state name or school, but instead with the  criteria "critical race theory" or "CRT". 
		* Each day for each state has a 100-article cap, except for `ALL_RELEV` has a 250-article cap. 

**2. Cleaning**

* `relevant_filter.py` takes files from the `gdelt_results` folder and generates labels for headline relevance: `1` if it contains ("race" and ("critical" or "theory") or "crt", `0` otherwise
	* Creates `relevant_results` folder, with a file for each state that includes the relevant label to identify CRT-relevant headlines. 
* `select_relevant.py` takes all files from the `gdelt_results` folder and filters out articles that are not labeled as relevant to CRT, such that each row corresponds to a unique headline. 
	* Creates `all_relevant.csv`
* `select_relevant_by_URL.py` takes all files from the `gdelt_results` folder and filters out articles that are not labeled as relevant to CRT, such that each row corresponds to a unique URL.  
	*  Creates `all_relevant_by_URL.csv`, which contains repeated headlines in case multiple URLs link to articles with the same headline. 

**3. Clustering for training dataset selection**  

* `headline_clustering.py` creates 100 headline clusters using unsupervised K-means clustering with BERT pre-trained model sentence embeddings 
	* Creates `cluster_centers.csv`, which is used to identify 100 headlines for the human-labeled validation dataset
	* Creates `cluster_results.csv`, which contains cluster assignments for all CRT headlines in the dataset.
* The `coding` folder contains files for the validation dataset (rater 1, rater 2, and consensus) and GPT performance evaluation (GPT coding of validation set). 
	* These files can be used for calculating interrater agreement and GPT performance metrics.

**4. GPT label generation**

* `get_labels.py` generates labels from GPT-4-Turbo using the OpenAI API. Queries are sent with scripts from `query_gpt4.py`. 
	* Creates output files `GPT_actors.csv` and `GPT_stances.csv`

**5. Combining datasets** 

* `combine_metrics.py` takes in `all_relevant.csv` and augments it with the following data to create `coverage_by_unique_headline.xlsx`: 
	* Assignments from unsupervised clustering results in `cluster_results.csv` (also removes irrelevant clusters)
	* News frame labels from `GPT_actors.csv` and `GPT_stances.csv`
* `combine_metrics.py` also takes in `all_relevant_with_URL.csv` and augments it with the following data to create `coverage_by_unique_URL.json`: 
	* Partisan audience bias scores for URL domains from `bias_scores.csv` (Robertson et al. 2018)
	* `reddit_post_data.json`, which includes Reddit posts with exposure and engagement metrics from the Pushshift Reddit dumps

**6. Plotting trends** 

**7. Time series modeling** 

**8. Supervised Approach: GPT-4 Prompt Engineering** 

**9. Unsupervised Approach: Topic Modeling with GPT-4 Augmentation** 
	
**References**

GDELT 2.0 Event Database. https://www.gdeltproject.org/ (DOC API Documentation [here](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/))

Ronald E. Robertson, Shan Jiang, Kenneth Joseph, Lisa Friedland, David Lazer, and Christo Wilson. 2018. Auditing Partisan Audience Bias within Google Search. Proc. ACM Hum.-Comput. Interact. 2, CSCW, Article 148 (November 2018), 22 pages. https://doi.org/10.1145/3274417