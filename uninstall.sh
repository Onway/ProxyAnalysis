#!/bin/bash

echo "Uninstalling ProxyAnalysis..."

[ -f /etc/init.d/ProxyAnalysis ] && /etc/init.d/ProxyAnalysis stop
rm -f /etc/init.d/ProxyAnalysis
rm -rf /opt/ProxyAnalysis

echo "done!"
