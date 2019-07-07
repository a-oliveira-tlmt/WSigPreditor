#!/bin/sh 

# Coleta na Ubiquiti Nanostation 2
# Esta versão possui o script nativo wstalist 
#localizada na pasta /usr/www/. Ele será o meio de 
#consulta aos dados de rede sem fio. 
# Sua saída é disposta na forma de tabulações das características 
#de cada enlace, de acordo com cada endereço MAC.

/usr/www/wstalist | grep -v `: ` | cut -sd\| -f1 > \ 
/tmp/maclist.dat 

for mac in `cat /tmp/maclist.dat` ; do 
   echo -n > /tmp/`echo $mac | sed s/[:]//g`.txt 
done 

var=1 
while [ $var -lt 60 ] ; do 
   for mac in `cat /tmp/maclist.dat`; do 
      /usr/www/wstalist | grep $mac | cut -d\| -f5 >> \ 
      /tmp/`echo $mac | sed s/[:]//g`.txt 
   done 
   sleep 60 
   var=$(( $var+1 )) 
done
