# 1. С помощью утилиты  enp0s3 (или тому, который является "основным" для вашей машины):
   1.1 IP Адрес должен быть назначен из пула немаршрутизируемых в Интернете пулов (aka серых IP)
   1.2 Адрес НЕ должен принадлежать пулу адресов, который уже назначен какому-либо из интерфейсов
   1.3 В подсети нового адреса должно быть как можно меньше адресов (broadcast и network адрес назначать интерфейсу нельзя)
   1.4 перезагрузите машину, убедитесь что оба интерфейса имеет оба адреса (вы должны мочь подключиться по ssh к новому ip адресу с виртаульной машины)
   
```bash
[root@localhost ~]# nmcli con add type ethernet con-name new_ip ifname eth0 ip4 172.16.0.7/24 gw4 172.16.0.1
[root@localhost ~]# nmcli con mod new_ip +ipv4.addresses 192.168.0.104/24 gw4 192.168.0.1

[root@localhost ~]# nmcli con up new_ip
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/9)
[root@localhost ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:38:01:00 brd ff:ff:ff:ff:ff:ff
    inet 172.16.0.7/24 brd 172.16.0.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet 192.168.0.104/24 brd 192.168.0.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::74cd:fb13:269f:d9dd/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
```
*Серверный конфиг

```vim
[root@localhost ~]# cat  /etc/sysconfig/network-scripts/ifcfg-eth0
TYPE=Ethernet
DHCP=no
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=eth0
UUID=75534b43-6a4f-49fe-bc95-1ed63ef5306c
DEVICE=eth0:0
ONBOOT=yes
IPADDR0=192.168.0.104
NETMASK0=255.255.255.0
GATEWAY0=192.168.0.1
DNS1=192.168.0.1
DNS2=172.16.0.1
PREFIX=24
IPADDR1=172.16.0.7
PREFIX1=24
GATEWAY1=172.16.0.1
NETMASK1=255.255.255.0
```
*Клиентский конфиг

```vim
[root@crabNebula ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth0
TYPE=Ethernet
DHCP=no
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=dhcp
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=eth0
UUID=80475bdc-27c5-46ee-bba6-e98366978c17
DEVICE=eth0
ONBOOT=yes
IPADDR=172.16.0.9
GATEWAY=172.16.0.1
NETMASK=255.255.255.0
PREFIX=24
DNS=172.16.0.1
```

*Тестирование ssh с клиента

```bash
[root@crabNebula ~]# ssh root@172.16.0.9
The authenticity of host '172.16.0.9 (172.16.0.9)' can't be established.
ECDSA key fingerprint is SHA256:Cz95uiFz5oCo2KGUN0gLI89RWX8V/7wnenNDidTuxwI.
ECDSA key fingerprint is MD5:8c:ff:b7:da:52:b4:f2:49:5d:00:d0:f1:71:54:ac:80.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '172.16.0.9' (ECDSA) to the list of known hosts.
root@172.16.0.9's password:
Last login: Sun Feb  7 07:40:19 2021 from 172.16.0.7
[root@crabNebula ~]#
```

# 2. Новый IP адрес должен "резолвиться" в "private" DNS запись, а hostname вашей машины должен быть таким же, как у ближайшей галактики к нашей Солнечной системе (ну или выберете обычное скучное имя). Продемонстрируйте результаты с помощью  одной из утилит (dig, nslookup, host)* или другой утиилитой

*hostnames
```bash
[root@mitnik ~]# hostnamectl
   Static hostname: mitnik
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 16d475c3430143feba210308853add75
           Boot ID: bb611526243c48f296aace41cdbf7114
    Virtualization: microsoft
  Operating System: CentOS Linux 7 (Core)
       CPE OS Name: cpe:/o:centos:centos:7
            Kernel: Linux 3.10.0-1160.el7.x86_64
      Architecture: x86-64

[root@crabNebula ~]# hostnamectl
   Static hostname: crabNebula
         Icon name: computer-vm
           Chassis: vm
        Machine ID: afabb1ea6a6a4a1998e83c2f7e7825b7
           Boot ID: 5ff49cf933614d6e8478e1f5ed02f720
    Virtualization: microsoft
  Operating System: CentOS Linux 7 (Core)
       CPE OS Name: cpe:/o:centos:centos:7
            Kernel: Linux 3.10.0-1160.el7.x86_64
      Architecture: x86-64
```
*Серверный /etc/hosts

```vim
127.0.0.1   localhost mitnik localhost4 localhost4.localdomain4
::1         localhost mitnik localhost6 localhost6.localdomain6
172.16.0.9  crabNebula
```
*Тест подключения к клиенту

```bash
[root@mitnik ~]# ssh root@crabNebula
The authenticity of host 'crabnebula (172.16.0.9)' can't be established.
ECDSA key fingerprint is SHA256:Cz95uiFz5oCo2KGUN0gLI89RWX8V/7wnenNDidTuxwI.
ECDSA key fingerprint is MD5:8c:ff:b7:da:52:b4:f2:49:5d:00:d0:f1:71:54:ac:80.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'crabnebula' (ECDSA) to the list of known hosts.
root@crabnebula's password:
Last login: Sun Feb  7 07:40:37 2021 from 172.16.0.9
[root@crabNebula ~]#
```
*Клиентский /etc/hosts

