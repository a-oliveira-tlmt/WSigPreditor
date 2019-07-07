import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from geopy.distance import geodesic

vdf = pd.read_csv('data/validarssi.csv',sep='|')
# ['C-1','C-5','C-9','C-13','P-1','P-7','P-13', 'P-19', 'P-25']

p=[]

p.append(np.asarray([-59.69140765677986, -56.516084203922404, -60.8475211291977, -58.10550201508295, -68.51515188912833, -69.9271541093655, -73.403627270096, -74.40561322424037, -76.67510663606001])) # Okumura

p.append(np.asarray([-61.740941176859906, -64.8493897320591, -68.89984304824652, -64.85241513584312, -95.0, -73.7885113113415, -83.12932258678755, -93.04146662750692, -95.0])) # RNN

p.append(np.asarray([-76.23383275117311, -73.05850929831566, -77.38994622359095, -74.6479271094762, -85.05757698352159, -86.46957920375876, -89.94605236448925, -90.94803831863362, -93.21753173045326])) # Perdas no Espaço Livre

#p.append(np.asarray([-3.8, -10.5, -14.4, -14.2, -17.8, -11.1, -16.5, -13.8, -14.4])) # Radio Mobile

p.append(np.asarray([-73.78372428, -75.070075, -78.34414755, -78.39054664, -81.21814991, -75.75265988, -78.69127141, -78.56665469, -77.97656578])) # Regressão Linear

#leg = ["Okumura","RNN","Espaço Livre","Radio Mobile","Regressão Linear"]
leg = ["Okumura","RNN","Espaço Livre","Regressão Linear"]

pltt = []
mk=["P","X","d","s","*","o","h","v","^"]
n = np.arange(1,1+len(vdf))
plt.clf()
plt.cla()
larg=.25
fig = plt.figure()
ax=fig.add_subplot(111)
ax.set_ylabel('Intensidade (dBm)')
#ax.set_ylim(-100.0,5.0)
ax.set_title('Comparação entre Métodos de Predição')
ax.set_xticks(n)
ax.set_xticklabels( vdf['ID'] )
for k in range(0,len(p)):
    pltt.append(ax.scatter(n,p[k],marker=mk[k]))

pltt.append(ax.scatter(n,vdf['SinaldBm'],color='black',marker="D"))
leg.append('Medido')
legg=plt.legend(pltt, leg, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0. )
legg.get_frame().set_edgecolor('black')
plt.tight_layout()
figname = 'imag/comparaprev.png'
plt.savefig(figname)
plt.close()

pltt = []
erroquad = []
#leg = ["Okumura","RNN","Espaço Livre","Radio Mobile","Regressão Linear"]
leg = ["Okumura","RNN","Espaço Livre","Regressão Linear"]
n = np.arange(1,1+len(p))
plt.clf()
plt.cla()
fig = plt.figure()
ax=fig.add_subplot(111)
ax.set_ylabel('Erro quadrático médio de predição por tipo (dBm)')
ax.set_title('Erros quadráticos médios de diferentes métodos de predição')
ax.set_xticks(n)
ax.set_xticklabels( leg )
for k in range(0,len(p)):
    erroquad.append(np.sqrt(np.sum( (np.array(p[k]-vdf['SinaldBm']))**2 ) / len(vdf['SinaldBm'])))
    
ax.bar(n,erroquad,color='gray')
plt.tight_layout()
figname = 'imag/comparaquad.png'
plt.savefig(figname)
plt.close()

pltt = []
#leg = ["Okumura","RNN","Espaço Livre","Radio Mobile","Regressão Linear"]
leg = ["Okumura","RNN","Espaço Livre","Regressão Linear"]
n = np.arange(1,1+len(vdf))
plt.clf()
plt.cla()
fig = plt.figure()
ax=fig.add_subplot(111)
ax.set_ylabel('Erro absoluto das predições por tipo (dBm)')
ax.set_title('Erros absolutos de diferentes métodos de predição ')
ax.set_xticks(n)
ax.set_xticklabels( vdf['ID'] )
for k in range(0,len(p)):
    erroabs = abs(np.array(p[k]-vdf['SinaldBm']))
    pltt.append(ax.scatter(n,erroabs,marker=mk[k]))
    
legg=plt.legend(pltt, leg, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0. )
legg.get_frame().set_edgecolor('black')
plt.tight_layout()
figname = 'imag/comparaabs.png'
plt.savefig(figname)
plt.close()

pltt = []
#leg = ["Okumura","RNN","Espaço Livre","Radio Mobile","Regressão Linear"]
leg = ["Okumura","RNN","Espaço Livre","Regressão Linear"]
n = np.arange(1,1+len(vdf))
plt.clf()
plt.cla()
fig = plt.figure()
ax=fig.add_subplot(111)
ax.set_ylabel('Erro relativo das predições por tipo (%)')
ax.set_title('Erros relativos de diferentes métodos de predição')
ax.set_xticks(n)
ax.set_xticklabels( vdf['ID'] )
for k in range(0,len(p)):
    errorel = 100*abs(np.array((p[k]-vdf['SinaldBm'])/(vdf['SinaldBm'])))
    pltt.append(ax.scatter(n,errorel,marker=mk[k]))

legg=plt.legend(pltt, leg, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0. )
legg.get_frame().set_edgecolor('black')
plt.tight_layout()
figname = 'imag/compararel.png'
plt.savefig(figname)
plt.close()



