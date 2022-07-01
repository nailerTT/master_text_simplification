import gensim
import pandas as pd
from gensim.models import Word2Vec
import os
from sklearn import preprocessing
from sklearn import svm
from sklearn import preprocessing
import pdb
import numpy
from nltk.corpus import wordnet
import babelnet as bn
from babelnet.language import Language

class Simplifier2:
    def __init__(self):
        """ Load word2vec model """
        model_word2vec = Word2Vec.load('data/model/text8.model')

        self.steps = open('steps_2.txt', 'w')
    
    """ select the english word """
    def english_check(self,word):
        for i in range(0,len(word)):
            if(word[i]<='z' and word[i]>='a'):
                continue
            else:
                return False
        return True

    """ Check POS, we only want to replace nouns, adjectives and verbs. """
    def check_if_replacable(self, word):
        
        word_tag = pos_tag([word])
        if 'NN' in word_tag[0][1] or 'JJ' in word_tag[0][1] or 'VB' in word_tag[0][1]:
            return True
        else:
            return False

    """ get the specific type file (such as"Train") """
    def get_data(self,path,type):
        self.steps.write(path + '\n')
        files= os.listdir(path)
        words=[]
        flag=[]
        feats=[]
        result=[]
        indx=0

        """ get all the files"""
        for file in files: 
            if not os.path.isdir(file): 
                name,file_name=file.split('.')
                if(file_name!="csv" or name.find(type)==-1):
                    continue
                print(name+":")
                new_words,new_flag=self.get_file(path+"/"+file)
                words.extend(new_words)
                flag.extend(new_flag)

        for item in words:
            item=item.lower()
            """ ignore the word could not be proccessed by the model """
            if(self.english_check(item)==False):
                continue
            try:
                temp =model_word2vec.wv[item]
            except KeyError:
                print ("Error: not find "+item)
            else:
                #print(item)
                #print(len(item),len(model_word2vec.wv[item]))
                temp=[len(item)]+temp
                feats.append(temp)
                result.append(flag[indx])
                indx+=1
        
        #print(feats,result)
        #print(len(feats),len(result))
        return feats,result          

    """get the data from a file"""   
    def get_file(self,file_name):
        self.steps.write(file_name + '\n')
        data = pd.read_csv(file_name)
        length_df=len(data)
        words=[]
        flag=[]
        for num in range(0,length_df):
            line=list(data.iloc[num])
            if(line[5].find('-')==-1 and line[5].find(' ')==-1 and line[5].isalpha()):
                
                try:    
                    temp=int(line[10])
                except ValueError:
                    print(line[5]+"has no label")
                    continue
                else:
                    words.append(line[5])
                    flag.append(int(line[10]))
            else:
                continue
        return words,flag

    """train the svm"""  
    def get_svm(self,train_feats,train_labels):
        self.clf = svm.SVC(gamma=0.001, C=100.)
        self.clf.fit(train_feats, train_labels)
    
    """predict labels"""
    def svm_classification(self,feats):
        labels=self.clf.predict(feats)
        return labels

    """get sym from babelnet"""
    def get_sym(self,word_):
        byl = bn.get_synsets(word_, from_langs=[Language.EN])
        print(byl)
        for item in byl:
            print(item)
        
if __name__ == '__main__':
    model_word2vec = Word2Vec.load('data/model/text8.model')
    #print(model_word2vec.wv['blue'])
    S=Simplifier2()
    feats,labels=S.get_data("data/cwiwithlevels/english","Train")
    S.get_svm(feats,labels)
    test_feats,test_labels=S.get_data("data/cwiwithlevels/english","Test")
    test_re_labels=S.svm_classification(test_feats)
    #print(test_re_labels)
    #print(test_labels)
    #print(len(test_re_labels),len(test_labels))
    num=0
    c=0
    for item in test_re_labels:
        if item==test_labels[num]:
            c+=1
        num+=1
    S.get_sym('word')
    print(c,len(test_labels))