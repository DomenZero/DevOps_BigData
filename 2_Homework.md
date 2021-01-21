# AWK
### 1. What is the most frequent browser (user agent)?
```bash
[root@localhost shared-folder]# sudo awk -F"\"" '{print $6}' access.log | sort | uniq -dc | sort -n | tail -1
  43172 Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)
```
### 2. Show number of requests per month for ip 95.108.129.196 (for example: Sep 2016 - 100500 reqs, Oct 2016 - 0 reqs, Nov 2016 - 2 reqs...)
```bash
[root@localhost shared-folder]# grep 193.106.31.130 access.log | awk -F[:\ ] '{print $4}' | sort | uniq -c | sort -nr | awk -F[/] '{print $2, $1}' | awk -F' ' '{print $1, "- " $2 " reqs"}' | uniq -c
      4 Dec - 1757 reqs
     12 Jan - 1757 reqs
      2 Dec - 1506 reqs
      7 Jan - 1506 reqs
      1 Jan - 1255 reqs
      1 Dec - 251 reqs
```
### 3. Show total amount of data which server has provided for each unique ip (i.e. 100500 bytes for 1.2.3.4; 9001 bytes for 5.4.3.2 and so on)
