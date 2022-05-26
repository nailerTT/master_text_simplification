import pandas as pd
import textstat	

def sent_evaluator(_string):
    j=_string
    #print(j)
    FOG=textstat.gunning_fog(j)
    ARI=textstat.automated_readability_index(j)
    CLI=textstat.coleman_liau_index(j)
    mean=(FOG+ARI+CLI)/3
    print(FOG,ARI,CLI,mean)
    return mean

if __name__ == '__main__':
    Idea=pd.read_csv(r"eval_test.csv",encoding="utf-8" )
    i=len(Idea)
    print(i)
    for x in range(0,i):
        print(x)
        print(sent_evaluator(Idea['sentence'][x]))
    print(sent_evaluator("We sleep in what had once been the gym."))