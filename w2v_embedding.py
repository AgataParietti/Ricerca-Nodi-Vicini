import kb_functions as kb
from gensim.models import Word2Vec

def save_embedding(model):
    coordinates = list()
    for i in range(model.wv.vector_size):
        coordinates.append(f'v{i+1}')
    df_vectors = pd.DataFrame(model.wv.vectors, columns=coordinates)
    df_elements = pd.DataFrame(model.wv.index_to_key, columns=['element'])
    df_all = pd.concat([df_elements, df_vectors], axis=1)

    all_name = f'dataset/embedding_w2v.csv'

    df_all.to_csv(all_name, index=False)

def main():
    print('Inserire il nome del dataset. NOTA BENE: il filw deve trovarsi nella cartella dataset ed è necessario '
          'che sia un file .ttl. Non inserire l\'estensione')
    file = input()
    data = kb.from_ttl_to_df('dataset/' + file + '.ttl')

    n = 2
    d = 3
    sentences = kb.from_df_to_phrases(df, n, d)
    model = Word2Vec(sentences, workers=4, vector_size = 2, min_count=1)
    save_embedding(model)