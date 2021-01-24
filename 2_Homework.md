# 1. AWK
### 1.1 What is the most frequent browser (user agent)?
```bash
[root@localhost shared-folder]# sudo sudo awk -F"\"" '{print $6}' access.log | awk ' {print $1}' | awk '{if (max < ++c[$1]) {max = c[$1]; browser = $1}} END {print browser, max}'
Mozilla/4.0 43666
```
### 1.2 Show number of requests per month for ip 95.108.129.196 (for example: Sep 2016 - 100500 reqs, Oct 2016 - 0 reqs, Nov 2016 - 2 reqs...)
```bash
grep 193.106.31.130 access.log | awk -F[:\ ] '{print $4}' | awk -F[/] '{print $2, $1}' | awk -F' ' '{print $1, "- " $2 " reqs"}'| awk -F, '$1 {/Jan/ a[$2]++; /Dec/ b[$2]++; /Feb/ c[$2]++ }END{ for (i in a) print i,a[i], b[i], c[i]}'
```
### 1.3 Show total amount of data which server has provided for each unique ip (i.e. 100500 bytes for 1.2.3.4; 9001 bytes for 5.4.3.2 and so on)
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
# 2. SED
### 2.1 Change all user agents to "lynx"
```bash
[root@localhost shared-folder]# sed 's/["]*[("| )][Mozilla|Mobile Safari|AppleWebKit|Chrome]*[(^/)]/lynx/2pg' access.log | head -5
13.66.139.0 - - [19/Dec/2020:13:57:26 +0100] "GET /index.php?option=com_phocagallery&view=category&id=1:almhuette-raith&Itemid=53 HTTP/1.1" 200 32653 "-" lynx5.0lynxcompatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)" "-"
13.66.139.0 - - [19/Dec/2020:13:57:26 +0100] "GET /index.php?option=com_phocagallery&view=category&id=1:almhuette-raith&Itemid=53 HTTP/1.1" 200 32653 "-" lynx5.0lynxcompatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)" "-"
157.48.153.185 - - [19/Dec/2020:14:08:06 +0100] "GET /apache-log/access.log HTTP/1.1" 200 233 "-" lynx5.0lynxWindows NT 6.3; Win64; x64lynx537.36lynxKHTML, like Geckolynx87.0.4280.88lynx537.36" "-"
157.48.153.185 - - [19/Dec/2020:14:08:06 +0100] "GET /apache-log/access.log HTTP/1.1" 200 233 "-" lynx5.0lynxWindows NT 6.3; Win64; x64lynx537.36lynxKHTML, like Geckolynx87.0.4280.88lynx537.36" "-"
157.48.153.185 - - [19/Dec/2020:14:08:08 +0100] "GET /favicon.ico HTTP/1.1" 404 217 "http://www.almhuette-raith.at/apache-log/access.log" lynx5.0lynxWindows NT 6.3; Win64; x64lynx537.36lynxKHTML, like Geckolynx87.0.4280.88lynx537.36" "-"
```
### 2.2 Masquerade all ip addresses. For example, 1.2.3.4 becomes "ip1", 3.4.5.6 becomse "ip2" and so on. Rewrite file.
```bash
[root@localhost shared-folder]# sed -e '=' -e 's/[[:digit:]]\{1,3\}\.[[:digit:]]\{1,3\}\.[[:digit:]]\{1,3\}\.[[:digit:]]\{1,3\}\ -//g' access.log | sed '/^[0-9]/ s/^/ip/'
ip1
 - [19/Dec/2020:13:57:26 +0100] "GET /index.php?option=com_phocagallery&view=category&id=1:almhuette-raith&Itemid=53 HTTP/1.1" 200 32653 "-" "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)" "-"
ip2
 - [19/Dec/2020:14:08:06 +0100] "GET /apache-log/access.log HTTP/1.1" 200 233 "-" "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" "-"
ip3
 - [19/Dec/2020:14:08:08 +0100] "GET /favicon.ico HTTP/1.1" 404 217 "http://www.almhuette-raith.at/apache-log/access.log" "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" "-"
ip4
 - [19/Dec/2020:14:14:26 +0100] "GET /robots.txt HTTP/1.1" 200 304 "-" "Mozilla/5.0 (compatible; DotBot/1.1; http://www.opensiteexplorer.org/dotbot, help@moz.com)" "-"
ip5
 - [19/Dec/2020:14:16:44 +0100] "GET /index.php?option=com_phocagallery&view=category&id=2%3Awinterfotos&Itemid=53 HTTP/1.1" 200 30662 "-" "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)" "-"

```
