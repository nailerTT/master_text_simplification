import pandas as pd
import textstat	
from sentence import Sentence
from evaluator import sent_evaluator
from simplifier_1 import Simplifier1

sent_arr=[]
temp=Sentence() 
S=Simplifier1()

Idea=pd.read_csv(r"eval_test.csv",encoding="utf-8" )
i=len(Idea)
print(i)

for x in range(0,i):
    print(x)
    print(sent_evaluator(Idea['sentence'][x]))
    temp.origin_sentence=Idea['sentence'][x]
    temp.origin_score=sent_evaluator(temp.origin_sentence)
    temp.simplified_sentence=S.simplify(temp.origin_sentence)
    temp.simplified_score=sent_evaluator(temp.simplified_sentence)
    sent_arr.append((temp))