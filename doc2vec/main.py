import numpy as np
from crawler.crawl import crawl
from opt import parse
import os
import json
import gensim
import collections
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import matplotlib.pyplot as plt
import ipdb
def preprocess_dict(papers):
    data = []
    for title, paper in papers.items():
        paper['title'] = title
        data.append(paper)
    data = sorted(data, key=lambda x:x['title']) 
    return data
def tsne(data):
    from sklearn.manifold import TSNE
    data_emb = TSNE(n_components=2, random_state=1208, verbose=1).fit_transform(data)
    return data_emb
def clustering(data, n_clusters=5):
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=1208)
    data_dist = kmeans.fit_transform(data)
    cat = kmeans.labels_
    return kmeans, cat, data_dist
def print_section(papers):
    for paper in papers:
        print(paper['section'])
    
def main():
    opt = parse()
    print(opt)
    if not os.path.isfile(opt.json_data):
        print('file %s not exist' %opt.json_data)
        print('start crawling from %s' % opt.url)
        papers = crawl(opt)
        json.dump(papers, open(opt.json_data, 'w'))
    else:
        print('file %s exists' %opt.json_data)
        papers = json.load(open(opt.json_data,'r'))
    papers = preprocess_dict(papers)
    tagged_docs = []
    titles = []
    for i, paper in enumerate(papers):
        title = paper['title']
        titles.append(title)
        abstract = paper['abstract']
        tokens = gensim.utils.simple_preprocess(abstract)
        tagged_doc = TaggedDocument(tokens, [i])
        tagged_docs.append(tagged_doc)
    model = Doc2Vec(vector_size=128, min_count=2, epochs=50, seed=1208)
    model.build_vocab(tagged_docs)
    print('Model Description :\nsamples:{}, epochs:{}'.format(model.corpus_count, model.epochs))
    print('Start Training.')
    model.train(tagged_docs, total_examples=model.corpus_count, epochs=model.epochs)
    print('Finish Training.')
    d2v = model.docvecs.vectors_docs
    kmeans, cat, data_dist = clustering(d2v, n_clusters=opt.n_class)
    # get top5 paper per cluster from kmeans
    top_papers = {}
    for label in range(opt.n_class):
        idx = (cat == label)
        data = data_dist[idx]
        data = data[:,label]
        topk_idx = data.argsort()[:opt.topk]
        paper = np.array(papers)[idx][topk_idx]
        top_papers[label] = paper
        print('---------------------')
        print('topic {}'.format(label))
        print_section(paper)
    print('Do t-SNE visualization.')
    d2v_tsne = tsne(d2v)
    for label in range(opt.n_class):
        idx = (cat == label)
        plt.scatter(x=d2v_tsne[idx,0], y=d2v_tsne[idx,1], s=2)
    print('Finsih t-SNE, output to tsne.png')
    plt.savefig('tsne.png')
    '''
    ranks = []
    second_ranks = []
    for i in range(len(papers)):
        inferred_vector = model.infer_vector(tagged_docs[i].words)
        sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
        rank = [docid for docid, sim in sims].index(i)
        ranks.append(rank)
        second_ranks.append(sims[1])
    inferred_vector = model.infer_vector(tagged_docs[0].words)
    sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
    '''
        

if __name__ == '__main__':
    main()
