#!/bin/sh

#   Coleta em Site Survey
#   Esta versão possui o script nativo wstalist
#localizada na pasta /usr/www/.
#   Sua saída é disposta como tabulações das características
#de cada enlace, de acordo com cada endereço MAC.

macx='00:11:22:33:44:55' # considerar MAC do Nanostation 2 Loco

echo -n > /tmp/`echo $macx | sed s/[:]//g`.txt

var=1
while [ $var -lt 1080 ] ; do 
    /usr/www/wstalist | grep $macx | \ 
    cut -d\| -f5 >> /tmp/`echo $macx | sed s/[:]//g`.txt 
    echo '0' >> /tmp/`echo $macx | sed s/[:]//g`.txt
    sleep 10
    date >> /tmp/`echo $macx | sed s/[:]//g`.txt
    var=$(( $var+1 ))
done

