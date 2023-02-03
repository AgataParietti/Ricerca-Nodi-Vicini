# Ricerca-Nodi-Vicini
Implementazione embeddings per la ricerca di nodi vicini su Fuseki.

## Requisiti Software
Per il funzionamento del programma è necessario avere:
1. Python 3 e le librerie *pandas, random, gensim, pytorch, numpy, tqdm e torchkge*
2. Java 11

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
3. Spostare il file manifest.txt modificato nella cartella *apache-jena-fuseki-4.7.0* ed eseguire i seguenti comandi da terminale:
```
git status
git add
git commit
```
