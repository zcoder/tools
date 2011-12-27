cat -n | sort -k 2 | uniq -f 1 | sort -k 1,1 -n | cut -b 8-
