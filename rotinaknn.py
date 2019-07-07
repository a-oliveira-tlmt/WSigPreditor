import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime as dt
from geopy.distance import geodesic
from sklearn import neighbors
from sklearn.metrics import mean_squared_error, r2_score

def geodist(x,y):
    return geodesic(x,y).m

dftorre = pd.read_csv('data/torre.csv',header=None,sep='|')
torre = (dftorre[1][0],dftorre[2][0]) 
tdf = pd.read_csv('data/treinarssi.csv',sep='|')
vdf = pd.read_csv('data/validarssi.csv',sep='|')

tlist=[]
for val in range(0,len(tdf)):
    tlist.append([tdf['Lat'][val],tdf['Long'][val]])

coordlist=np.asarray(tlist)
siglist=np.asarray(tdf['SinaldBm'])

prevsinal = []
erroabs = []
errorel = []
k = 6
knn=neighbors.KNeighborsRegressor(k, weights='uniform', metric=geodist)
yf = knn.fit(coordlist, siglist)
prevsinal=[]
for val in range(0,len(vdf)):
    pred = yf.predict([[vdf['Lat'][val],vdf['Long'][val]]])
    prevsinal.append(pred[0])
    erroabs.append(abs( pred[0] - vdf['SinaldBm'][val]))
    errorel.append((pred[0]-vdf['SinaldBm'][val])/vdf['SinaldBm'][val])

print("Erro medio quadratico: %.2f"
      % mean_squared_error(vdf['SinaldBm'], prevsinal))
print('Coeficiente de determinacao: %.2f' % r2_score(vdf['SinaldBm'], prevsinal))

n = np.arange(1,1+len(vdf))
plt.clf()
plt.cla()
larg=.25
fig = plt.figure()
ax=fig.add_subplot(111)
plt1 = ax.bar(n,prevsinal,larg,color='blue')
plt2 = ax.bar(n+larg,vdf['SinaldBm'],larg,color='red')
ax.set_ylabel('Intensidade (dBm)')
ax.set_title('Comparação entre Intensidades Medidas e Estimadas')
ax.set_xticks(n + larg / 2)
ax.set_xticklabels( vdf['ID'] )
legg=ax.legend( (plt1[0], plt2[0]), ('Estimado', 'Medido'), bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0. )
legg.get_frame().set_edgecolor('black')
plt.tight_layout()
figname = 'imag/prevXmed.png'
plt.savefig(figname)

plt.clf()
plt.cla()
larg=.35
fig = plt.figure()
ax1=fig.add_subplot(111)
ax2=ax1.twinx()
plt1 = ax1.bar(n,erroabs,larg,color='gray')
plt2 = ax2.bar(n+larg,100*abs(np.array(errorel)),larg,color='black')
ax1.set_ylabel('Erro absoluto de Predição (dBm)')
ax2.set_ylabel('Erro relativo de Predição (%)')
ax1.set_title('Erros de Predição relacionados à coleta')
ax1.set_xticks(n+larg/2)
ax1.set_xticklabels( vdf['ID'] )
legg=ax1.legend( (plt1[0], plt2[0]), ('Erro Absoluto', 'Erro Relativo'), bbox_to_anchor=(1.1, 0.95), loc='upper left', borderaxespad=0. )
legg.get_frame().set_edgecolor('black')
plt.tight_layout()
figname = 'imag/erroabsrel.png'
plt.savefig(figname)



