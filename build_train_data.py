import pandas as pd
import os

"""change the dataformat"""

path = "data/cwiwithlevels/english"
files= os.listdir(path)
train_data= open('data/cwiwithlevels/english/sentences.txt', 'w',encoding='utf-8')
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
                train_data.write(line[2] + '\n',)
                print(line[2])