#%% crear una grafica para medida
input_ex = [4.16,-4.16,4.16,-4.16]
input_in = [2.16,-2.16,2.16,-2.16]
matplotlib.rc('xtick', labelsize=22) 
matplotlib.rc('ytick', labelsize=22) 
plt.plot(input_ex, marker='d', color='blue',drawstyle='steps-pre', linewidth=10)
plt.plot(input_in, marker='d', color='red',drawstyle='steps-pre', linewidth=10)
plt.axvline(x=1.7, linewidth=10)
plt.title("")
plt.ylabel('Voltage', fontsize= 22)
plt.xlabel("Time",fontsize= 22)

plt.show()
