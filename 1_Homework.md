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

# 1. Используя команду __ls__
## 1.1 Вывести на экран все файлы, которые расположены в секционных директориях /usr/share/man/manX и содержат слово "config" в имени.
```bash
[admin@localhost ~]$ sudo ls  /usr/share/man/man*/*config*
[sudo] password for admin:
/usr/share/man/man1/pkg-config.1.gz      /usr/share/man/man5/x509v3_config.5ssl.gz  /usr/share/man/man8/iprconfig.8.gz
/usr/share/man/man5/config.5ssl.gz       /usr/share/man/man8/authconfig.8.gz        /usr/share/man/man8/lvm-config.8.gz
/usr/share/man/man5/config-util.5.gz     /usr/share/man/man8/authconfig-tui.8.gz    /usr/share/man/man8/lvmconfig.8.gz
/usr/share/man/man5/selinux_config.5.gz  /usr/share/man/man8/chkconfig.8.gz         /usr/share/man/man8/lvm-dumpconfig.8.gz
/usr/share/man/man5/ssh_config.5.gz      /usr/share/man/man8/grub2-mkconfig.8.gz    /usr/share/man/man8/plipconfig.8.gz
/usr/share/man/man5/sshd_config.5.gz     /usr/share/man/man8/ifconfig.8.gz          /usr/share/man/man8/sys-unconfig.8.gz
```
или
```bash
[admin@localhost ~]$ sudo ls  /usr/share/man/man?/*config*
```
## 1.2 Одним вызовом ls найти все файлы, содержащие слово "system" в каталогах /usr/share/man/man1 и /usr/share/man/man7 
```bash
[admin@localhost ~]$ sudo ls /usr/share/man/man{1,7}/*system*
/usr/share/man/man1/systemctl.1.gz             /usr/share/man/man1/systemd-escape.1.gz             /usr/share/man/man1/systemd-tty-ask-password-agent.1.gz
/usr/share/man/man1/systemd.1.gz               /usr/share/man/man1/systemd-firstboot.1.gz          /usr/share/man/man7/lvmsystemid.7.gz
/usr/share/man/man1/systemd-analyze.1.gz       /usr/share/man/man1/systemd-firstboot.service.1.gz  /usr/share/man/man7/systemd.directives.7.gz
/usr/share/man/man1/systemd-ask-password.1.gz  /usr/share/man/man1/systemd-inhibit.1.gz            /usr/share/man/man7/systemd.generator.7.gz
/usr/share/man/man1/systemd-bootchart.1.gz     /usr/share/man/man1/systemd-machine-id-commit.1.gz  /usr/share/man/man7/systemd.index.7.gz
/usr/share/man/man1/systemd-cat.1.gz           /usr/share/man/man1/systemd-machine-id-setup.1.gz   /usr/share/man/man7/systemd.journal-fields.7.gz
/usr/share/man/man1/systemd-cgls.1.gz          /usr/share/man/man1/systemd-notify.1.gz             /usr/share/man/man7/systemd.special.7.gz
/usr/share/man/man1/systemd-cgtop.1.gz         /usr/share/man/man1/systemd-nspawn.1.gz             /usr/share/man/man7/systemd.time.7.gz
/usr/share/man/man1/systemd-delta.1.gz         /usr/share/man/man1/systemd-path.1.gz
/usr/share/man/man1/systemd-detect-virt.1.gz   /usr/share/man/man1/systemd-run.1.gz
```

# 2. Команда __find__

## 2.1 Найти в директории /usr/share/man все файлы, которые содержат слово "help"
```bash
[admin@localhost ~]$ find /usr/share/man -name *help*
/usr/share/man/man1/help.1.gz
/usr/share/man/man5/firewalld.helper.5.gz
/usr/share/man/man8/mkhomedir_helper.8.gz
/usr/share/man/man8/pwhistory_helper.8.gz
/usr/share/man/man8/ssh-pkcs11-helper.8.gz
```
## 2.2 Найти там же все файлы, имя которых начинается на "conf"
```bash
[admin@localhost ~]$ find /usr/share/man -name conf*
/usr/share/man/man5/config.5ssl.gz
/usr/share/man/man5/config-util.5.gz
```

## 2.3 Какие действия мы можем выполнить с файлами, найденными командой find (не запуская других команд)? 
Например можно удалить файл используя ключ __-delete__
```bash
[admin@localhost ~]$ ls
fileb1.txt  fileb2.txt  testdir
[admin@localhost ~]$ find fileb1.txt -delete
[admin@localhost ~]$ ls
fileb2.txt  testdir
```

# 3. Команды head и tail

## 3.1 Выведите последние 2 строки файла /etc/fstab
```bash
[admin@localhost ~]$ sudo tail -n2 /etc/fstab
UUID=c2d48651-fb36-4d59-89f6-133f0a7fe8d7 /boot                   xfs     defaults        0 0
/dev/mapper/centos-swap swap                    swap    defaults        0 0
```

## 3.2 Первые 7 строк файла /etc/yum.conf
```bash
[admin@localhost ~]$ sudo head -n7 /etc/yum.conf
[main]
cachedir=/var/cache/yum/$basearch/$releasever
keepcache=0
debuglevel=2
logfile=/var/log/yum.log
exactarch=1
obsoletes=1
```

## 3.3 Что произойдёт, если мы запросим больше строк, чем есть в файле?
Выведутся все строки
```bash
[admin@localhost ~]$ sudo wc -l /etc/fstab && head -n13 /etc/fstab
11 /etc/fstab

#
# /etc/fstab
# Created by anaconda on Mon Jan 11 22:11:52 2021
#
# Accessible filesystems, by reference, are maintained under '/dev/disk'
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
#
/dev/mapper/centos-root /                       xfs     defaults        0 0
UUID=c2d48651-fb36-4d59-89f6-133f0a7fe8d7 /boot                   xfs     defaults        0 0
/dev/mapper/centos-swap swap                    swap    defaults        0 0
```