```vim
[root@crabNebula ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
172.16.0.7 mitnik
```
*Тест обращения к серверному

```bash
[root@crabNebula ~]# ping mitnik
PING mitnik (172.16.0.7) 56(84) bytes of data.
64 bytes from mitnik (172.16.0.7): icmp_seq=1 ttl=64 time=0.765 ms
64 bytes from mitnik (172.16.0.7): icmp_seq=2 ttl=64 time=0.537 ms
```
# 3. tcpdump и веселье:
### 3.1 Подключаетесь по ssh ко второму интерфейсу машины, логинетесь.
### 3.2 В одной сессии запускаете tcpdum, в другой сессии пытаетесь получить используя любой http клиент контент страницы по адресу: example.com
### 3.2* Получите контент страницы с помощью telnet
```bash
sudo telnet example.com 80
Trying 93.184.216.34...
Connected to example.com.
Escape character is '^]'.
GET /index.html HTTP/1.1
Host: example.com

HTTP/1.1 200 OK
Accept-Ranges: bytes
Age: 277863
Cache-Control: max-age=604800
Content-Type: text/html; charset=UTF-8
Date: Sun, 07 Feb 2021 17:15:53 GMT
Etag: "3147526947+gzip"
Expires: Sun, 14 Feb 2021 17:15:53 GMT
Last-Modified: Thu, 17 Oct 2019 07:18:26 GMT
Server: ECS (dcb/7F83)
Vary: Accept-Encoding
X-Cache: HIT
Content-Length: 1256

<!doctype html>
<html>
<head>
    <title>Example Domain</title>
```
### 3.3 В полученном выводе, найдите содержимое страницы и все HTTP заголовки.
### 3.4 tcpdump команда должна быть максимально "узконаправленная", то есть, в выводе должно быть минимум трафика, не относящегося к цели задания.
![6_Test_telnet_tcpdump](/images/6_tcpdump_telnet.jpg)
*Лог с ssh подключения на клиент и tcpdump (с начала telnet)
```bash
[root@crabNebula ~]# tcpdump -A -s 0 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'

tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
12:26:29.606340 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 139300                               4256:1393004282, ack 1859022747, win 457, options [nop,nop,TS val 17350695 ecr 4                               088513121], length 26: HTTP: GET /index.html HTTP/1.1
E..N..@.@......m]..".b.PS...n.o......0.....
...'...aGET /index.html HTTP/1.1

12:26:30.052528 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 0:26,                                ack 1, win 457, options [nop,nop,TS val 17351142 ecr 4088513121], length 26: HTT                               P: GET /index.html HTTP/1.1
E..N..@.@......m]..".b.PS...n.o......0.....
.......aGET /index.html HTTP/1.1

12:26:30.545971 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 0:26,                                ack 1, win 457, options [nop,nop,TS val 17351635 ecr 4088513121], length 26: HTT                               P: GET /index.html HTTP/1.1
E..N..@.@......m]..".b.PS...n.o......0.....
.......aGET /index.html HTTP/1.1

12:26:31.530741 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 0:26,                                ack 1, win 457, options [nop,nop,TS val 17352620 ecr 4088513121], length 26: HTT                               P: GET /index.html HTTP/1.1
E..N..@.@......m]..".b.PS...n.o......0.....
.......aGET /index.html HTTP/1.1

12:26:33.502509 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 0:26,                                ack 1, win 457, options [nop,nop,TS val 17354592 ecr 4088513121], length 26: HTT                               P: GET /index.html HTTP/1.1
E..N..@.@......m]..".b.PS...n.o......0.....
...`...aGET /index.html HTTP/1.1

12:26:37.446736 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 0:26,                                ack 1, win 457, options [nop,nop,TS val 17358536 ecr 4088513121], length 26: HTT                               P: GET /index.html HTTP/1.1
E..N..@.@......m]..".b.PS...n.o......0.....
.......aGET /index.html HTTP/1.1

12:26:45.342463 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 0:26,                                ack 1, win 457, options [nop,nop,TS val 17366432 ecr 4088513121], length 26: HTT                               P: GET /index.html HTTP/1.1
E..N..@.@......m]..".b.PS...n.o......0.....
.......aGET /index.html HTTP/1.1

12:26:52.859506 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 26:45,                                ack 1, win 457, options [nop,nop,TS val 17373949 ecr 4088547106], length 19: HT                               TP
E..G..@.@......m]..".b.PS...n.o......).....
.       ....G"Host: example.com

12:26:53.307515 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 26:45,                                ack 1, win 457, options [nop,nop,TS val 17374397 ecr 4088547106], length 19: HT                               TP
E..G..@.@......m]..".b.PS...n.o......).....
.       ....G"Host: example.com

