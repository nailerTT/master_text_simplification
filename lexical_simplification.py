import gensim
import pandas as pd
from gensim.models import Word2Vec
import os
from sklearn import preprocessing
from sklearn import svm
from sklearn import preprocessing
import numpy
from nltk.corpus import wordnet
import babelnet as bn
from babelnet.language import Language
from babelnet.pos import POS
from nltk import sent_tokenize, word_tokenize, pos_tag
from babelnet import BabelSynsetID
from nltk.stem.snowball import SnowballStemmer

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
            hook,temp=self.get_feats(item)
            if(hook==-1): 
                continue
            feats.append(temp)
            result.append(flag[indx])
            indx+=1    
        return feats,result

    def get_feats(self,item):
        if(self.english_check(item)==False):
            return -1,[]
        try:
            temp =model_word2vec.wv[item]
        except KeyError:
            print ("Error: not find "+item)
            return -1,[]
        else:
            temp=[len(item)]+temp
            return 1,temp
             

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
        self.clf = svm.SVC(C=200.0, kernel='rbf', gamma='auto',coef0=0.0, 
        shrinking=True, probability=False,tol=0.003, cache_size=300, class_weight=None, 
        verbose=False, max_iter=-1,random_state=None)
        self.clf.fit(train_feats, train_labels)
    
    """predict labels"""
    def svm_classification(self,feats):
        labels=self.clf.predict(feats)
        return labels

    def check_if_replacable(self, word):
        """ Check POS, we only want to replace nouns, adjectives and verbs. """
        word_tag = pos_tag([word])
        if 'NN' in word_tag[0][1] or 'JJ' in word_tag[0][1] or 'VB' in word_tag[0][1]:
            return True
        else:
            return False

    """get sym from babelnet"""
    def get_sym(self,word_):
        word_tag = pos_tag([word_])
        print(word_tag)
        if(self.check_if_replacable(word_)):
            if('NN' in word_tag[0][1]):
                word_type=[POS.NOUN]
            if('JJ' in word_tag[0][1]):
                word_type=[POS.ADJ]
            if('VB' in word_tag[0][1]):
                word_type=[POS.VERB]

            byl = bn.get_synsets(word_, from_langs=[Language.EN],poses=word_type)
            synwords=[]
            for item in byl:
                synset = bn.get_synset(BabelSynsetID(str(item.id)))
                """ a synset is an iterator over its senses"""
                for sense in synset:
                    synwords.append(sense.full_lemma)

            """remove the word with the same root"""
            stemmer=SnowballStemmer("english") 
            word_root=stemmer.stem(word_)
            syn_set=set(synwords)
            same_root_set=[]
            for item in syn_set:
                if(stemmer.stem(item)==word_root):
                    same_root_set.append(item)
            
            for item in same_root_set:
                syn_set.remove((item))
            
            print(syn_set)
            return syn_set
    
    """get the complex word of the sentence"""
    def get_difficult_words(self,sent):
        model_word2vec = Word2Vec.load('data/model/text8.model')
        feats,labels=S.get_data("data/cwiwithlevels/english","Train")
        S.get_svm(feats,labels)
        test_re_labels=S.svm_classification(test_feats)
        tokens = word_tokenize(sent)
         
    """get the complex word of the sentence"""
    def simplify(self,input):
        simplified = ''
        sent = input
        self.steps.write(sent + '\n')
        tokens = word_tokenize(sent)  # Split a sentence by words
        difficultWords = [t for t in tokens if self.freq_dict[t] < freq_top_n]
        self.steps.write('difficultWords:' + str(difficultWords) + '\n')
        
if __name__ == '__main__':
    model_word2vec = Word2Vec.load('data/model/text8.model')
    #print(model_word2vec.wv['blue'])
    S=Simplifier2()
    #print(test_re_labels)
    #print(test_labels)
    #print(len(test_re_labels),len(test_labels))
    """num=0
    c=0
    for item in test_re_labels:
        if item==test_labels[num]:
            c+=1
        num+=1
    """
    S.get_sym('positive')
    
    #print(c,len(test_labels))