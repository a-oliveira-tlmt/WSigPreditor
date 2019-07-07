#!/bin/sh 

# Esta versão possui o script nativo wstalist 
#localizada na pasta /bin/. Ele será o meio de 
#consulta aos dados de rede sem fio. 
# Sua saída é formatada como uma listagem completa 
#das características de cada enlace, de acordo com 
#seu endereço MAC. 

wstalist | grep mac | cut -sd\" -f4 > /tmp/maclist.dat 

for mac in `cat /tmp/maclist.dat` ; do 
   echo -n > /tmp/`echo $mac | sed s/[:]//g`.txt 
done 

var=1 
while [ $var -lt 60 ] ; do 
   for mac in `cat /tmp/maclist.dat`; do 
      wstalist | grep 'mac\|\signal' | sed 'N;s/\n//' | \ 
      sed s/[,]/:/g | sed s/' '//g | grep $mac | \ 
      cut -d\: -f9 >> /tmp/`echo $mac | sed s/[:]//g`.txt 
   done 
   sleep 60 
   var=$(( $var+1 )) 
done