12:26:53.801479 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 26:45,                                ack 1, win 457, options [nop,nop,TS val 17374891 ecr 4088547106], length 19: HT                               TP
E..G..@.@......m]..".b.PS...n.o......).....
.       ....G"Host: example.com

12:26:54.790517 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 26:45,                                ack 1, win 457, options [nop,nop,TS val 17375880 ecr 4088547106], length 19: HT                               TP
E..G..@.@......m]..".b.PS...n.o......).....
.       "...G"Host: example.com

12:26:56.767136 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 26:45,                                ack 1, win 457, options [nop,nop,TS val 17377856 ecr 4088547106], length 19: HT                               TP
E..G..@.@......m]..".b.PS...n.o......).....
.       *@..G"Host: example.com

12:27:00.718613 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 26:45,                                ack 1, win 457, options [nop,nop,TS val 17381808 ecr 4088547106], length 19: HT                               TP
E..G..@.@......m]..".b.PS...n.o......).....
.       9...G"Host: example.com

12:27:08.622548 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 26:45,                                ack 1, win 457, options [nop,nop,TS val 17389712 ecr 4088547106], length 19: HT                               TP
E..G..@.@......m]..".b.PS...n.o......).....
.       X...G"Host: example.com

12:27:24.414751 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 26:45, ack 1, win 457, options [nop,nop,TS val 17405504 ecr 4088547106], length 19: HTTP
E..G..@.@......m]..".b.PS...n.o......).....
.       .@..G"Host: example.com

12:27:32.617115 IP 93.184.216.34.http > crabNebula.54882: Flags [FP.], seq 1:591, ack 45, win 128, options [nop,nop,TS val 4088594215 ecr 17405504], length 590: HTTP: HTTP/1.0 408 Request Timeout
E...#;..7.gK].."...m.P.bn.o.S....... ......
...'.   .@HTTP/1.0 408 Request Timeout
Content-Type: text/html
Content-Length: 431
Connection: close
Date: Sun, 07 Feb 2021 17:27:00 GMT
Server: ECSF (dcb/7F83)

<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
         "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head>
                <title>408 - Request Timeout</title>
        </head>
        <body>
                <h1>408 - Request Timeout</h1>
                <div>Server timeout waiting for the HTTP request from the client.</div>
        </body>
</html>

12:27:32.617195 IP crabNebula.54882 > 93.184.216.34.http: Flags [P.], seq 45:49, ack 592, win 475, options [nop,nop,TS val 17413706 ecr 4088594215], length 4: HTTP
E..8..@.@......m]..".b.PS...n.q............
.       .J...'
```
# 4. Найдите номер порта, на котором запущен SSH сервер на хосте: 79.134.223.227 + все открытые порты.
```bash
[root@mitnik ~]# sudo nmap -sV -PN -p 22 79.134.223.227

Starting Nmap 6.40 ( http://nmap.org ) at 2021-02-08 00:56 MSK
Nmap scan report for 79-134-223-227.obit.ru (79.134.223.227)
Host is up.
PORT   STATE    SERVICE VERSION
22/tcp filtered ssh

Service detection performed. Please report any incorrect results at http://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.71 seconds

[root@mitnik ~]# sudo nmap -sV -PN -p- 79.134.223.227

```

# 5. Найти сообщение в icmp трафике, который поступает на этот хост (на lo интерфейс и/или 42.88.76.32)
```bash
[root@mitnik ~]# sudo ssh -i /home/admin/.ssh/hw_5 student8@45.88.76.32
The authenticity of host '45.88.76.32 (45.88.76.32)' can't be established.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '45.88.76.32' (ECDSA) to the list of known hosts.
███████████████████████████
███████▀▀▀░░░░░░░▀▀▀███████
████▀░░░░░░░░░░░░░░░░░▀████
███│░░░░░░░░░░░░░░░░░░░│███
██▌│░░░░░░░░░░░░░░░░░░░│▐██
██░└┐░░░░░░░░░░░░░░░░░┌┘░██
██░░└┐░░░░░░░░░░░░░░░┌┘░░██
██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██
██▌░│██████▌░░░▐██████│░▐██
███░│▐███▀▀░░▄░░▀▀███▌│░███
██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██
██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██
████▄─┘██▌░░░░░░░▐██└─▄████
█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████
████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████
█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████
███████▄░░░░░░░░░░░▄███████
██████████▄▄▄▄▄▄▄██████████
███████████████████████████
Linux vpc01 4.19.0-11-amd64 #1 SMP Debian 4.19.146-1 (2020-09-17) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
```
Нет прав использовать 
```bash
student8@vpc01:~$ /usr/sbin/tcpdump -i lo
tcpdump: lo: You don't have permission to capture on that device
(socket: Operation not permitted)

student8@vpc01:~$ test/tcpdump -i lo
tcpdump: lo: You don't have permission to capture on that device
(socket: Operation not permitted)
```
