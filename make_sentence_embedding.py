# Documentation: https://www.sbert.net/
# Quickstart: https://www.sbert.net/docs/quickstart.html
# paper: https://arxiv.org/pdf/1908.10084.pdf

from sentence_transformers import SentenceTransformer

def main():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentences = ['This framework generates embeddings for each input sentence',
                 'Sentences are passed as a list of string.',
                 'The quick brown fox jumps over the lazy dog.']
    embeddings = model.encode(sentences)

    # print embeddings
    for sentence, embedding in zip(sentences, embeddings):
        print("Sentence:", sentence)
        print("Embedding:", embedding)
        print(len(embedding))
        print("")

main()
