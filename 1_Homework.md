# 0. 
Использую __Hyper-V__. Основная идея поднять __NAT__ для виртуальных машин
1. Создаю в диспетчере виртуальных коммутаторов В дополнение к Интернет коммутатору еще один коммутатор Внутренний называю его __NAT__
2. Вирт. машине 1 (**Asterisk**) добавляю два сетевых адаптера __Internet__ и __NAT__
3. Вирт. машине 2 (**CentOS_2**) добавляю только NAT
### Настройка вирт. машины **Asterisk**
1. Прописываю статические настройки на __eth0__

2. Прописываю статические настройки на __eth1__

### Настройка вирт. машины **CentOS_2**
Прописываю статические настройки на __eth0__

### Тест
``[root@localhost ~]# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group defaul                                                         t qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group defa                                                         ult qlen 1000
    link/ether 00:15:5d:38:01:00 brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.104/24 brd 192.168.0.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::bf43:b9c6:1b12:7cc/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group defa                                                         ult qlen 1000
    link/ether 00:15:5d:38:01:03 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.2/24 brd 192.168.1.255 scope global noprefixroute eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::215:5dff:fe38:103/64 scope link
       valid_lft forever preferred_lft forever
[root@localhost ~]# ping 192.168.1.3
PING 192.168.1.3 (192.168.1.3) 56(84) bytes of data.
64 bytes from 192.168.1.3: icmp_seq=1 ttl=64 time=0.993 ms
64 bytes from 192.168.1.3: icmp_seq=2 ttl=64 time=0.633 ms
64 bytes from 192.168.1.3: icmp_seq=3 ttl=64 time=0.529 ms
64 bytes from 192.168.1.3: icmp_seq=4 ttl=64 time=0.447 ms
^C
--- 192.168.1.3 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3000ms
rtt min/avg/max/mdev = 0.447/0.650/0.993/0.209 ms
[root@localhost ~]# ssh admin@192.168.1.3
The authenticity of host '192.168.1.3 (192.168.1.3)' can't be established.
ECDSA key fingerprint is SHA256:8rR0MGZQCkjRgZpDvt+XqBMjNf2SFWwLTxzOi2PiFe0.
ECDSA key fingerprint is MD5:2f:c9:56:ed:ae:2f:56:c4:5b:e9:e4:5e:a8:c7:e8:4a.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.1.3' (ECDSA) to the list of known hosts.
admin@192.168.1.3's password:
[admin@localhost ~]$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:38:01:02 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.3/24 brd 192.168.1.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::7d88:bb0:fb28:7330/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
``
