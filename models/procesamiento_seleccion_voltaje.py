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
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import glob
import matplotlib
import matplotlib.pyplot as plt
from adjustText import adjust_text
#%%
#import logging
#from logging.handlers import RotatingFileHandler
#
#file_name = 'preprocesamiento'
#logger = logging.getLogger()
#dir_log = os.path.join(base_path, f'models/loggers/{file_name}.log')
#
#handler = RotatingFileHandler(dir_log, maxBytes=2000000, backupCount=10)
#logging.basicConfig(level=logging.DEBUG,
#                    format="%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s",
#                    handlers = [handler])


#%%
def main(raw_path, raw_path_1, file_save, n_rep, fig_save):

#lectura por porcentaje    
    
#    logger.info('seleccionando los archivos .csv')
    all_files = glob.glob(base_path + raw_path)
    
    for i in all_files:
        
        file_name = str(i)
        Folder_name = os.path.basename(file_name)
        df = (pd.read_csv(i))
        
#        for cols in df.columns.tolist()[1:]:
#            data = df.ix[df[cols] > 0]     
    
        df_cen = df.filter(like='Cen')
        df_ext = df.filter(like='Ext')

        perc = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    
        count = 0 
             
        df_save = []
        while count <= 7:
            count_1 = 0 
            df_pro = []
            test_cen_mean = []
            test_cen_std = []
            
        
            for i_cen in range(1,int(len(df)/25)):
                
                t = int(perc[count]*25)
                n_centro = t + 25*count_1
                data_cen = (df_cen.iloc[n_centro]).reset_index(drop = True) 
                data_ext = (df_ext.iloc[n_centro])
                corriente = (data_ext/2200).reset_index(drop = True)
                resistencia = data_cen/ corriente
                
                
                if n_rep == 1:
                    resistencia_mean = resistencia
                    resistencia_mean = pd.Series.tolist(resistencia_mean)
                    resistencia_mean = ''.join(map(str, resistencia_mean))
                
                else:
                    resistencia_mean = resistencia.mean()
                    resistencia_std = resistencia.std()
                    
                if n_rep == 1:
                    test_cen_mean.append(resistencia_mean)
                    
                                
                else:
                    test_cen_mean.append(resistencia_mean) 
                    test_cen_std.append(resistencia_std)
                count_1 = count_1 + 1   
            
            name = perc[count]
            c_name_mean = 'Res_at_'+str(name)
            c_name_std = 'R_std_'+str(name)
            
            if n_rep == 1:
                test_cen_mean = pd.DataFrame({c_name_mean : test_cen_mean})
                df_pro = test_cen_mean
            
            else:
                 test_cen_mean = pd.DataFrame({c_name_mean : test_cen_mean})
                 test_cen_std = pd.DataFrame({c_name_std : test_cen_std})
                 df_pro = pd.merge(test_cen_mean,test_cen_std, left_index=True, right_index=True)
            
            if count == 0:
                df_save = df_pro
                
            else:
                df_save = df_save.merge(df_pro, left_index=True, right_index=True)
            
            df_save.to_csv(os.path.join(base_path + file_save, Folder_name),  index = False, sep=',')
            count = count + 1
            
    
    all_files = glob.glob(base_path + raw_path_1)   
    
    for i in all_files:

        file_name = str(i)
        Folder_name = os.path.basename(file_name)
        Folder_name = os.path.splitext(Folder_name)[0]
        df = (pd.read_csv(i))
        df_mean = df.filter(like='Res_at')
#        df_std = df.filter(like='std')
        df_medio = df_mean.mean()
        df_standar = df_mean.std()
        df_result =  pd.concat([df_medio, df_standar], axis=1)
        df_result.to_csv(os.path.join(base_path + fig_save, Folder_name+'.csv'),  index = bool, sep=',')
        
#        data = np.array([np.arange(1,len(df)+1)]*len(df_mean.columns)).T    
#        data = (pd.DataFrame(data))
        
        #figsize=(5,5)
        
        df_mean.plot.box()
        plt.grid()
        plt.ylabel('Impedance (Ohm)')
        plt.xlabel('Wave percentage')
        
        plt.xticks(rotation = 20 )
        plt.show()
        plt.savefig(os.path.join(base_path + fig_save, Folder_name+'.svg'), bbox_inches='tight')
        plt.clf()
        plt.cla()
        plt.close() 
      
    
    return None
#%%
if __name__ == '__main__':
    
    raw_path = '/data/Interim/1_Hz_6/*.csv'
    raw_path_1 = '/data/Processed/1_Hz_6/*.csv'
    file_save = '/data/processed/1_Hz_6'
    n_rep = 5
    fig_save = '/reports/figures/Voltaje/1_Hz_6'

    main(raw_path, raw_path_1, file_save, n_rep, fig_save) 