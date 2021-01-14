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

# 4. Создайте в домашней директории файлы file_name1.md, file_name2.md и file_name3.md. Используя {}, переименуйте.

```bash
[admin@localhost ~]$ touch file_name{1..3}.md
[admin@localhost ~]$ mv -v {file_name1.md,file_name1.textdoc} && mv -v {file_name2.md,file_name2} && mv -v {file_name3.md,file_name3.md.latest} && mv -v {file_name1.textdoc,file_name1.txt}
‘file_name1.md’ -> ‘file_name1.textdoc’
‘file_name2.md’ -> ‘file_name2’
‘file_name3.md’ -> ‘file_name3.md.latest’
‘file_name1.textdoc’ -> ‘file_name1.txt’
[admin@localhost ~]$ ls
file_name1.txt  file_name2  file_name3.md.latest  testdir
```

# 5. Перейдите в директорию /mnt. Напишите как можно больше различных вариантов команды cd, с помощью которых вы можете вернуться обратно в домашнюю директорию вашего пользователя

```bash
cd ~

cd

cd $HOME

cd ~admin
 
cd /home/admin

[admin@localhost ~]$ cd /mnt
[admin@localhost mnt]$ cd -
/home/admin

```

# 6. Создайте одной командой в домашней директории 3 папки new, in-process, processed. При этом in-process должна содержать в себе еще 3 папки tread0, tread1, tread2

```bash
[admin@localhost ~]$ mkdir -p -v ~/{new,in-process/tread{0..2},processed}
mkdir: created directory ‘/home/admin/new’
mkdir: created directory ‘/home/admin/in-process’
mkdir: created directory ‘/home/admin/in-process/tread0’
mkdir: created directory ‘/home/admin/in-process/tread1’
mkdir: created directory ‘/home/admin/in-process/tread2’
mkdir: created directory ‘/home/admin/processed’
```

## 6.1 Cоздайте 100 файлов формата data[[:digit:]][[:digit:]] в папке new
```bash
[admin@localhost ~]$ touch new/files{1..100}.data[[:digit:]][[:digit:]]
[admin@localhost ~]$ ls new -la
total 12
drwxrwxr-x. 2 admin admin 8192 Jan 14 16:51 .
drwx------. 7 admin admin  156 Jan 14 16:50 ..
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files100.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files10.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files11.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files12.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files13.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files14.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files15.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files16.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files17.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files18.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files19.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files1.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files20.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files21.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files22.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files23.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files24.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files25.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files26.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files27.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files28.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files29.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files2.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files30.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files31.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files32.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files33.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files34.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files35.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files36.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files37.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files38.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files39.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files3.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files40.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files41.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files42.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files43.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files44.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files45.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files46.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files47.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files48.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files49.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files4.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files50.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files51.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files52.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files53.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files54.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files55.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files56.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files57.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files58.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files59.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files5.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files60.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files61.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files62.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files63.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files64.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files65.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files66.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files67.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files68.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files69.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files6.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files70.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files71.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files72.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files73.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files74.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files75.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files76.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files77.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files78.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files79.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files7.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files80.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files81.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files82.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files83.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files84.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files85.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files86.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files87.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files88.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files89.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files8.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files90.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files91.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files92.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files93.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files94.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files95.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files96.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files97.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files98.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files99.data[[:digit:]][[:digit:]]
-rw-rw-r--. 1 admin admin    0 Jan 14 16:51 files9.data[[:digit:]][[:digit:]]
```

