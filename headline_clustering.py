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
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    # write cluster results to file
    clusters_df = pd.DataFrame({"sentence": sentences, 
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


main()

##def test(): 
##    X = np.array([[1, 2], [1.2, 4.2], [1, 0],
##                  [10, 2], [10.2, 4.2], [10, 0]])
##    kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(X)
##    centroids = kmeans.cluster_centers_
##    print(centroids)
##    # centroids: [10.,  2.], [ 1.,  2.]
##
##    centroid_ind = []
##    for c in centroids: 
##        centroid_ind.append(np.where((X == c).all(axis=1)))
##    print(centroid_ind)
##    print(len(centroid_ind))
##
##    a = np.array([[0, 1, 2],
##                  [0, 2, 4],
##                  [0, 3, 6]])
##    print(np.where((a == [0, 1, 2]).all(axis=1)))

# test()
