# Ricerca-Nodi-Vicini
Implementazione embeddings per la ricerca di nodi vicini su Fuseki.

## Requisiti Software
Per il funzionamento del programma è necessario avere:
1. Python 3 e le librerie *pandas, random, gensim, pytorch, numpy, csv, tqdm, cython, torchkge e rdflib*
2. Java 11 o superiore (testato con java 11)

## Primo step: set dei file
Prima di scaricare il contenuto di questa repository è necessario scaricare Apache Jena e Apache Jena Fuseki. Per il downolad cliccare [qui](https://jena.apache.org/download/) e dalla sezione **Apache Jena Binary Distributions** scaricare:
- apache-jena-fuseki-4.7.0.zip
- apache-jena-4.7.0.zip
<br /> Saranno necessarie entrambe le cartella unzippate. Poi scaricare il contenuto della repository e mettere tutti i file e cartelle (comprese quelle di Apache) in un'unica cartella (nel nostro caso Nodi_Vicini), come mostrato in figura.
![](img/passo1.1.png?raw=true)

## Secondo step: set del manifest.txt
Per poter far funzionare le funzioni che estendono SPARQL su Fuseki è necessario aggiungere i file .jar nel classpath del file .jar del server Fuseki. Quindi è molto importante seguire i passaggi indicati a seconda del vostro Sistema Operativo.
### Per sistemi Unix
1. Aprire il file manifest.txt, che si presenterà come in figura:
![](img/manifest1.png?raw=true)
2. Accanto a *Class-Path:* scrivere l'absolute path della cartella *functions_and_embeddings* ricordandosi il '/' finale, come in figura.
![](img/manifest2.png?raw=true)
***NB*** E' molto importante lasciare una riga blank, come mostrato in figura!
3. Spostare il file manifest.txt modificato nella cartella *apache-jena-fuseki-4.7.0*, aprire il terminale ed entrare attraverso il comando *cd* nella cartella  *apache-jena-fuseki-4.7.0*.
4. Eseguire il seguente comando da terminale:
```
jar umf manifest.txt fuseki-server.jar
```
5. Il terminale potrebbe restituire il seguente WARNING, in caso abbiate già svolto questo procedimento. Potete ignorarlo senza problemi.
![](img/manifest3.png?raw=true)
### Per Windows
***Work in progress***

## Terzo step: effettuare l'embedding
Gli script python hanno il compito di creare, a partire dal file contenente il dataset, due tipologie di embeddings e salvarle in due file CSV nella cartella *functions_and_embeddings*. È importante che tali file CSV rimangano in questa directory per il funzionamento delle funzioni java su Fuseki. Nel caso in cui siano già presenti due file contenenti gli embeddings, questi verranno sovrascritti. Consigliamo, nel caso in cui non si vogliano perdere gli embeddings di un certo dataset, di fare delle copie di questi file in una cartella a parte.
 <br> 
 Per eseguire gli script python:
 1. Aprire il terminale nella cartella dove sono presenti i file python
 2. Eseguire i file da terminale e seguire le istruzioni che compariranno. Non eseguire lo script *dataset_preparation.py*
 ```
 python te_embedding.py
 python w2v_embedding.py 
 ```
Controllare che nella cartella *functions_and_embeddings* siano stati aggiunti/modificati i due file *embedding_transe.csv* e *embedding_w2v.csv*

## Quarto step: aprire Fuseki e caricare il dataset
Una volta preparati gli embeddings è necessario aprire Fuseki. Per fare questo aprire da terminale la cartella in cui sono salvate anche le due cartelle *apache-jena-fuseki-4.7.0* e *apache-jena-4.7.0* (nel nostro caso *cd Path_to_desktop/Nodi_Vicini/*) ed eseguire il seguente comando:
```
 apache-jena-fuseki-4.7.0/fuseki-server
 ```
 Il terminale dovrebbe restituire un output simile a quello in figura.
  ![](img/fuseki1.png?raw=true)
 Come è possibile vedere il server si apre sulla porta 3030, e quindi andare sul browser per entrare in localhost:3030. Apparirà la seguente schermata.
 ![](img/fuseki2.png?raw=true)
 1. Cliccare su **add one** e poi inserire il nome del dataset e scegliere che tipo di dataset si vuole creare. Si consiglia di scegliere l'opzione *Persistent (TDB2)*
 2. Una volta creato il dataset cliccare su **add data** e poi *select files*. Selezionare il file turtle nella cartella dataset. Cliccare infine su *upload now* 
 ![](img/fuseki3.png?raw=true)
 3. Cliccare su query in alto a sinistra, sotto il nome del dataset.

## Quinto step: quey e funzioni java
Una volta sulla sezione query di Fuseki possiamo usare le funzioni implementate per fare la ricerca di nodi vicini. Le funzioni che estendono SPARQL sono due: **W2V** che implementa l'embedding Word To Vector e **TE** che implementa l'embedding TransE. Per i dettagli teorici leggere il pdf della relazione. <br>
La query di base da usare per calcolare la distanza di tutti i nodi con tutti gli altri nodi usando l'embedding Word To Vector è la seguente:
```
 PREFIX f: <java:>
 SELECT ?s1 ?s2 ?dist WHERE {
   {
   SELECT ?s1 ?s2
   WHERE {
       ?s1 ?p1 ?o1.
       ?s2 ?p2 ?o2
       FILTER(?s1 != ?s2)
     } GROUP BY ?s1 ?s2
   }
     BIND(f:W2V(?s1, ?s2) as ?dist)
 }
 ```
Se si vuole usare l'embedding TransE sostituire *f:W2V* con *f:TE*. Se si hanno dataset grandi è possibile che l'esecuzione della query non sia immediata. Nella relazione sono riportati altri esempi di query.

## Developed by [Agata Parietti](https://github.com/AgataParietti) and [Sofia Galante](https://github.com/Sofia-Galante)
