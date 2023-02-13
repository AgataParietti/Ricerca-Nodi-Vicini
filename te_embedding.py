from torch.optim import Adam

from torchkge.data_structures import KnowledgeGraph

import pandas as pd
import numpy as np
import csv

from torchkge.models import TransEModel
from torchkge.sampling import BernoulliNegativeSampler
from torchkge.utils import MarginLoss, DataLoader

from tqdm.autonotebook import tqdm

import dataset_preparation

def main():
    # Hyper-parameters
    emb_dim = 10
    lr = 0.0004
    n_epochs = 50
    b_size = 10
    margin = 0.5

    # Load dataset
    data = dataset_preparation.create_dataframe()

    data = data.reindex(columns=['head', 'tail', 'rel'])
    data.rename( columns={"head": "from", "tail": "to"}, inplace=True)

    kg_train = KnowledgeGraph(df=data)

    # Define the model and criterion
    model = TransEModel(emb_dim, kg_train.n_ent, kg_train.n_rel, dissimilarity_type='L2')
    criterion = MarginLoss(margin)


    # Define the torch optimizer to be used
    optimizer = Adam(model.parameters(), lr=lr, weight_decay=1e-5)

    sampler = BernoulliNegativeSampler(kg_train)
    dataloader = DataLoader(kg_train, batch_size=b_size)

    iterator = tqdm(range(n_epochs), unit='epoch')
    for epoch in iterator:
        running_loss = 0.0
        for i, batch in enumerate(dataloader):
            h, t, r = batch[0], batch[1], batch[2]
            n_h, n_t = sampler.corrupt_batch(h, t, r)

            optimizer.zero_grad()

            # forward + backward + optimize
            pos, neg = model(h, t, r, n_h, n_t)
            loss = criterion(pos, neg)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
        iterator.set_description(
            'Epoch {} | mean loss: {:.5f}'.format(epoch + 1, running_loss / len(dataloader)))
    
    #Save Embeddings
    embeddings = model.get_embeddings()
    v_emb = embeddings[0].numpy()
    r_emb = embeddings[1].numpy()
    total_emb = np.concatenate((v_emb, r_emb))

    coordinates = list()
    for i in range(emb_dim):
        coordinates.append(f'v{i+1}')

    total_emb = pd.DataFrame.from_records(total_emb, columns = coordinates)

    v_dict = dict(zip(kg_train.ent2ix.values(), kg_train.ent2ix.keys()))
    r_dict = dict(zip(kg_train.rel2ix.values(), kg_train.rel2ix.keys()))

    v_df = pd.DataFrame.from_dict(v_dict, orient='index', columns= ['element'])
    r_df = pd.DataFrame.from_dict(r_dict, orient='index', columns=['element'])
    total_df = pd.concat([v_df, r_df], axis=0, ignore_index=True)

    df_all = pd.concat([total_df, total_emb], axis=1)

    df_all.to_csv('functions_and_embeddings/embedding_transe.csv', index=False, header=False, quoting=csv.QUOTE_NONE, escapechar=';', sep = ';')

    


if __name__ == "__main__":
    main()
