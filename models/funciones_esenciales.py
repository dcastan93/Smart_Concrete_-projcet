import os
current_dir = os.getcwd()

#%%
import json

file_name = 'conf.json'
path = os.path.join(current_dir, f'{file_name}')
with open(path, 'r') as f:
    info_conf = json.load(f)
            
base_path = info_conf['base_path']
print(base_path)
#%%
import sys
sys.path.insert(0, base_path)
#%%
import time
import logging

import pandas as pd
import datetime as dt
import glob
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from sklearn.ensemble import GradientBoostingClassifier
from cookiecutter.main import cookiecutter
#%%
ruta = f'data/Raw'

#%%

def limpieza_csv_res(ruta, cnt):
    cnt = "02"
    ruta = f'data/Raw/'+ cnt
#   file_name = version
    path = os.path.join(base_path, ruta)
    all_files = glob.glob(path + "/*.csv")

    for i in all_files:
        
        file_name = str(i)
        df = (pd.read_csv(i))
        df['tiempo'] = df[df.columns[[3]]]
        df['voltaje'] = df[df.columns[[4]]]
        df = df[['tiempo','voltaje']]
        df.to_csv(os.path.join(base_path, f'data/interim/'+ cnt, os.path.basename(file_name)),  index = False, sep=',')
        
    return None

def merge_csv(ruta, cnt):
    ruta = f'data\interim'
    path = os.path.join(base_path, ruta)
    all_files = glob.glob(path + "/*.csv")
    read_csv = []
    count = 0
    
    for i in all_files:
        
        file_name = str(i)
        V_name = 'Voltaje_'+(os.path.basename(file_name))
        file_name = str(i)
        df = (pd.read_csv(i))
        df[V_name] = df[df.columns[[1]]]
        df = df.drop(['voltaje'], axis = 1)
        
        if count ==0:
            read_csv = df
        else:
            read_csv = read_csv.merge(df, how = 'left', on = 'tiempo')
            
        
        count = count+1
        read_csv.to_csv(os.path.join(base_path, f'data/interim/'+ cnt, 'Procesamiento_voltajes.csv'),  index = False, sep=',')
        

    return read_csv


def data_positivo(ruta, cnt):
    ruta = f'data\interim\Procesamiento_voltajes.csv'
    path = os.path.join(base_path, ruta)
    df = pd.read_csv(path)
    df=df[df[[1]]>0].reset_index(drop = True)
    df=df.dropna(how='all',axis=0).reset_index(drop=True)



def find_voltage():
    
    perc = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    count= int(len(df)/25)
    test = []
    
    
    while count<= 7:
        count_extremo = 0
        
        for i_extremo in range(1,40):
            
            t = int(perc[count]*25)
            valor = t + 25*count_extremo
            data = df.iloc[valor]
            count_extremo = count_extremo + 1
            test.append(data)
    
        count=count+1
        
    df = pd.DataFrame(test)
    
    
    



        
    
        
        
        
    
    
    
    
    
    
    
    
    
