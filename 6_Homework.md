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

[root@mitnik ~]# sudo nmap -oN test65000.txt 79.134.223.227 -p1-65000

Starting Nmap 6.40 ( http://nmap.org ) at 2021-02-08 23:38 MSK
Nmap scan report for 79-134-223-227.obit.ru (79.134.223.227)
Host is up (0.0051s latency).
Not shown: 64999 filtered ports
PORT      STATE SERVICE
60022/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 814.12 seconds

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
```bash
student8@vpc01:~$ sudo /usr/sbin/tcpdump -nvvvxX -i lo icmp
tcpdump: listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
19:03:43.323591 IP (tos 0x0, ttl 64, id 41133, offset 0, flags [DF], proto ICMP (1), length 1370)
    127.0.0.1 > 127.0.0.1: ICMP echo request, id 1, seq 1, length 1350
        0x0000:  4500 055a a0ad 4000 4001 96f3 7f00 0001  E..Z..@.@.......
        0x0010:  7f00 0001 0800 002d 0001 0001 0022 0052  .......-.....".R
        0x0020:  006f 0062 006f 0074 0073 0020 0061 0072  .o.b.o.t.s...a.r
        0x0030:  0065 0020 006d 0075 006c 0074 0069 002d  .e...m.u.l.t.i.-
        0x0040:  0075 0073 0065 0020 0074 006f 006f 006c  .u.s.e...t.o.o.l
        0x0050:  0073 002e 0020 0052 006f 0062 006f 0074  .s.....R.o.b.o.t
        0x0060:  0073 0020 0073 0068 006f 0075 006c 0064  .s...s.h.o.u.l.d
        0x0070:  0020 006e 006f 0074 0020 0062 0065 0020  ...n.o.t...b.e..
        0x0080:  0064 0065 0073 0069 0067 006e 0065 0064  .d.e.s.i.g.n.e.d
        0x0090:  0020 0073 006f 006c 0065 006c 0079 0020  ...s.o.l.e.l.y..
        0x00a0:  006f 0072 0020 0070 0072 0069 006d 0061  .o.r...p.r.i.m.a
        0x00b0:  0072 0069 006c 0079 0020 0074 006f 0020  .r.i.l.y...t.o..
        0x00c0:  006b 0069 006c 006c 0020 006f 0072 0020  .k.i.l.l...o.r..
        0x00d0:  0068 0061 0072 006d 0020 0068 0075 006d  .h.a.r.m...h.u.m
        0x00e0:  0061 006e 0073 002c 0020 0065 0078 0063  .a.n.s.,...e.x.c
        0x00f0:  0065 0070 0074 0020 0069 006e 0020 0074  .e.p.t...i.n...t
        0x0100:  0068 0065 0020 0069 006e 0074 0065 0072  .h.e...i.n.t.e.r
        0x0110:  0065 0073 0074 0073 0020 006f 0066 0020  .e.s.t.s...o.f..
        0x0120:  006e 0061 0074 0069 006f 006e 0061 006c  .n.a.t.i.o.n.a.l
        0x0130:  0020 0073 0065 0063 0075 0072 0069 0074  ...s.e.c.u.r.i.t
        0x0140:  0079 002e 0020 0048 0075 006d 0061 006e  .y.....H.u.m.a.n
        0x0150:  0073 002c 0020 006e 006f 0074 0020 0052  .s.,...n.o.t...R
        0x0160:  006f 0062 006f 0074 0073 002c 0020 0061  .o.b.o.t.s.,...a
        0x0170:  0072 0065 0020 0072 0065 0073 0070 006f  .r.e...r.e.s.p.o
        0x0180:  006e 0073 0069 0062 006c 0065 0020 0061  .n.s.i.b.l.e...a
        0x0190:  0067 0065 006e 0074 0073 002e 0020 0052  .g.e.n.t.s.....R
        0x01a0:  006f 0062 006f 0074 0073 0020 0073 0068  .o.b.o.t.s...s.h
        0x01b0:  006f 0075 006c 0064 0020 0062 0065 0020  .o.u.l.d...b.e..
        0x01c0:  0064 0065 0073 0069 0067 006e 0065 0064  .d.e.s.i.g.n.e.d
        0x01d0:  0020 0061 006e 0064 0020 006f 0070 0065  ...a.n.d...o.p.e
        0x01e0:  0072 0061 0074 0065 0064 0020 0061 0073  .r.a.t.e.d...a.s
        0x01f0:  0020 0066 0061 0072 0020 0061 0073 0020  ...f.a.r...a.s..
        0x0200:  0070 0072 0061 0063 0074 0069 0063 0061  .p.r.a.c.t.i.c.a
        0x0210:  0062 006c 0065 0020 0074 006f 0020 0063  .b.l.e...t.o...c
        0x0220:  006f 006d 0070 006c 0079 0020 0077 0069  .o.m.p.l.y...w.i
        0x0230:  0074 0068 0020 0065 0078 0069 0073 0074  .t.h...e.x.i.s.t
        0x0240:  0069 006e 0067 0020 006c 0061 0077 0073  .i.n.g...l.a.w.s
        0x0250:  002c 0020 0066 0075 006e 0064 0061 006d  .,...f.u.n.d.a.m
        0x0260:  0065 006e 0074 0061 006c 0020 0072 0069  .e.n.t.a.l...r.i
        0x0270:  0067 0068 0074 0073 0020 0061 006e 0064  .g.h.t.s...a.n.d
        0x0280:  0020 0066 0072 0065 0065 0064 006f 006d  ...f.r.e.e.d.o.m
        0x0290:  0073 002c 0020 0069 006e 0063 006c 0075  .s.,...i.n.c.l.u
        0x02a0:  0064 0069 006e 0067 0020 0070 0072 0069  .d.i.n.g...p.r.i
        0x02b0:  0076 0061 0063 0079 002e 0020 0052 006f  .v.a.c.y.....R.o
        0x02c0:  0062 006f 0074 0073 0020 0061 0072 0065  .b.o.t.s...a.r.e
        0x02d0:  0020 0070 0072 006f 0064 0075 0063 0074  ...p.r.o.d.u.c.t
        0x02e0:  0073 002e 0020 0054 0068 0065 0079 0020  .s.....T.h.e.y..
        0x02f0:  0073 0068 006f 0075 006c 0064 0020 0062  .s.h.o.u.l.d...b
        0x0300:  0065 0020 0064 0065 0073 0069 0067 006e  .e...d.e.s.i.g.n
        0x0310:  0065 0064 0020 0075 0073 0069 006e 0067  .e.d...u.s.i.n.g
        0x0320:  0020 0070 0072 006f 0063 0065 0073 0073  ...p.r.o.c.e.s.s
        0x0330:  0065 0073 0020 0077 0068 0069 0063 0068  .e.s...w.h.i.c.h
        0x0340:  0020 0061 0073 0073 0075 0072 0065 0020  ...a.s.s.u.r.e..
        0x0350:  0074 0068 0065 0069 0072 0020 0073 0061  .t.h.e.i.r...s.a
        0x0360:  0066 0065 0074 0079 0020 0061 006e 0064  .f.e.t.y...a.n.d
        0x0370:  0020 0073 0065 0063 0075 0072 0069 0074  ...s.e.c.u.r.i.t
        0x0380:  0079 002e 0020 0052 006f 0062 006f 0074  .y.....R.o.b.o.t
        0x0390:  0073 0020 0061 0072 0065 0020 006d 0061  .s...a.r.e...m.a
        0x03a0:  006e 0075 0066 0061 0063 0074 0075 0072  .n.u.f.a.c.t.u.r
        0x03b0:  0065 0064 0020 0061 0072 0074 0065 0066  .e.d...a.r.t.e.f
        0x03c0:  0061 0063 0074 0073 002e 0020 0054 0068  .a.c.t.s.....T.h
        0x03d0:  0065 0079 0020 0073 0068 006f 0075 006c  .e.y...s.h.o.u.l
        0x03e0:  0064 0020 006e 006f 0074 0020 0062 0065  .d...n.o.t...b.e
        0x03f0:  0020 0064 0065 0073 0069 0067 006e 0065  ...d.e.s.i.g.n.e
        0x0400:  0064 0020 0069 006e 0020 0061 0020 0064  .d...i.n...a...d
        0x0410:  0065 0063 0065 0070 0074 0069 0076 0065  .e.c.e.p.t.i.v.e
        0x0420:  0020 0077 0061 0079 0020 0074 006f 0020  ...w.a.y...t.o..
        0x0430:  0065 0078 0070 006c 006f 0069 0074 0020  .e.x.p.l.o.i.t..
        0x0440:  0076 0075 006c 006e 0065 0072 0061 0062  .v.u.l.n.e.r.a.b
        0x0450:  006c 0065 0020 0075 0073 0065 0072 0073  .l.e...u.s.e.r.s
        0x0460:  003b 0020 0069 006e 0073 0074 0065 0061  .;...i.n.s.t.e.a
        0x0470:  0064 0020 0074 0068 0065 0069 0072 0020  .d...t.h.e.i.r..
        0x0480:  006d 0061 0063 0068 0069 006e 0065 0020  .m.a.c.h.i.n.e..
        0x0490:  006e 0061 0074 0075 0072 0065 0020 0073  .n.a.t.u.r.e...s
        0x04a0:  0068 006f 0075 006c 0064 0020 0062 0065  .h.o.u.l.d...b.e
        0x04b0:  0020 0074 0072 0061 006e 0073 0070 0061  ...t.r.a.n.s.p.a
        0x04c0:  0072 0065 006e 0074 002e 0020 0054 0068  .r.e.n.t.....T.h
        0x04d0:  0065 0020 0070 0065 0072 0073 006f 006e  .e...p.e.r.s.o.n
        0x04e0:  0020 0077 0069 0074 0068 0020 006c 0065  ...w.i.t.h...l.e
        0x04f0:  0067 0061 006c 0020 0072 0065 0073 0070  .g.a.l...r.e.s.p
        0x0500:  006f 006e 0073 0069 0062 0069 006c 0069  .o.n.s.i.b.i.l.i
        0x0510:  0074 0079 0020 0066 006f 0072 0020 0061  .t.y...f.o.r...a
        0x0520:  0020 0072 006f 0062 006f 0074 0020 0073  ...r.o.b.o.t...s
        0x0530:  0068 006f 0075 006c 0064 0020 0062 0065  .h.o.u.l.d...b.e
        0x0540:  0020 0061 0074 0074 0072 0069 0062 0075  ...a.t.t.r.i.b.u
        0x0550:  0074 0065 0064 002e 0022                 .t.e.d..."
19:03:43.324084 IP (tos 0x0, ttl 64, id 41134, offset 0, flags [none], proto ICMP (1), length 1370)
```
