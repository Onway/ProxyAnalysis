#!/bin/bash

echo "Installing ProxyAnalysis..."

insdir=/opt/ProxyAnalysis
[ ! -d ${insdir} ] && mkdir ${insdir}
cp -u * ${insdir}
cp -u "${insdir}/ProxyAnalysis" /etc/init.d

vardir="${insdir}/var"
if [ ! -d ${vardir} ] ; then
    mkdir $vardir
    chown -R nobody:nogroup $vardir
fi

echo "done!"
