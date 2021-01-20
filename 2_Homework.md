# AWK
### 1. What is the most frequent browser (user agent)?
```bash
[root@localhost shared-folder]# sudo awk -F"\"" '{print $6}' access.log | sort | uniq -dc | sort -n | tail -1
  43172 Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)
```
### 2. Show number of requests per month for ip 95.108.129.196 (for example: Sep 2016 - 100500 reqs, Oct 2016 - 0 reqs, Nov 2016 - 2 reqs...)
```bash
[root@localhost shared-folder]# awk -F[:\ ] '{print $4}' access.log | sort | uniq -c | sort -nr | awk '{print $2,$1}'
[28/Dec/2020 7478
[25/Dec/2020 5644
[18/Jan/2021 4988
[11/Jan/2021 4283
[08/Jan/2021 4056
[21/Dec/2020 3982
[23/Dec/2020 3856
[20/Dec/2020 3698
[22/Dec/2020 3645
[24/Dec/2020 3607
[07/Jan/2021 3098
[29/Dec/2020 2919
[09/Jan/2021 2805
[04/Jan/2021 2788
[17/Jan/2021 2498
[13/Jan/2021 2475
[30/Dec/2020 2389
[06/Jan/2021 2386
[03/Jan/2021 2379
[16/Jan/2021 2328
[10/Jan/2021 2313
[19/Jan/2021 2302
[12/Jan/2021 2300
[26/Dec/2020 2269
[15/Jan/2021 2227
[27/Dec/2020 2181
[01/Jan/2021 2165
[31/Dec/2020 2067
[05/Jan/2021 2017
[14/Jan/2021 1954
[02/Jan/2021 1942
[20/Jan/2021 1896
[19/Dec/2020 1135
```
