import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime as dt
from geopy.distance import geodesic
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

def geodist(x,y):
    return geodesic(x,y).m

dftorre = pd.read_csv('data/torre.csv',header=None,sep='|')
torre = (dftorre[1][0],dftorre[2][0]) 

tdf = pd.read_csv('data/treinarssi.csv',sep='|')
vdf = pd.read_csv('data/validarssi.csv',sep='|')

tlist=[]
dtlist=[]
for val in range(0,len(tdf)):
    tlist.append([tdf['Lat'][val],tdf['Long'][val]])
    dtlist.append(geodesic([tdf['Lat'][val],tdf['Long'][val]],torre).m)

dvlist=[]
for val in range(0,len(vdf)):
    dvlist.append(geodesic([vdf['Lat'][val],vdf['Long'][val]],torre).m)

tdlist=np.asarray(dtlist).reshape(-1,1)
vdlist=np.asarray(dvlist).reshape(-1,1)
siglist=np.asarray(tdf['SinaldBm'])

prevsinal = []
erroabs = []
errorel = []
linreg=linear_model.LinearRegression()
yf = linreg.fit(tdlist, siglist)

prevsinal = yf.predict(vdlist)
erroabs = abs( prevsinal - vdf['SinaldBm'])
errorel = abs((prevsinal-vdf['SinaldBm'])/vdf['SinaldBm'])

print("Erro médio quadrático: %.2f"
      % mean_squared_error(vdf['SinaldBm'], prevsinal))
print('Escore de Variância: %.2f' % r2_score(vdf['SinaldBm'], prevsinal))
#print("Prev.Sinal:")
#print(prevsinal)
#print("Erro Absoluto:")
#print(erroabs)
#print("Erro Relativo:")
#print(errorel)

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
ax.legend( (plt1[0], plt2[0]), ('Estimado', 'Medido') )
figname = 'imag/linregprevXmed.png'
plt.savefig(figname)
plt.close()

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
ax1.set_ylim(0.0,95.0)
ax2.set_ylim(0.0,100.0)
ax1.set_title('Erros de Predição relacionados à coleta')
ax1.set_xticks(n+larg/2)
ax1.set_xticklabels( vdf['ID'] )
ax1.legend( (plt1[0], plt2[0]), ('Erro Absoluto', 'Erro Relativo') )
figname = 'imag/linregerroabsrel.png'
plt.savefig(figname)
plt.close()