## 6.2 Скопируйте 34 файла в tread0 и по 33 в tread1 и tread2 соответственно.
```bash
[admin@localhost ~]$ cp -v {new/files{1..34}.*,in-process/tread0} && cp -v {new/files{35..68}.*,in-process/tread1} && cp -v {new/files{69..100}.*,in-process/tread2}
‘new/files1.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files1.data[[:digit:]][[:digit:]]’
‘new/files2.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files2.data[[:digit:]][[:digit:]]’
‘new/files3.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files3.data[[:digit:]][[:digit:]]’
‘new/files4.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files4.data[[:digit:]][[:digit:]]’
‘new/files5.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files5.data[[:digit:]][[:digit:]]’
‘new/files6.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files6.data[[:digit:]][[:digit:]]’
‘new/files7.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files7.data[[:digit:]][[:digit:]]’
‘new/files8.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files8.data[[:digit:]][[:digit:]]’
‘new/files9.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files9.data[[:digit:]][[:digit:]]’
‘new/files10.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files10.data[[:digit:]][[:digit:]]’
‘new/files11.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files11.data[[:digit:]][[:digit:]]’
‘new/files12.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files12.data[[:digit:]][[:digit:]]’
‘new/files13.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files13.data[[:digit:]][[:digit:]]’
‘new/files14.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files14.data[[:digit:]][[:digit:]]’
‘new/files15.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files15.data[[:digit:]][[:digit:]]’
‘new/files16.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files16.data[[:digit:]][[:digit:]]’
‘new/files17.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files17.data[[:digit:]][[:digit:]]’
‘new/files18.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files18.data[[:digit:]][[:digit:]]’
‘new/files19.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files19.data[[:digit:]][[:digit:]]’
‘new/files20.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files20.data[[:digit:]][[:digit:]]’
‘new/files21.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files21.data[[:digit:]][[:digit:]]’
‘new/files22.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files22.data[[:digit:]][[:digit:]]’
‘new/files23.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files23.data[[:digit:]][[:digit:]]’
‘new/files24.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files24.data[[:digit:]][[:digit:]]’
‘new/files25.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files25.data[[:digit:]][[:digit:]]’
‘new/files26.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files26.data[[:digit:]][[:digit:]]’
‘new/files27.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files27.data[[:digit:]][[:digit:]]’
‘new/files28.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files28.data[[:digit:]][[:digit:]]’
‘new/files29.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files29.data[[:digit:]][[:digit:]]’
‘new/files30.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files30.data[[:digit:]][[:digit:]]’
‘new/files31.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files31.data[[:digit:]][[:digit:]]’
‘new/files32.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files32.data[[:digit:]][[:digit:]]’
‘new/files33.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files33.data[[:digit:]][[:digit:]]’
‘new/files34.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread0/files34.data[[:digit:]][[:digit:]]’
‘new/files35.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files35.data[[:digit:]][[:digit:]]’
‘new/files36.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files36.data[[:digit:]][[:digit:]]’
‘new/files37.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files37.data[[:digit:]][[:digit:]]’
‘new/files38.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files38.data[[:digit:]][[:digit:]]’
‘new/files39.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files39.data[[:digit:]][[:digit:]]’
‘new/files40.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files40.data[[:digit:]][[:digit:]]’
‘new/files41.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files41.data[[:digit:]][[:digit:]]’
‘new/files42.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files42.data[[:digit:]][[:digit:]]’
‘new/files43.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files43.data[[:digit:]][[:digit:]]’
‘new/files44.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files44.data[[:digit:]][[:digit:]]’
‘new/files45.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files45.data[[:digit:]][[:digit:]]’
‘new/files46.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files46.data[[:digit:]][[:digit:]]’
‘new/files47.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files47.data[[:digit:]][[:digit:]]’
‘new/files48.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files48.data[[:digit:]][[:digit:]]’
‘new/files49.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files49.data[[:digit:]][[:digit:]]’
‘new/files50.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files50.data[[:digit:]][[:digit:]]’
‘new/files51.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files51.data[[:digit:]][[:digit:]]’
‘new/files52.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files52.data[[:digit:]][[:digit:]]’
‘new/files53.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files53.data[[:digit:]][[:digit:]]’
‘new/files54.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files54.data[[:digit:]][[:digit:]]’
‘new/files55.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files55.data[[:digit:]][[:digit:]]’
‘new/files56.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files56.data[[:digit:]][[:digit:]]’
‘new/files57.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files57.data[[:digit:]][[:digit:]]’
‘new/files58.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files58.data[[:digit:]][[:digit:]]’
‘new/files59.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files59.data[[:digit:]][[:digit:]]’
‘new/files60.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files60.data[[:digit:]][[:digit:]]’
‘new/files61.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files61.data[[:digit:]][[:digit:]]’
‘new/files62.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files62.data[[:digit:]][[:digit:]]’
‘new/files63.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files63.data[[:digit:]][[:digit:]]’
‘new/files64.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files64.data[[:digit:]][[:digit:]]’
‘new/files65.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files65.data[[:digit:]][[:digit:]]’
‘new/files66.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files66.data[[:digit:]][[:digit:]]’
‘new/files67.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files67.data[[:digit:]][[:digit:]]’
‘new/files68.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread1/files68.data[[:digit:]][[:digit:]]’
‘new/files69.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files69.data[[:digit:]][[:digit:]]’
‘new/files70.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files70.data[[:digit:]][[:digit:]]’
‘new/files71.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files71.data[[:digit:]][[:digit:]]’
‘new/files72.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files72.data[[:digit:]][[:digit:]]’
‘new/files73.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files73.data[[:digit:]][[:digit:]]’
‘new/files74.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files74.data[[:digit:]][[:digit:]]’
‘new/files75.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files75.data[[:digit:]][[:digit:]]’
‘new/files76.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files76.data[[:digit:]][[:digit:]]’
‘new/files77.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files77.data[[:digit:]][[:digit:]]’
‘new/files78.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files78.data[[:digit:]][[:digit:]]’
‘new/files79.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files79.data[[:digit:]][[:digit:]]’
‘new/files80.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files80.data[[:digit:]][[:digit:]]’
‘new/files81.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files81.data[[:digit:]][[:digit:]]’
‘new/files82.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files82.data[[:digit:]][[:digit:]]’
‘new/files83.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files83.data[[:digit:]][[:digit:]]’
‘new/files84.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files84.data[[:digit:]][[:digit:]]’
‘new/files85.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files85.data[[:digit:]][[:digit:]]’
‘new/files86.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files86.data[[:digit:]][[:digit:]]’
‘new/files87.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files87.data[[:digit:]][[:digit:]]’
‘new/files88.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files88.data[[:digit:]][[:digit:]]’
‘new/files89.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files89.data[[:digit:]][[:digit:]]’
‘new/files90.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files90.data[[:digit:]][[:digit:]]’
‘new/files91.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files91.data[[:digit:]][[:digit:]]’
‘new/files92.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files92.data[[:digit:]][[:digit:]]’
‘new/files93.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files93.data[[:digit:]][[:digit:]]’
‘new/files94.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files94.data[[:digit:]][[:digit:]]’
‘new/files95.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files95.data[[:digit:]][[:digit:]]’
‘new/files96.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files96.data[[:digit:]][[:digit:]]’
‘new/files97.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files97.data[[:digit:]][[:digit:]]’
‘new/files98.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files98.data[[:digit:]][[:digit:]]’
‘new/files99.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files99.data[[:digit:]][[:digit:]]’
‘new/files100.data[[:digit:]][[:digit:]]’ -> ‘in-process/tread2/files100.data[[:digit:]][[:digit:]]’
```

