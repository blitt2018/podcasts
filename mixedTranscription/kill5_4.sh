ps -u blitt -o pid,command | grep 5_4 | cut -f1 -d ' ' | parallel kill
ps -u blitt -o pid,command | grep 5_4 | cut -f2 -d ' ' | parallel kill
ps -u blitt -o pid,command | grep 5_4 | cut -f3 -d ' ' | parallel kill
