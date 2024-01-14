# Documentation: https://www.sbert.net/
# Quickstart: https://www.sbert.net/docs/quickstart.html
# paper: https://arxiv.org/pdf/1908.10084.pdf
# blog: https://blog.ml6.eu/decoding-sentence-encoders-37e63244ae00
# hugging face: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

from sentence_transformers import SentenceTransformer, util
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np

def get_sentence_embeddings(fName, model): 
    articles = pd.read_csv(fName)
    headline_list = articles['title'].tolist()
    embeddings = np.array(model.encode(headline_list))
    print("headline 1:", headline_list[0])
    print("vector 1:", embeddings[0])
    print(type(embeddings[0]))
    print("vector length", len(embeddings[0]))

    return embeddings, headline_list

def main():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings, sentences = get_sentence_embeddings("all_relevant.csv", model)
    kmeans = KMeans(n_clusters=100, random_state=0, n_init="auto")
    kmeans.fit(embeddings)
    centroids = kmeans.cluster_centers_

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

    # assign all headlines (including 2020 headlines) to clusters

    # make embeddings for full dataset
    embeddings, sentences = get_sentence_embeddings("all_relevant_with_2020.csv", model)
    preds = kmeans.predict(embeddings)

    # write cluster results to file
    clusters_df = pd.DataFrame({"headline": sentences, 
                                "cluster_label": preds})
    clusters_df.to_csv('cluster_results_with_2020.csv', index=False)
    return preds

main()
