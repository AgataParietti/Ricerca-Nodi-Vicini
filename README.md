# Ricerca-Nodi-Vicini
Implementazione embeddings per la ricerca di nodi vicini su Fuseki.

## Requisiti Software
Per il funzionamento del programma è necessario avere:
1. Python 3 e le librerie *pandas, random, gensim, pytorch, numpy, csv, tqdm, time, cython, torchkge e rdflib*
2. Java 11 o superiore (testato con java 11)

## Primo step: set dei file
Prima di scaricare il contenuto di questa repository è necessario scaricare Apache Jena e Apache Jena Fuseki. Per il downolad cliccare [qui](https://jena.apache.org/download/) e dalla sezione **Apache Jena Binary Distributions** scaricare:
- apache-jena-fuseki-4.7.0.zip
- apache-jena-4.7.0.zip
<br /> Saranno necessarie entrambe le cartella unzippate. Poi scaricare il contenuto della repository e mettere tutti i file e cartelle (comprese quelle di Apache) in un'unica cartella (nel nostro caso Nodi_Vicini), come mostrato in figura.
![](img/passo1.png?raw=true)

## Secondo step: set del manifest.txt
Per poter far funzionare le funzioni che estendono SPARQL su Fuseki è necessario aggiungere i file .jar nel classpath del file .jar del server Fuseki. Quindi è molto importante seguire i passaggi:

1. Spostare il file manifest.txt nella cartella *apache-jena-fuseki-4.7.0*
2. Aprire il terminale ed entrare attraverso il comando *cd* nella cartella  *apache-jena-fuseki-4.7.0*.
3. Eseguire il seguente comando da terminale:
```
jar umf manifest.txt fuseki-server.jar
```

## Terzo step: effettuare l'embedding
### Dataset salvato in locale
Nella cartella *dataset* in questa repository è già presente un dataset di esempio fornito da **Apache Jena** chiamato *cheeses.ttl*. Quindi nella cartella *functions_and_embeddings* sono già stati caricati gli embeddings di questo dataset. Nel caso se ne voglia aggiungere uno nuovo, inserire il file nella cartella *dataset* ed eseguire gli script. <br>
Gli script python hanno il compito di creare, a partire dal file contenente il dataset, due tipologie di embeddings e salvarle in due file CSV nella cartella *functions_and_embeddings*. È importante che tali file CSV rimangano in questa directory per il funzionamento delle funzioni java su Fuseki. Nel caso in cui siano già presenti due file contenenti gli embeddings, questi verranno sovrascritti. Consigliamo, nel caso in cui non si vogliano perdere gli embeddings di un certo dataset, di fare delle copie di questi file in una cartella a parte.
 <br> 
 Per eseguire gli script python:
 1. Aprire il terminale nella cartella dove sono presenti i file python
 2. Eseguire i file da terminale, scegliere la prima opzione e seguire le istruzioni che compariranno. Non eseguire lo script *dataset_preparation.py*
 ```
 python te_embedding.py
 python w2v_embedding.py 
 ```
Controllare che nella cartella *functions_and_embeddings* siano stati aggiunti/modificati i due file *embedding_transe.csv* e *embedding_w2v.csv*

### Prendere dati da RDF Store
È possibile anche ottenere i dati direttamente da un RDF Store fornendo un default graph o un grafo specifico. Di default è stato scelto di prendere tutte le triple del grafo *https://query.wikidata.org/sparql*, effettuando la query seguente: 
```
CONSTRUCT {?s ?p ?o}

WHERE {
?s ?p ?o
}
LIMIT 100000
 ```
Il grafo e la query da eseguire possono essere scelti a piacere andando a modificare:
- per il grafo il file *sparql.txt* 
- per la query il file *query.txt*

Successivamente si va a salvare gli embeddings dei nodi nei file *embedding_transe.csv* e *embedding_w2v.csv* nella cartella *functions_and_embeddings*. È importante che tali file CSV rimangano in questa directory per il funzionamento delle funzioni java su Fuseki. Nel caso in cui siano già presenti due file contenenti gli embeddings, questi verranno sovrascritti. Consigliamo, nel caso in cui non si vogliano perdere gli embeddings di un certo dataset, di fare delle copie di questi file in una cartella a parte.
<br>
Per eseguire gli script python:
 1. Aprire il terminale nella cartella dove sono presenti i file python
 2. Eseguire i file da terminale, scegliere la seconda opzione e seguire le istruzioni che compariranno. Non eseguire lo script *dataset_preparation.py*
 ```
 python te_embedding.py
 python w2v_embedding.py 
 ```
 In questo caso, però, non si avranno dati da caricare su Fuseki, che necessita di un file salvato in locale per poter fare l'upload del dataset. Di conseguenza questa opzione è consigliabile se si vuole fare l'embedding di una Knowledge Base molto grande e, successivamente, lavorare su Fuseki con un sottoinsieme di dati per la ricerca di nodi vicini. Tale sottoinsieme occuperà uno spazio minore in memoria rispetto alla KB, ma avendo gli embeddings di tutti i nodi è possibile lavorare con informazioni complete, che tengono conto di tutte le triple processate. 

## Quarto step: aprire Fuseki e caricare il dataset
Una volta preparati gli embeddings è necessario aprire Fuseki. Per fare questo aprire da terminale la cartella *apache-jena-fuseki-4.7.0* ed eseguire il seguente comando:
- su sistemi Unix
```
 ./fuseki-server
 ```
 - su sistemi Windows
 ```
 fuseki-server
 ```
 Il terminale dovrebbe restituire un output simile a quello in figura.
  ![](img/fuseki1.png?raw=true)
 Come è possibile vedere il server si apre sulla porta 3030, e quindi andare sul browser per entrare in localhost:3030. Apparirà la seguente schermata.
 ![](img/fuseki2.png?raw=true)
 1. Cliccare su **add one** e poi inserire il nome del dataset e scegliere che tipo di dataset si vuole creare. Si consiglia di scegliere l'opzione *Persistent (TDB2)*
 2. Una volta creato il dataset cliccare su **add data** e poi *select files*. Selezionare il file turtle nella cartella dataset. Cliccare infine su *upload now* 
 ![](img/fuseki3.png?raw=true)
 3. Cliccare su query in alto a sinistra, sotto il nome del dataset.

## Quinto step: query e funzioni java
Una volta sulla sezione query di Fuseki possiamo usare le funzioni implementate per fare la ricerca di nodi vicini. Le funzioni che estendono SPARQL sono due: **W2V** che implementa l'embedding Word2Vec e **TE** che implementa l'embedding TransE. Per i dettagli teorici leggere il pdf della relazione. <br>
La query di base da usare per calcolare la distanza di tutti i nodi con tutti gli altri nodi usando l'embedding Word2Vec è la seguente:
```
PREFIX f: <java:>
SELECT * WHERE {
  { SELECT DISTINCT ?s1 { ?s1 ?p1 ?o1 } }
  { SELECT DISTINCT ?s2 { ?s2 ?p1 ?o1 } }
  FILTER(STR(?s1)<STR(?s2))
  BIND(f:TE(?s1,?s2) as ?distTE)
  BIND(f:W2V(?s1,?s2) as ?distW2V)
} ORDER BY ?distTE
 ```
Se si hanno dataset grandi è possibile che l'esecuzione della query non sia immediata. Nella relazione sono riportati altri esempi di query.

## Developed by [Agata Parietti](https://github.com/AgataParietti) and [Sofia Galante](https://github.com/Sofia-Galante)
