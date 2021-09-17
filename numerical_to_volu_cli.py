import numpy as np
import time
import os
import pandas as pd

tym = time.localtime() 
opt = time.strftime("%Y_%m_%d_%H_%M_%S",tym) 
folder=os.getcwd()

filenaLL=folder +'\\Results_'+opt+'.txt'
now="Distrib_"+opt+".png"


print("File input.csv opened\n")
Data50k = pd.read_csv('input.csv')
print(Data50k.describe())
print("File input.csv opened\nInput bins num( n > 0 ):\n")

plotbins=int(input(''))

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
    file.write("\nBins boundaries:\n")
    for item in a_bins:
        file.writelines(str(item) +'\t')
	
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

print("Search for files")
print(filenaLL)
#print("And")
#print(now)

plotbins=int(input(''))