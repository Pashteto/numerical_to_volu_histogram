from tkinter import *
 
import numpy as np
import time
import os
import pandas as pd

import matplotlib.pyplot as plt



def display_full_name():
    tym = time.localtime() 
    opt = time.strftime("%Y_%m_%d_%H_%M_%S",tym) 
    folder=os.getcwd()
    
    filenaLL=folder +'\\Results_'+opt+'.txt'
    now="Distrib_"+opt+".png"
    
    
    print("File input.csv opened\n")
    Data50k = pd.read_csv('input.csv')
    print(Data50k.describe())
    
    plotbins=name.get()
    
    #norm_th=[1,3,4,7,12,4,234,234,4,5,5,5,6,6]
    
    first_column = Data50k.iloc[:, 0]
    norm_th=first_column.tolist()
    we_list = norm_th[:]
    for we in range(len(we_list)):
        we_list[we]=norm_th[we]**3
    	
    
    a_heights, a_bins = np.histogram(norm_th, bins=plotbins)
    v_heights, v_bins = np.histogram(norm_th, bins=plotbins,weights=we_list)
    
    a_heightsd=a_heights/len(norm_th)
    v_heightsd=v_heights/sum(v_heights)
    
    print("a_heights\n",a_heights,"\na_bins\n", a_bins)
    with open(filenaLL, 'a') as file:
        file.write("Bins boundaries:\n")
        for item in a_bins:
            file.writelines(str(item) +'\t')

    xd = list([a_bins[0]])
    ynd = list([0])
    yvd = list([0])
    
    for i in range(len(a_bins)-1):
        xd.append(a_bins[i])
        xd.append(a_bins[i+1])
        xd.append(a_bins[i+1])
        ynd.append(a_heightsd[i])
        ynd.append(a_heightsd[i])
        ynd.append(0)
        yvd.append(v_heightsd[i])
        yvd.append(v_heightsd[i])
        yvd.append(0)
    
    width_a = (a_bins[1] - a_bins[0])/1.0
    
    started,endedd = a_bins[0],a_bins[len(a_bins)-1]
    fuldist=endedd-started
    delta=fuldist/(len(a_bins)-1)
    bins = a_bins[:-1]
    avend=0
    avevd=0
    sumvd=0
    sumnd=0
    
    for i in range(len(bins)):
        bins[i]=started+i*delta+delta*0.5
        avend+=bins[i]*a_heightsd[i]
        avevd+=bins[i]*v_heightsd[i]
        sumnd+=a_heightsd[i]
        sumvd+=v_heightsd[i]
    
    
    avevd=avevd/sumvd
    avend=avend/sumnd
       
    print("Average dia numeric:\t",avend,"Average dia volu:\t",avevd)
    
    
    with open(filenaLL, 'a') as file:
        file.write("\nNumber of spheres in each bin:\n")
        for item in a_heights:
            file.writelines(str(item) +'\t')
        file.write("\nNumeric prob. densities:\n")
        for item in a_heightsd:
            file.writelines(str(item) +'\t')
        file.write("\nVolumic prob. densities:\n")
        for item in v_heightsd:
            file.writelines(str(item) +'\t')
        file.write("\nNumeric prob. densities plot X and Y:\n")
        for item in xd:
            file.writelines(str(item) +'\t')
        file.write("\n")
        for item in ynd:
            file.writelines(str(item) +'\t')
    
        file.write("\nVolumic prob. densities plot X and Y:\n")
        for item in xd:
            file.writelines(str(item) +'\t')
        file.write("\n")
        for item in yvd:
            file.writelines(str(item) +'\t')
        file.write("\nAverage dia numeric:\t")
        file.write(str(avend))
        file.write("\nAverage dia volu:\t")
        file.write(str(avevd))
    
        file.close()
		
    v_heights, v_bins = np.histogram(norm_th, bins=plotbins,weights=we_list,density=True)
    fig, ax = plt.subplots(figsize=(6,4), facecolor='white', dpi= 160)
    ax.grid()
    
    ax.bar(bins, a_heightsd, width=width_a, facecolor='blue',alpha=0.75,label='Количественное распределение')#'cornflowerblue')
    ax.bar(bins, v_heightsd, width=width_a,alpha=0.5, facecolor='red',label='Объемное распределение')#'cornflowerblue')
    
    ax.set_xlabel('Диаметр, мкм')
    ax.set_ylabel('Относительная доля')
    plt.legend(loc='best')
    now="Distrib_"+opt+".png"
    plt.savefig(now)
	
    print("Search for files")
    print(filenaLL)
    print("And:")
    print(now)
	


 
root = Tk()
root.title("Python")
 
name = IntVar()
name_label = Label(text="Разбиений:")
name_label.grid(row=0, column=0, sticky="w")
name_entry = Entry(textvariable=name)
name_entry.grid(row=0,column=1, padx=5, pady=5)
 
# вставка начальных данных
name_entry.insert(0, 1)

message_button = Button(text="calc", command=display_full_name)
message_button.grid(row=2,column=1, padx=5, pady=5, sticky="e")
 
root.mainloop()