# 1. Установить CentOS на две виртуальные машины
Виртуальные машина Scylla (VM1 – headnote) и Charybdis (VM2 - worker).
По 2 дополнительных диска по 5G
•	Scylla
![11_Scylla_main](/images/11_Scylla_main.jpg)
•	Charybdis
![11_Charybdis_main](/images/11_Charybdis_main.jpg)
# 2. Пользователь exam
```bash
[root@localhost exam]# visudo -f /etc/sudoers
```
```bash
## Same thing without a password
# %wheel        ALL=(ALL)       NOPASSWD: ALL
exam ALL=(ALL) NOPASSWD: ALL
```
__Scylla___ Network eth0

```bash
"/etc/sysconfig/network-scripts/ifcfg-eth0"
ONBOOT=yes
IPADDR=192.168.0.120
NETMASK=255.255.255.0
```
__Charibdys___ Network eth0
```bash
"/etc/sysconfig/network-scripts/ifcfg-eth0"
ONBOOT=yes
IPADDR=192.168.0.121
NETMASK=255.255.255.0
```
