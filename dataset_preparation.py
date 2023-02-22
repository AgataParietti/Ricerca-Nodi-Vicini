import pandas as pd
import rdflib
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def code_name(element):
    if isinstance(element, rdflib.term.BNode):
        return None
    if isinstance(element, rdflib.term.URIRef):
        return '<'+str(element)+'>'
    else:
        if element.language:
            return '\"'+str(element)+'\"@'+element.language
        else:
            return '\"'+str(element)+'\"'

def create_dataframe():
    g = rdflib.Graph()
    file = None
    while(file == None):
        print('Si vuole fare l\'embedding di un grafo salvato in locale (nella cartella dataset) o online?')
        print('1 - locale\n2 - online')
        i = input()
        if i == "1":
            print('Inserire il nome del dataset compresa l\'estensione del file')
            file = input()
            file = 'dataset/'+file
        elif i == "2":
            print('Inserire la URL del grafo.')
            file = input()
        else:
            print('Scelta non valida.')

    g.parse(file)
    data = list()
    for s, p, o in g.triples((None, None, None)):
        head = code_name(s)
        rel = code_name(p)
        tail = code_name(o)
        data.append([head, rel, tail])
    df = pd.DataFrame.from_records(data, columns = ['head', 'rel', 'tail'])
    df = df.sort_values(by=['head'], ignore_index=True).dropna()
    return df