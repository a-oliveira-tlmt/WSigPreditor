import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dfmac = pd.read_csv('data/idlist.csv',header=None,sep='|')

validalatlist=[]
treinalatlist=[]

validalonglist=[]
treinalonglist=[]

validalist = ['C-1','C-5','C-9','C-13','P-1','P-7','P-13', 'P-19', 'P-25']
treinalist=[]

for val in range(0,len(dfmac)):
    if dfmac[0][val] not in validalist:
        treinalist.append(dfmac[0][val])
        treinalatlist.append(dfmac[1][val])
        treinalonglist.append(dfmac[2][val])
    else:
        validalatlist.append(dfmac[1][val])
        validalonglist.append(dfmac[2][val])

validarssilist=[]
treinarssilist=[]

for addr in dfmac[0]:

    df = pd.read_csv('data/'+addr+'.csv',header=None)

    dataNorm = df[0].cumsum().to_numpy()/(1+df[0].index.to_numpy())

    reg = dataNorm[len(dataNorm)-1]

    if addr in treinalist:
        treinarssilist.append(str(reg))
    else:
        validarssilist.append(str(reg))

    print('Para ID ' + addr + ': '+str(reg))
    n = np.arange(1,1+len(df[0]))
    plt.clf()
    plt.cla()
    fig = plt.figure()
    ax=fig.add_subplot(111)
    plt1 = ax.plot(n,dataNorm,label='avsum',color='blue')
    plt2 = ax.plot(n,df[0],label='medido',color='orange')
    ax.set_ylabel('Intensidade (dBm)')
    ax.set_xlabel('Medidas')
    ax.set_title('Comparação entre as Medidas e suas Médias Acumuladas')
    ax.legend( (plt1[0], plt2[0]), ('Média acumulada', 'Medidas') )
    figname = 'imag/'+addr+'_av.png'
    plt.savefig(figname)
    plt.close()

treinadct = {}
treinadct['ID'] = treinalist
treinadct['SinaldBm'] = treinarssilist
treinadct['Lat'] = treinalatlist
treinadct['Long'] = treinalonglist

validadct = {}
validadct['ID'] = validalist
validadct['SinaldBm'] = validarssilist
validadct['Lat'] = validalatlist
validadct['Long'] = validalonglist

treinadf = pd.DataFrame(treinadct)
treinadf.to_csv('data/treinarssi.csv',index=False,sep='|')

validadf = pd.DataFrame(validadct)
validadf.to_csv('data/validarssi.csv',index=False,sep='|')

