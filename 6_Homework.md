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

# 2. Новый IP адрес должен "резолвиться" в "private" DNS запись, а hostname вашей машины должен быть таким же, как у ближайшей галактики к нашей Солнечной системе (ну или выберете обычное скучное имя). Продемонстрируйте результаты с помощью  одной из утилит (dig, nslookup, host)* или другой утиилитой

# 3. tcpdump и веселье:
  3.1 Подключаетесь по ssh ко второму интерфейсу машины, логинетесь.
  3.2 В одной сессии запускаете tcpdum, в другой сессии пытаетесь получить используя любой http клиент контент страницы по адресу: example.com
  3.2* Получите контент страницы с помощтью telnet
  3.3 В полученном выводе, найдите содержимое страницы и все HTTP заголовки.
  3.4 tcpdump команда должна быть максимально "узконаправленная", то есть, в выводе должно быть минимум трафика, не относящегося к цели задания.
  
# 4. Найдите номер порта, на котором запущен SSH сервер на хосте: 79.134.223.227 + все открытые порты.
