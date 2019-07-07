import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from geopy.distance import geodesic
dftorre = pd.read_csv('data/torre.csv',header=None,sep='|')
torre = (dftorre[1][0],dftorre[2][0]) 
tdf = pd.read_csv('data/treinarssi.csv',sep='|')
vdf = pd.read_csv('data/validarssi.csv',sep='|')
dlist=[]
tlist=[]
for val in range(0,len(tdf)):
    tlist.append([tdf['Lat'][val],tdf['Long'][val]])
    dlist.append(geodesic([tdf['Lat'][val],tdf['Long'][val]],torre).m)

coordlist=np.asarray(tlist)
siglist=np.asarray(tdf['SinaldBm'])
hte=20
hre=10
f=2.4e+009
c=3e+008
wvlen = c/f

Pt=0.7943
Gt=25
Gr=25

Ghte = 20*np.log10(hte/200)

if(hre>3):
    Ghre = 20*np.log10(hre/3)
else:
    Ghre = 10*np.log10(hre/3)


Lf = [] # Modelo de Espaço Livre
for val in range(0,len(vdf)):
    Lf.append(10*np.log10( (wvlen / (4*np.pi*dlist[val]))**2 ) )

Lr = [] # Modelo de 2 Raios
for val in range(0,len(vdf)):
    Lr.append(10*np.log10( ( (hte * hre) / (dlist[val]**2) )**2 ) + 10*np.log10(Pt*Gt*Gr))

Amu = 20
Garea = 13
Pt=0.7943
prevsinal = []
for val in range(0,len(vdf)):
    prevsinal.append(Lf[val]+Amu-Ghre-Ghte-Garea)

erroabs = abs( prevsinal - vdf['SinaldBm'])
errorel = abs((prevsinal-vdf['SinaldBm'])/vdf['SinaldBm'])

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
figname = 'imag/okumprevXmed.png'
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
figname = 'imag/okumerroabsrel.png'
plt.savefig(figname)
plt.close()



