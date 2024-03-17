import pandas as pd
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

""" 
Modularity in BERTopic: You can swap out any of these models or even remove them entirely. 
The following steps are completely modular:

Embedding documents
Reducing dimensionality of embeddings
Clustering reduced embeddings into topics
Tokenization of topics
Weight tokens
Represent topics with one or multiple representations 
"""

def prep_data(inFile): 
    '''read in GPT-4 actor descriptions, filter out "no actor" type descriptions'''

    actor_desc = pd.read_csv(inFile)
    all_docs = actor_desc['title'].tolist()
    
    # no_actor = []
    # docs = []
    # for i, d in enumerate(all_docs): 
    #     if ("does not reference" in d) or ("does not explicitly reference" in d): 
    #         no_actor.append(all_docs[i])
    #     else: 
    #         docs.append(all_docs[i])

    # print("no actor identified for", len(no_actor), "docs,", len(docs), "docs remaining")
    return all_docs

def make_topic_model(min_topic_size, ngram): 
    '''Construct BERTopic model'''
    # set representation to make topics more interpretable
    keybert_representation = KeyBERTInspired()

    # set vectorizer to add custom stopwords
    stop_words = stopwords.words('english') + ["actor", "actors", 
                                               "critical", "race", "theory", "crt",
                                               "headline", "primary"]
    ngram_range = (1, 1)
    if ngram == "bigram": 
        ngram_range = (1, 2)
    vectorizer_model = CountVectorizer(stop_words=stop_words, ngram_range=ngram_range) # ngram_range=(1, 2)

    # embed documents using sentence-BERT
    topic_model = BERTopic(min_topic_size=min_topic_size, 
                           embedding_model="all-MiniLM-L6-v2", 
                           vectorizer_model=vectorizer_model,
                           representation_model=keybert_representation) # S-BERT built in to BERTopic
    
    return topic_model


def main():
    docs = prep_data("GPT_actor_blurbs.csv")

    topic_model = make_topic_model(90, "unigram")

    print("Fitting model...")
    topics, probs = topic_model.fit_transform(docs)

    info = topic_model.get_topic_info()
    print(info)
    info.to_csv("baseline_bertopic_clusters_min=90_ngram=1.csv")

main()
# view stopwords list: 
# print("stopwords: ", stopwords.words('english') + ["actor", "actors", 
#                                                    "critical", "race", "theory", 
#                                                    "headline"])
    
# count = 0
# docs = prep_data("GPT_actor_blurbs.csv")
# for d in docs: 
#     if "No new teachers" in d: 
#         count += 1
# print(count) # output: 359