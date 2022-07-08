from gensim.models import word2vec
import pandas as pd
import os
import nltk

"""get the raw data"""
path = "data/cwiwithlevels/english"
files= os.listdir(path)
train_data= open('data/cwiwithlevels/english/sentences.txt', 'w',encoding='utf-8')
raw_corpus=[]
print(files)
for file in files: 
    if not os.path.isdir(file): 
        name,file_name=file.split('.')
        if(file_name!="csv"):
            continue  
        data = pd.read_csv(path+"/"+file)
        length_df=len(data)
        print(file,length_df)
        for num in range(1,length_df):
            line=list(data.iloc[num])
            pre=list(data.iloc[num-1])
            if(num!=1 and len(line[2])==len(pre[2])):
                continue
            else:
                raw_corpus.append(line[2])
                train_data.write(line[2] + '\n')


with open("data/text8.txt", "r") as f:  
    plus_data = f.read()  
length_df=len(plus_data)
print(length_df)
raw_corpus.append(plus_data)

process_corpus = [nltk.word_tokenize(t) for t in raw_corpus]

"""train word2vec model"""

model = word2vec.Word2Vec(sentences=process_corpus, vector_size=100, window=5, min_count=2, workers=4)
model.save("data/model/text8.model")