import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime as dt
from geopy.distance import geodesic
from sklearn import neighbors
from sklearn.metrics import mean_squared_error, r2_score

def geodist(x,y):
    return geodesic(x,y).m

tdf = pd.read_csv('data/treinarssi.csv',sep='|')
vdf = pd.read_csv('data/validarssi.csv',sep='|')

raios=np.arange(175,501,75)

tlist=[]
for val in range(0,len(tdf)):
    tlist.append([tdf['Lat'][val],tdf['Long'][val]])

coordlist=np.asarray(tlist)
siglist=np.asarray(tdf['SinaldBm'])

p=[]
a=[]
r=[]

for d in raios:
    prevsinal = []
    erroabs = []
    errorel = []
    rnn=neighbors.RadiusNeighborsRegressor(radius=d, weights='distance', metric=geodist)
    yf = rnn.fit(coordlist, siglist)
    prevsinal=[]
    for val in range(0,len(vdf)):
        pred = yf.predict([[vdf['Lat'][val],vdf['Long'][val]]])
        prevsinal.append(pred[0])
        erroabs.append(abs( pred[0] - vdf['SinaldBm'][val]))
        errorel.append((pred[0]-vdf['SinaldBm'][val])/vdf['SinaldBm'][val])
    p.append(prevsinal)
    a.append(erroabs)
    r.append(errorel)
    print("Erro mádio quadrático de d=" + str(d) + ": %.2f"
          % mean_squared_error(vdf['SinaldBm'], prevsinal))
    print('Escore de Variância: %.2f' % r2_score(vdf['SinaldBm'], prevsinal))
    print(prevsinal)


#print("Prev.Sinal:")
#print(prevsinal)
#print("Erro Absoluto:")
#print(erroabs)
#print("Erro Relativo:")
#print(errorel)

pltt = []
leg = []
mk=["P","X","d","s","*","o","h","v","^"]
n = np.arange(1,1+len(vdf))
plt.clf()
plt.cla()
larg=.25
fig = plt.figure()
ax=fig.add_subplot(111)
ax.set_ylabel('Intensidade (dBm)')
ax.set_title('Comparação de predição entre raios limite R')
ax.set_xticks(n + larg / 2)
ax.set_xticklabels( vdf['ID'] )
for k in range(0,len(p)):
    prevsinal = p[k]
    pltt.append(ax.scatter(n,prevsinal,marker=mk[k]))
    leg.append('R = ' + str(raios[k]) + " m")

pltt.append(ax.scatter(n,vdf['SinaldBm'],color='black',marker="D"))
leg.append('Medido')

legg=plt.legend(pltt, leg, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0. )
legg.get_frame().set_edgecolor('black')
plt.tight_layout()
figname = 'imag/rnncrossdistprev.png'
plt.savefig(figname)
plt.close()

pltt = []
leg = []
n = np.arange(1,1+len(vdf))
plt.clf()
plt.cla()
fig = plt.figure()
ax=fig.add_subplot(111)
#ax.set_ylim(-2.0,30.0)
ax.set_ylabel('Erro absoluto de predição (dBm)')
ax.set_title('Erros absolutos de predição pelo raio limite R')
ax.set_xticks(n)
ax.set_xticklabels( vdf['ID'] )
for k in range(0,len(a)):
    erroabs = abs(np.array(a[k]))
    pltt.append(ax.scatter(n,erroabs,marker=mk[k]))
    leg.append('R = ' + str(raios[k]) + " m")

legg=plt.legend(pltt, leg, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0. )
legg.get_frame().set_edgecolor('black')
plt.tight_layout()
figname = 'imag/rnncrossdistabs.png'
plt.savefig(figname)
plt.close()

pltt = []
leg = []
n = np.arange(1,1+len(vdf))
plt.clf()
plt.cla()
fig = plt.figure()
ax=fig.add_subplot(111)
ax.set_ylabel('Erro relativo de predição (%)')
ax.set_title('Erros relativos de predição pelo raio limite R')
ax.set_xticks(n)
ax.set_xticklabels( vdf['ID'] )
for k in range(0,len(r)):
    errorel = 100*abs(np.array(r[k]))
    pltt.append(ax.scatter(n,errorel,marker=mk[k]))
    leg.append('R = ' + str(raios[k]) + " m")

legg=plt.legend(pltt, leg, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0. )
legg.get_frame().set_edgecolor('black')
plt.tight_layout()
figname = 'imag/rnncrossdistrel.png'
plt.savefig(figname)
plt.close()

