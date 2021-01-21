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
```bash
[root@localhost shared-folder]# awk '{ sum_byte[$1] += $10 } END { for (ip in sum_byte) { print ip, sum_byte[ip]} }' access.log
23.94.20.157 41916
95.91.42.30 1654080
62.28.204.42 14231169
1.65.209.180 10053208
156.220.58.189 8907704
173.44.165.202 41864
81.16.140.72 1617259
173.252.107.11 524288
80.122.6.67 1366942
51.81.71.215 10439
....
```
