ps -u blitt -o pid,command | grep download | cut -f1 -d ' ' | parallel kill
