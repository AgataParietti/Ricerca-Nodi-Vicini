# Ricerca-Nodi-Vicini
Implementazione embeddings per la ricerca di nodi vicini su Fuseki.

## Requisiti Software
Per il funzionamento del programma è necessario avere:
1. Python 3 e le librerie *pandas, random, gensim, pytorch, numpy, tqdm, cython e torchkge*
2. Java 11 o superiore (testato con java 11)

## Primo step: set dei file
Prima di scaricare il contenuto di questa repository è necessario scaricare Apache Jena e Apache Jena Fuseki. Per il downolad cliccare [qui](https://jena.apache.org/download/) e dalla sezione **Apache Jena Binary Distributions** scaricare:
- apache-jena-fuseki-4.7.0.zip
- apache-jena-4.7.0.zip
<br /> Saranno necessari entrambe le cartella unzippate. Poi scaricare il contenuto della repository e mettere tutti i file, cartelle (comprese quelle di Apache) nella stessa cartella, come mostrato in figura.
![](img/passo1.1.png?raw=true)

## Secondo step: settare il manifest.txt
Per poter far funzionare le funzioni che estendono SPAQL su Fuseki è necessario aggiungere i file .jar nel classpath del file .jar del server Fuseki. Quindi è molto importante seguire i seguenti step:
1. Aprire il file manifest.txt, che si presenterà come in figura:
![](img/manifest1.png?raw=true)
2. Accanto a *Class-Path:* scrivere l'absolute path della cartella *functions_and_embeddings* ricordandosi il '/' finale, come in figura.
![](img/manifest2.png?raw=true)
***NB*** E' molto importante lasciare una riga blank, come mostrato in figura!
3. Spostare il file manifest.txt modificato nella cartella *apache-jena-fuseki-4.7.0*, aprire il terminale ed entrare attraverso il comando *cd* nella cartella  *apache-jena-fuseki-4.7.0*.
4. Eseguire ii seguente comando da terminale:
```
jar umf manifest.txt fuseki-server.jar
```
5. Il terminale potrebbe restituire il seguente WARNING, in caso abbiate già svolto questo procedimento. Potete ignorarlo senza problemi.
![](img/manifest3.png?raw=true)

## Terzo step: eseguire gli script python per effettuare l'embedding
 ***È importante per il funzionamento degli script python che il file contenente il dataset sia in formato turtle (.ttl)*** 
 <br> Questi script hanno il compito di creare, a partire dal file tutrte, due tipologie di embeddings e salvarle in due file CSV nella cartella *functions_and_embeddings*. È importante che tali file CSV rimangano in questa directory per il funzionamento delle funzioni java su Fuseki. Nel caso in cui siano già presenti due file contenenti gli embeddings, questi verranno sovrascritti. Consigliamo, nel caso in cui non si vogliano perdere gli embeddings di un certo dataset, di fare delle copie di questi file in una cartella a parte.
 <br> 
 Per eseguire gli script python:
 1. Aprire il terminale nella cartella dove sono presenti i file python
 2. Eseguire i file da terminale e seguire le istruzioni che compariranno. Non eseguire lo script *kb_functions.py*
 ```
 python te_embedding.py
 python w2v_embedding.py 
 ```
Controllate che nella cartella *functions_and_embeddings* siano stati aggiunti/modificati i due file *embedding_transe.csv* e *embedding_w2v.csv*