## 6.3 Выведете содержимое каталога in-process одной командой
```bash
[admin@localhost ~]$ ls -R in-process
in-process:
tread0  tread1  tread2

in-process/tread0:
files10.data[[:digit:]][[:digit:]]  files21.data[[:digit:]][[:digit:]]  files32.data[[:digit:]][[:digit:]]
files11.data[[:digit:]][[:digit:]]  files22.data[[:digit:]][[:digit:]]  files33.data[[:digit:]][[:digit:]]
files12.data[[:digit:]][[:digit:]]  files23.data[[:digit:]][[:digit:]]  files34.data[[:digit:]][[:digit:]]
files13.data[[:digit:]][[:digit:]]  files24.data[[:digit:]][[:digit:]]  files3.data[[:digit:]][[:digit:]]
files14.data[[:digit:]][[:digit:]]  files25.data[[:digit:]][[:digit:]]  files4.data[[:digit:]][[:digit:]]
files15.data[[:digit:]][[:digit:]]  files26.data[[:digit:]][[:digit:]]  files5.data[[:digit:]][[:digit:]]
files16.data[[:digit:]][[:digit:]]  files27.data[[:digit:]][[:digit:]]  files6.data[[:digit:]][[:digit:]]
files17.data[[:digit:]][[:digit:]]  files28.data[[:digit:]][[:digit:]]  files7.data[[:digit:]][[:digit:]]
files18.data[[:digit:]][[:digit:]]  files29.data[[:digit:]][[:digit:]]  files8.data[[:digit:]][[:digit:]]
files19.data[[:digit:]][[:digit:]]  files2.data[[:digit:]][[:digit:]]   files9.data[[:digit:]][[:digit:]]
files1.data[[:digit:]][[:digit:]]   files30.data[[:digit:]][[:digit:]]
files20.data[[:digit:]][[:digit:]]  files31.data[[:digit:]][[:digit:]]

in-process/tread1:
files35.data[[:digit:]][[:digit:]]  files47.data[[:digit:]][[:digit:]]  files59.data[[:digit:]][[:digit:]]
files36.data[[:digit:]][[:digit:]]  files48.data[[:digit:]][[:digit:]]  files60.data[[:digit:]][[:digit:]]
files37.data[[:digit:]][[:digit:]]  files49.data[[:digit:]][[:digit:]]  files61.data[[:digit:]][[:digit:]]
files38.data[[:digit:]][[:digit:]]  files50.data[[:digit:]][[:digit:]]  files62.data[[:digit:]][[:digit:]]
files39.data[[:digit:]][[:digit:]]  files51.data[[:digit:]][[:digit:]]  files63.data[[:digit:]][[:digit:]]
files40.data[[:digit:]][[:digit:]]  files52.data[[:digit:]][[:digit:]]  files64.data[[:digit:]][[:digit:]]
files41.data[[:digit:]][[:digit:]]  files53.data[[:digit:]][[:digit:]]  files65.data[[:digit:]][[:digit:]]
files42.data[[:digit:]][[:digit:]]  files54.data[[:digit:]][[:digit:]]  files66.data[[:digit:]][[:digit:]]
files43.data[[:digit:]][[:digit:]]  files55.data[[:digit:]][[:digit:]]  files67.data[[:digit:]][[:digit:]]
files44.data[[:digit:]][[:digit:]]  files56.data[[:digit:]][[:digit:]]  files68.data[[:digit:]][[:digit:]]
files45.data[[:digit:]][[:digit:]]  files57.data[[:digit:]][[:digit:]]
files46.data[[:digit:]][[:digit:]]  files58.data[[:digit:]][[:digit:]]

in-process/tread2:
files100.data[[:digit:]][[:digit:]]  files78.data[[:digit:]][[:digit:]]  files89.data[[:digit:]][[:digit:]]
files68.data[[:digit:]][[:digit:]]   files79.data[[:digit:]][[:digit:]]  files90.data[[:digit:]][[:digit:]]
files69.data[[:digit:]][[:digit:]]   files80.data[[:digit:]][[:digit:]]  files91.data[[:digit:]][[:digit:]]
files70.data[[:digit:]][[:digit:]]   files81.data[[:digit:]][[:digit:]]  files92.data[[:digit:]][[:digit:]]
files71.data[[:digit:]][[:digit:]]   files82.data[[:digit:]][[:digit:]]  files93.data[[:digit:]][[:digit:]]
files72.data[[:digit:]][[:digit:]]   files83.data[[:digit:]][[:digit:]]  files94.data[[:digit:]][[:digit:]]
files73.data[[:digit:]][[:digit:]]   files84.data[[:digit:]][[:digit:]]  files95.data[[:digit:]][[:digit:]]
files74.data[[:digit:]][[:digit:]]   files85.data[[:digit:]][[:digit:]]  files96.data[[:digit:]][[:digit:]]
files75.data[[:digit:]][[:digit:]]   files86.data[[:digit:]][[:digit:]]  files97.data[[:digit:]][[:digit:]]
files76.data[[:digit:]][[:digit:]]   files87.data[[:digit:]][[:digit:]]  files98.data[[:digit:]][[:digit:]]
files77.data[[:digit:]][[:digit:]]   files88.data[[:digit:]][[:digit:]]  files99.data[[:digit:]][[:digit:]]
```

