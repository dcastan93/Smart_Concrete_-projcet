import sqlite3

import datetime as dt
import pandas as pd
#import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats # importando scipy.stats
import numpy as np

#%%
dataset_centro_1hz = pd.read_csv('50seg_2.2kohm_centro_1hz.csv')
#dataset_centro_10hz = pd.read_csv('50seg_2,2kohm_centro_10hz.csv')
dataset_extremo_1hz = pd.read_csv('50seg_2.2kohm_extremo_1hz.csv')
#dataset_extremo_10hz= pd.read_csv('50seg_2,2kohm_extremo_10hz.csv')
dataset_centro_1hz['Tiempo'] = dataset_centro_1hz[dataset_centro_1hz.columns[[3]]]
dataset_extremo_1hz['Tiempo'] = dataset_extremo_1hz[dataset_extremo_1hz.columns[[3]]]
dataset_centro_1hz['Voltaje'] = dataset_centro_1hz[dataset_centro_1hz.columns[[4]]]
dataset_extremo_1hz['Voltaje'] = dataset_extremo_1hz[dataset_extremo_1hz.columns[[4]]]
dataset_centro_1hz= dataset_centro_1hz[dataset_centro_1hz.columns[[6,7]]]
dataset_extremo_1hz= dataset_extremo_1hz[dataset_extremo_1hz.columns[[6,7]]]

#%% para sacar la resistencia

dataset_centro_1hz=dataset_centro_1hz[dataset_centro_1hz[['Voltaje']]>0].reset_index(drop = True)
dataset_centro_1hz=dataset_centro_1hz[['Voltaje']]
dataset_centro_1hz=dataset_centro_1hz.dropna(how='all',axis=0).reset_index(drop=True)


dataset_extremo_1hz=dataset_extremo_1hz[dataset_extremo_1hz[['Voltaje']]>0].reset_index(drop = True)
dataset_extremo_1hz=dataset_extremo_1hz[['Voltaje']]
dataset_extremo_1hz=dataset_extremo_1hz.dropna(how='all',axis=0).reset_index(drop=True)

#%% valor de los datos
perc = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
#perc = int(perc*25)
#%% se sacan los valores para dataset extremo
count=0
test_extremo = []


while count<= 7:
    count_extremo = 0
    
    for i_extremo in range(1,40):
        
        t = int(perc[count]*25)
        n_extremo = t + 25*count_extremo
        data_extremo = dataset_extremo_1hz.iloc[n_extremo]
        count_extremo = count_extremo + 1
        test_extremo.append(data_extremo)

    count=count+1
    
df_extremo = pd.DataFrame(test_extremo)

#%%se sacan los valores para centro
count_1 = 0
test_centro = []

while count_1<= 7:
    count_centro = 0

    for i_centro in range(1,40):
        
        c = int(perc[count_1]*25)
        n_centro = c + 25*count_centro
        data_centro = dataset_centro_1hz.iloc[n_centro]
        count_centro = count_centro + 1
        test_centro.append(data_centro)
                
    count_1=count_1+1
df_centro = pd.DataFrame(test_centro)

#%%encontrar la resistencia
Corriente = df_extremo/(2200)
Resistencia = df_centro/Corriente
ciclos = list(range(1,313))
ciclos = pd.DataFrame(ciclos)

#%%
count_0 = 0
count_1 = 39
res_22_1hz_mean = []
res_22_1hz_std = []
for i in range (1,9):
    
    Res = Resistencia[count_0 : count_1]
    I_22_1hz_mean = Res.mean()
    I_22_1hz_std = Res.std()
    res_22_1hz_mean.append(I_22_1hz_mean)
    res_22_1hz_std.append(I_22_1hz_std)
    count_0 = count_1
    count_1=count_1 + 39
    
res_22_1hz_mean = pd.DataFrame(res_22_1hz_mean)
res_22_1hz_std = pd.DataFrame(res_22_1hz_std)

res_22_1hz_mean.to_csv('res_22_05_mean.csv')
res_22_1hz_std.to_csv('res_22_05_std.csv')


#%%grafica de resistencia

fig, ax = plt.subplots()
matplotlib.rc('axes', titlesize=20)

matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20) 
ax.plot(ciclos, Resistencia, color='green')

ax.set(xlabel='ciclo', ylabel='Resistencia (Ohm)')
ax.grid()

x = ciclos.values
x = np.delete(x,[1,2],axis=1) 
x = x.ravel()
y = Resistencia.values
y = np.delete(y,[1,2],axis=1) 
y = y.ravel()
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x,p(x),"r--")

#fig.savefig("Resistencia_1hz.eps")
plt.show()


#%% para sacar la grafica
import matplotlib.pyplot as plt

y = df_02_22_mean

x = [1,2,3,4,5,6,7,8]
x = pd.DataFrame(x)
x = x.values 

#x = x.transpose()
e = df_02_22_std

fig, ax = plt.subplots()


fig.suptitle('test title', fontsize=20)
plt.xlabel('xlabel', fontsize=18)
plt.ylabel('ylabel', fontsize=16)
matplotlib.rc('axes', titlesize=20)

matplotlib.rc('xtick', labelsize=20) 
matplotlib.rc('ytick', labelsize=20) 
ax.set(xlabel='Sample', ylabel='Resistence (Ohm)', )
ax.grid()
fig.canvas.draw()

labels = [1,2,3,4,5,6,7,8,9]
labels[1] = '0.2'
labels[2] = '0.3'
labels[3] = '0.4'
labels[4] = '0.5'
labels[5] = '0.6'
labels[6] = '0.7'
labels[7] = '0.8'

ax.set_xticklabels(labels)
ax.errorbar(x, df_02_22_mean, yerr=df_02_22_std, fmt='o', marker='s', mfc='red',
         mec='green', ms=20, mew=4, ecolor='orangered',
            color='steelblue', capsize=2)
ax.set_title('')


# error bar values w/ different -/+ errors that
# also vary with the x-position

plt.show()

#%%

