import pandas as pd
import random

def from_ttl_to_df(data_path):
    with open(data_path) as f:
        data = f.read()

    data = data.split(sep = '.')
    data = [e for e in data if e != '']
    final_data = list()
    for ttl in data:
        head = ttl.split()[0]
        ttl = ttl.split(sep = ';')
        for d in ttl:
            d = d.split()
            if len(d) < 3:
                d = [head, d[0], d[1]]
            final_data.append(d)

    df = pd.DataFrame.from_records(final_data, columns = ['head', 'rel', 'tail'])
    df = df.sort_values(by=['head'], ignore_index=True)
    return df


def from_df_to_phrases(df, n, d):
    sequences = list()
    random.seed(2208)
    for v1 in df['head'].unique():
        nv = n
        while nv > 0:
            sentence = list()
            currentV = v1
            sentence.append(v1)
            dv = d
            while dv > 0:
                r = df.loc[df['head'] == currentV, 'rel'].values.tolist()
                r = random.choice(r)
                sentence.append(r)
                v2 = df.loc[(df['head'] == currentV) & (df['rel'] == r), 'tail'].values.tolist()
                v2 = random.choice(v2)
                currentV = v2
                sentence.append(v2)
                dv = dv-1
            sequences.append(sentence)
            nv = nv-1
    return sequences

