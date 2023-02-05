import pandas as pd
import rdflib

def code_name(element):
    if isinstance(element, rdflib.term.URIRef):
        return '<'+str(element)+'>'
    else:
        if element.language:
            return '\"'+str(element)+'\"@'+element.language
        else:
            return '\"'+str(element)+'\"'

def create_dataframe():
    g = rdflib.Graph()
    print('Inserire il nome del dataset. NOTA BENE: il file deve trovarsi nella cartella dataset ed è necessario '
          'inserire anche l\'estensione del file.')
    file = input()
    g.parse('dataset/' + file)
    data = list()
    for s, p, o in g.triples((None, None, None)):
        head = code_name(s)
        rel = code_name(p)
        tail = code_name(o)
        data.append([head, rel, tail])
    df = pd.DataFrame.from_records(data, columns = ['head', 'rel', 'tail'])
    df = df.sort_values(by=['head'], ignore_index=True)
    return df