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
from matplotlib.patches import Rectangle
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
def main( raw_path_1, fig_save, Filter):
            
    
    all_files = glob.glob(base_path + raw_path_1)   
    
    for i in all_files:
        
        file_name = str(i)
        Folder_name = os.path.basename(file_name)
        Folder_name = os.path.splitext(Folder_name)[0]
        column_name = 'Res_at_'+str(Filter)
        df = (pd.read_csv(i))
        df_mean = df.filter(like = str(Filter))
        column_name = 'Res_at_'+str(Filter)
        df_mean = df_mean[column_name]

        
        df_medio = df_mean.mean()
        df_medio = round(df_medio, 2)
        
        df_std = df_mean.std()
        df_std = round(df_std, 2)
        text_1= 'Valor medio = ' + str(df_medio) + ' Ohm'
        text_2= 'Desviación estandar = ' + str(df_std)+ ' Ohm'
    
        data = np.array([np.arange(1,len(df)+1)]).T    
#        data = (pd.DataFrame(data))
        data = data.ravel()
        z = np.polyfit(data, df_mean, 1)
        p = np.poly1d(z)
        
        #figsize=(5,5)
        
        plt.plot(data, df_mean, color='steelblue')
        plt.plot(data,p(data),"r--")
        plt.grid()
        plt.xlabel('tiempo (s)')
        plt.ylabel('Impedancia (Ohm)')
#        plt.text(8, 8, str(text_1) , fontsize=11)
#        plt.text(0.5, 0.85, str(text_2) , fontsize=11)
        extra = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
        plt.legend([extra, extra], (text_1,text_2 ))
        plt.show()
        plt.savefig(os.path.join(base_path + fig_save, Folder_name+'.pdf'), bbox_inches='tight')
        plt.clf()
        plt.cla()
        plt.close()
    
    return None
#%%
if __name__ == '__main__':
    
    raw_path_1 = '/data/Processed/1_Hz_6/*.csv'
 
    fig_save = '/reports/figures/Voltaje_selected/1_Hz_6'
    Filter = 0.6

    main(raw_path_1, fig_save, Filter) 