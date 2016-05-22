#!/bin/bash

echo "Uninstalling ProxyAnalyze..."

[ -f /etc/init.d/ProxyAnalyze ] && /etc/init.d/ProxyAnalyze stop
rm -f /etc/init.d/ProxyAnalyze
rm -rf /opt/ProxyAnalyze

echo "done!"
