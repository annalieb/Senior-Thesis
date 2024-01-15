# Documentation: https://www.sbert.net/
# Quickstart: https://www.sbert.net/docs/quickstart.html
# paper: https://arxiv.org/pdf/1908.10084.pdf
# blog: https://blog.ml6.eu/decoding-sentence-encoders-37e63244ae00
# hugging face: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

from sentence_transformers import SentenceTransformer, util
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from IPython.display import display

def get_sentence_embeddings(fName, model): 
    articles = pd.read_csv(fName)
    headline_list = articles['title'].tolist()
    embeddings = np.array(model.encode(headline_list))
    print(type(embeddings[0]))
    print("vector length", len(embeddings[0]))

    return embeddings, headline_list

def assign_headlines(headlines, centers, transformer_model): 
    '''assign a list of headlines (list of str) to clusters (list of str)'''
    headline_embeddings = transformer_model.encode(headlines)
    center_embeddings = transformer_model.encode(centers)

    # Compute cosine similarity between all embeddings and centroids
    cos_sim = util.cos_sim(headline_embeddings, center_embeddings)

    # find closest centroid for each headline
    cos_sim = cos_sim.numpy()
    # get max cosine similarity for each row, ie. closest cluster for each headline
    preds = np.argmax(cos_sim, axis=1) 

    # write cluster results to file
    clusters_df = pd.DataFrame({"title": headlines, 
                                "cluster_label": preds})
    return clusters_df

def main():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # Note: initial clustering used only articles from 2021 and 2022
    # To replicate results, "all_relevant_2021_2022.csv" should contain only 
    # a subset of headlines from "all_relevant.csv" from 2021-2022. 
    embeddings, sentences = get_sentence_embeddings("all_relevant_2021_2022.csv", model)
    kmeans = KMeans(n_clusters=100, random_state=0, n_init="auto")
    kmeans.fit(embeddings)
    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_
    # write cluster results to file
    clusters_df = pd.DataFrame({"title": sentences, 
                                "cluster_label": labels})
    clusters_df.to_csv('cluster_results.csv', index=False)

    # Compute cosine similarity between all embeddings and centroids
    # to find 100 closest to each centroid
    cos_sim = util.cos_sim(embeddings, centroids)
    cos_sim = cos_sim.numpy()
    # get max cosine similarity for each column, ie. closest sentence for each cluster
    centers = np.argmax(cos_sim, axis=0) 
    center_headlines = [sentences[i] for i in centers]

    # write headline cluster centers to .csv file
    num_clusters = list(range(100))
    centers_df = pd.DataFrame({"cluster_label": num_clusters, 
                               "cluster_center": center_headlines})
    centers_df.to_csv('cluster_centers.csv', index=False)

    # get cluster assignments for headlines from 2020
    # To replicate results, "all_relevant_2020.csv" should contain only 
    # a subset of headlines from "all_relevant.csv" from 2020. 
    headlines = pd.read_csv("all_relevant_2020.csv")['title'].tolist()
    centers = pd.read_csv("cluster_centers.csv")['cluster_center'].tolist()
    
    clusters_2020 = assign_headlines(headlines, centers, model)
    clusters_2020.to_csv('cluster_results_2020.csv', index=False)

# main()
    
def fill_in_missing(): 
    model = SentenceTransformer('all-MiniLM-L6-v2')
    missing = ["A Momma Bear in Carmel New York Fights Back Against Critical Race Theory and Confronts School Board", 
               "How Biden Aims to Take Critical Race Theory to the Next Level in Your School",
               "Fox & Friends bring on guest to suggest schools are using critical race theory to tell kids to  murder our police officers  ",
               "Rep . Lee Zeldin : Critical race theory radical politicization of education undermines who we are as Americans", 
               "Rep . Lee Zeldin : Critical race theory radical politicization of education undermines who we are as Americans Critical race theory requires that everything be viewed through the lens of race . It focuses on identity group politics Rep . Lee Zeldin R..."
               ]
    centers = pd.read_csv("cluster_centers.csv")['cluster_center'].tolist()
    missing_clusters = assign_headlines(missing, centers, model)
    display(missing_clusters)
    missing_clusters.to_csv("missing_headline_clusters.csv")

fill_in_missing()