## 6.4 Переместите все файлы из каталогов tread в processed одной командой
```bash
[admin@localhost ~]$ mv -v in-process/tread{0..2}/* processed
```

## 6.5 Выведете содержимое каталога in-process и processed одной командой
```bash
[admin@localhost ~]$ ls -R processed in-process
in-process:
tread0  tread1  tread2

in-process/tread0:

in-process/tread1:

in-process/tread2:

processed:
files100.data[[:digit:]][[:digit:]]  files40.data[[:digit:]][[:digit:]]  files71.data[[:digit:]][[:digit:]]
files10.data[[:digit:]][[:digit:]]   files41.data[[:digit:]][[:digit:]]  files72.data[[:digit:]][[:digit:]]
files11.data[[:digit:]][[:digit:]]   files42.data[[:digit:]][[:digit:]]  files73.data[[:digit:]][[:digit:]]
files12.data[[:digit:]][[:digit:]]   files43.data[[:digit:]][[:digit:]]  files74.data[[:digit:]][[:digit:]]
files13.data[[:digit:]][[:digit:]]   files44.data[[:digit:]][[:digit:]]  files75.data[[:digit:]][[:digit:]]
files14.data[[:digit:]][[:digit:]]   files45.data[[:digit:]][[:digit:]]  files76.data[[:digit:]][[:digit:]]
files15.data[[:digit:]][[:digit:]]   files46.data[[:digit:]][[:digit:]]  files77.data[[:digit:]][[:digit:]]
files16.data[[:digit:]][[:digit:]]   files47.data[[:digit:]][[:digit:]]  files78.data[[:digit:]][[:digit:]]
files17.data[[:digit:]][[:digit:]]   files48.data[[:digit:]][[:digit:]]  files79.data[[:digit:]][[:digit:]]
files18.data[[:digit:]][[:digit:]]   files49.data[[:digit:]][[:digit:]]  files7.data[[:digit:]][[:digit:]]
files19.data[[:digit:]][[:digit:]]   files4.data[[:digit:]][[:digit:]]   files80.data[[:digit:]][[:digit:]]
files1.data[[:digit:]][[:digit:]]    files50.data[[:digit:]][[:digit:]]  files81.data[[:digit:]][[:digit:]]
files20.data[[:digit:]][[:digit:]]   files51.data[[:digit:]][[:digit:]]  files82.data[[:digit:]][[:digit:]]
files21.data[[:digit:]][[:digit:]]   files52.data[[:digit:]][[:digit:]]  files83.data[[:digit:]][[:digit:]]
files22.data[[:digit:]][[:digit:]]   files53.data[[:digit:]][[:digit:]]  files84.data[[:digit:]][[:digit:]]
files23.data[[:digit:]][[:digit:]]   files54.data[[:digit:]][[:digit:]]  files85.data[[:digit:]][[:digit:]]
files24.data[[:digit:]][[:digit:]]   files55.data[[:digit:]][[:digit:]]  files86.data[[:digit:]][[:digit:]]
files25.data[[:digit:]][[:digit:]]   files56.data[[:digit:]][[:digit:]]  files87.data[[:digit:]][[:digit:]]
files26.data[[:digit:]][[:digit:]]   files57.data[[:digit:]][[:digit:]]  files88.data[[:digit:]][[:digit:]]
files27.data[[:digit:]][[:digit:]]   files58.data[[:digit:]][[:digit:]]  files89.data[[:digit:]][[:digit:]]
files28.data[[:digit:]][[:digit:]]   files59.data[[:digit:]][[:digit:]]  files8.data[[:digit:]][[:digit:]]
files29.data[[:digit:]][[:digit:]]   files5.data[[:digit:]][[:digit:]]   files90.data[[:digit:]][[:digit:]]
files2.data[[:digit:]][[:digit:]]    files60.data[[:digit:]][[:digit:]]  files91.data[[:digit:]][[:digit:]]
files30.data[[:digit:]][[:digit:]]   files61.data[[:digit:]][[:digit:]]  files92.data[[:digit:]][[:digit:]]
files31.data[[:digit:]][[:digit:]]   files62.data[[:digit:]][[:digit:]]  files93.data[[:digit:]][[:digit:]]
files32.data[[:digit:]][[:digit:]]   files63.data[[:digit:]][[:digit:]]  files94.data[[:digit:]][[:digit:]]
files33.data[[:digit:]][[:digit:]]   files64.data[[:digit:]][[:digit:]]  files95.data[[:digit:]][[:digit:]]
files34.data[[:digit:]][[:digit:]]   files65.data[[:digit:]][[:digit:]]  files96.data[[:digit:]][[:digit:]]
files35.data[[:digit:]][[:digit:]]   files66.data[[:digit:]][[:digit:]]  files97.data[[:digit:]][[:digit:]]
files36.data[[:digit:]][[:digit:]]   files67.data[[:digit:]][[:digit:]]  files98.data[[:digit:]][[:digit:]]
files37.data[[:digit:]][[:digit:]]   files68.data[[:digit:]][[:digit:]]  files99.data[[:digit:]][[:digit:]]
files38.data[[:digit:]][[:digit:]]   files69.data[[:digit:]][[:digit:]]  files9.data[[:digit:]][[:digit:]]
files39.data[[:digit:]][[:digit:]]   files6.data[[:digit:]][[:digit:]]
files3.data[[:digit:]][[:digit:]]    files70.data[[:digit:]][[:digit:]]
```

## 6.6 Сравните количество файлов в каталогах new и processed, если они равны удалите файлы из new

Есть такая идея, если под условием подразумевается if-then
```bash
[admin@localhost ~]$ if [ $(ls new | wc -l) -eq $(ls processed | wc -l) ];then rm new/*; fi
```
