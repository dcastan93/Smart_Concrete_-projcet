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
import csv
import glob


#%%
def main(raw_path, interim_path, n_rep, n_datos, raw_path_1):
    
    all_files = glob.glob(base_path + raw_path)
    read_csv = []
    count = 0
    contador=0
    contador1 = n_rep
    while contador <= len(all_files):
        count = 0
        read_csv = []
        folder = all_files[contador:contador1]
        for i in folder:
            break
                   
            df = pd.read_csv(i, sep=";", header=0, names=['Time', 'MDef', 'lambda'], usecols=['Time', 'MDef'])
            df = df[54:len(df)+1]
            df.to_csv(os.path.join(base_path + interim_path + fold er_save + save + name +'.csv'),  index = False, sep=',')
       
            count = count+1
        
        contador=contador + n_rep
        contador1 = contador1 + n_rep
    
    
 
    
#    logger.info('seleccionando los archivos .csv')
    all_files = glob.glob(base_path + raw_path_1)
#    logger.info('se seleccionaron srt(all_files) archivos')
    for i in all_files:
        
        file_name = str(i)
        file_save = os.path.dirname(i)
        df = (pd.read_csv(i))
        df['tiempo'] = df[df.columns[[3]]]
        df['voltaje'] = df[df.columns[[4]]]
        df = df[['tiempo','voltaje']]
        lon = len(df)
        df = df[100:lon].reset_index(drop=True)

        if df['voltaje'].iloc[0]>= 0:
            count = 0
            while df['voltaje'].iloc[count]>= 0:
                count = count + 1
            if count >=n_datos:
                    df = df[0:2300]
                    
            else:
                    value = count + n_datos
                    df = df[value:2300]
        
        else:
            c = 0
            while df['voltaje'].iloc[c]<= 0:
                c = c + 1
            if c >=n_datos:
                df = df[n_datos:2300]
                    
            else:
                df = df[c:2300]
            
            
            
        df.to_csv(os.path.join(file_save, os.path.basename(file_name)),  index = False, sep=',')
        
        

    all_files = glob.glob(base_path + raw_path_1)
    read_csv = []
    count = 0
    contador=0
    contador1 = 2*n_rep
    while contador <= len(all_files):
        count = 0
        read_csv = []
        folder = all_files[contador:contador1]
        for i in folder:
            
            file_name = str(i)
            Folder_name = os.path.dirname(i)
            Folder_name = os.path.basename(Folder_name)
            file_name = os.path.basename(file_name)
            file_name = os.path.splitext(file_name)[0]
            V_name = 'Voltaje_'+(file_name)
            file_name = str(i)
            df = (pd.read_csv(i))
            df[V_name] = df[df.columns[[1]]]
            df = df.drop(['voltaje', 'tiempo'], axis = 1)
            df = df[(df > 0).all(1)].reset_index(drop=True)
            
            
            if count ==0:
                read_csv = df
            
            else:
                
                df = df[0:len(read_csv)]
                read_csv = read_csv.merge(df, left_index=True, right_index=True)
                
            
            count = count+1
            read_csv.to_csv(os.path.join(base_path + interim_path, Folder_name+'.csv'),  index = False, sep=',')
            
    
        
        contador=contador + 2*n_rep
        contador1 = contador1 + 2*n_rep
        
#    logger.info("Finished program")
    
    return None

#%%
if __name__ == '__main__':
    
    raw_path = '/data/Interim/Def_08_2/*.csv'
    raw_path_1 = '/data/Interim/1_Hz_6/**/**/*.csv'
    file = '1_Hz_6'
    interim_path = '/data/Interim/1_Hz_6'
    n_rep = 5
    n_datos = 25

    main(raw_path, interim_path, n_rep, n_datos, raw_path_1)