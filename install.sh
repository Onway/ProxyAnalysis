#!/bin/bash

echo "Installing ProxyAnalyze..."

insdir=/opt/ProxyAnalyze
[ ! -d ${insdir} ] && mkdir ${insdir}
cp -u * ${insdir}
cp -u "${insdir}/ProxyAnalyze" /etc/init.d

vardir="${insdir}/var"
if [ ! -d ${vardir} ] ; then
    mkdir $vardir
    chown -R nobody:nogroup $vardir
fi

echo "done!"
