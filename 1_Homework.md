# 0. Установить вторую ВМ с доступом только до первой ВМ.
Использую __Hyper-V__. Основная идея поднять __NAT__ для виртуальных машин
1. Создаю в диспетчере виртуальных коммутаторов В дополнение к Интернет коммутатору еще один коммутатор Внутренний называю его __NAT__
2. Вирт. машине 1 (**Asterisk**) добавляю два сетевых адаптера __Internet__ и __NAT__
3. Вирт. машине 2 (**CentOS_2**) добавляю только NAT
### Настройка вирт. машины **Asterisk**
1. Прописываю статические настройки на __eth0__ (__Internet__)
```editorcongif
TYPE=Ethernet
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
DEVICE=eth0
ONBOOT=yes
IPADDR=192.168.0.104
NETMASK=255.255.255.0
GATEWAY=192.168.0.1
DNS1=192.168.0.1
DNS2=192.168.0.2
```
2. Прописываю статические настройки на __eth1__ (__NAT__)
```editorcongif
DEVICE=eth1
NAME=eth1
BOOTPROTO=static
ONBOOT=yes
IPADDR=192.168.1.2
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=192.168.1.1
```
### Настройка вирт. машины **CentOS_2**
Прописываю статические настройки на __eth0__ (__NAT__)
```editorcongif
TYPE=Ethernet
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
UUID=a21eda13-aabe-437b-a8fb-9666b7e7acae
DEVICE=eth0
ONBOOT=yes
IPADDR=192.168.1.3
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS=192.168.1.1
```

### Тест ssh с Asterisk на CentOS_2
```bash
[admin@localhost ~]$ ssh admin@192.168.1.3
The authenticity of host '192.168.1.3 (192.168.1.3)' can't be established.
ECDSA key fingerprint is SHA256:8rR0MGZQCkjRgZpDvt+XqBMjNf2SFWwLTxzOi2PiFe0.
ECDSA key fingerprint is MD5:2f:c9:56:ed:ae:2f:56:c4:5b:e9:e4:5e:a8:c7:e8:4a.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.1.3' (ECDSA) to the list of known hosts.
admin@192.168.1.3's password:
Last login: Wed Jan 13 13:36:08 2021 from 192.168.1.2
[admin@localhost ~]$ vi /etc/sysconfig/network-scripts/ifcfg-eth0
```

### Тест __ssh__ с __CentOS_2__ на __Asterisk__
![SSH connect to Asterisk from CENTOS_2](/images/0_ssh_from_CentOS_2_to_Asterisk.jpg)
### Тест __ip addr__ на Asterisk
![ip addr on Asterisk](/images/0_ip_addr_Asterisk.jpg)
### Тест __ip addr__ на CentOS_2
![ip addr on CENTOS_2](/images/0_ip_addr_CentOS_2.jpg)
