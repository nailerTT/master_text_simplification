from gensim.models import word2vec

"""train word2vec model"""
sentences = word2vec.Text8Corpus('data/text8')
model = word2vec.Word2Vec(sentences, vector_size=100, window=5, min_count=2, workers=4)
model.save("data/model/text8.model")