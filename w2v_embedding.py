from gensim.models import Word2Vec
import pandas as pd
import random
import dataset_preparation
from tqdm.autonotebook import tqdm
import time
import csv

def from_df_to_phrases(df, n, d, reverse = False):
    sequences = list()
    random.seed(time.time())
    if reverse:
        col_1 = 'tail'
        col_2 = 'head'
    else:
        col_1 = 'head'
        col_2 = 'tail'
    for v1 in tqdm(df[col_1].unique(), desc = 'node'):
        nv = n
        while nv > 0:
            sentence = list()
            currentV = v1
            sentence.append(v1)
            dv = d
            while dv > 0:
                dv = dv - 1
                r = df.loc[df[col_1] == currentV, 'rel'].values.tolist()
                if len(r) > 0:
                    r = random.choice(r)
                    sentence.append(r)
                    if dv > 0:
                        v2 = df.loc[(df[col_1] == currentV) & (df['rel'] == r), col_2].values.tolist()
                        v2 = random.choice(v2)
                        currentV = v2
                        sentence.append(v2)
                        dv = dv - 1
            if reverse:
                sentence.reverse()
            sequences.append(sentence)
            nv = nv-1
    return sequences

def save_embedding(model):
    coordinates = list()
    for i in range(model.wv.vector_size):
        coordinates.append(f'v{i+1}')
    df_vectors = pd.DataFrame(model.wv.vectors, columns=coordinates)
    df_elements = pd.DataFrame(model.wv.index_to_key, columns=['element'])
    df_all = pd.concat([df_elements, df_vectors], axis=1)

    all_name = f'functions_and_embeddings/embedding_w2v.csv'

    df_all.to_csv(all_name, index=False, header=False, quoting=csv.QUOTE_NONE, escapechar=",")

def main():
    df = dataset_preparation.create_dataframe()

    #Hyper-parameters
    n_phrases = 10
    dim_phrases = 3
    workers = 4
    emb_dim = 10
    min_count = 1
    sg = 0
    
    #We do both forward and backward sentences because we want to have at least n example for every node (even the ones that are only in the tail column)
    sentences_forward = from_df_to_phrases(df, n_phrases, dim_phrases)
    sentences_backward = from_df_to_phrases(df, n_phrases, dim_phrases, reverse=True)
    sentences = [x for n in (sentences_forward, sentences_backward) for x in n]

    #Train model
    model = Word2Vec(sentences, workers=workers, vector_size = emb_dim, min_count=min_count, sg=sg)

    #Save Embeddings
    save_embedding(model)



if __name__ == "__main__":
    main()
