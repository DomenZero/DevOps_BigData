# Задача
Установить, настроить и запустить Hadoop Сore в минимальной конфигурации. Для этого  
потребуется подготовить 2 виртуальные машины: VM1 - headnode; VM2 - worker. 
# 1. Установить CentOS на две виртуальные машины  
Виртуальные машина Scylla (VM1 – headnote) и Charybdis (VM2 - worker).  
• VM1: 2CPU, 2-4G памяти, системный диск на 15-20G и дополнительные 2 диска по 5G
• VM2: 2CPU, 2-4G памяти, системный диск на 15-20G и дополнительные 2 диска по 5G   
![11_Scylla_main](/images/11_Scylla_main.jpg)  
Например Scylla  
![11_Scylla_settings](/images/11_Charybdis_main.jpg)  
# 2. При установке CentOS создать дополнительного пользователя exam и настроить для него
использование sudo без пароля. Все последующие действия необходимо выполнять от этого
пользователя, если не указано иное.
```bash
[root@localhost exam]# visudo -f /etc/sudoers
```
Добавим в файл безпарольное выполнение  
```bash
## Same thing without a password
exam ALL=(ALL) NOPASSWD: ALL
```
Информация о exam юзере  
```bash
[exam@localhost ~]$ lslogins -u
 UID USER PROC PWD-LOCK PWD-DENY  LAST-LOGIN GECOS
   0 root  105                   Feb23/10:24 root
1000 exam    2                      12:53:27 exam
# Тест доступа
[exam@localhost ~]$ sudo ls -la /root
total 28
dr-xr-x---.  2 root root  135 Feb 23 10:24 .
dr-xr-xr-x. 17 root root  224 Feb 23 09:49 ..
-rw-------.  1 root root 1281 Feb 23 09:49 anaconda-ks.cfg
-rw-------.  1 root root   21 Feb 23 10:24 .bash_history
-rw-r--r--.  1 root root   18 Dec 28  2013 .bash_logout
-rw-r--r--.  1 root root  176 Dec 28  2013 .bash_profile
-rw-r--r--.  1 root root  176 Dec 28  2013 .bashrc
-rw-r--r--.  1 root root  100 Dec 28  2013 .cshrc
-rw-r--r--.  1 root root  129 Dec 28  2013 .tcshrc

```
Параметры для ssh подключения  
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
# 3. Установить OpenJDK8 из репозитория CentOS.
```bash
[exam@localhost ~]$ sudo yum install java-1.8.0-openjdk-devel
Loaded plugins: fastestmirror
Determining fastest mirrors
 * base: mirror.sale-dedic.com
 * extras: mirror.awanti.com
 * updates: mirror.axelname.ru
base                                                                                                                                                                                   | 3.6 kB  00:00:00
extras                                                                                                                                                                                 | 2.9 kB  00:00:00
updates 
......

[exam@localhost ~]$ java -version
openjdk version "1.8.0_282"
OpenJDK Runtime Environment (build 1.8.0_282-b08)
OpenJDK 64-Bit Server VM (build 25.282-b08, mixed mode)

# узнать путь до Java, скопировать
[exam@scylla ~]$ sudo update-alternatives --config java

There is 1 program that provides 'java'.

  Selection    Command
-----------------------------------------------
*+ 1           java-1.8.0-openjdk.x86_64 (/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/bin/java)

# Добавить PATH для Java
[exam@scylla ~]$ vi .bash_profile
JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/bin/java
export JAVA_HOME

# Обновить .bash_profile
[exam@scylla ~]$ source .bash_profile
[exam@scylla ~]$ echo $JAVA_HOME
/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.282.b08-1.el7_9.x86_64/jre/bin/java

# Инфа для всех
[exam@charybdis ~]$ sudo vi /etc/profile
HADOOP_HOME=/opt/hadoop-3.1.2
export HADOOP_HOME

export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
export PATH=$JAVA_HOME/bin:$PATH

```
# 4. Скачать архив с Hadoop версии 3.1.2 (https://hadoop.apache.org/release/3.1.2.html)  
Копируем адрес ссылки https://archive.apache.org/dist/hadoop/common/hadoop-3.1.2/hadoop-3.1.2.tar.gz   
Выполняем скачивание в /home/downloads   
```bash
[exam@localhost ~]$ mkdir downloads
[exam@localhost ~]$ cd downloads
[exam@localhost downloads]$ sudo yum -y install wget
[exam@localhost downloads]$ sudo wget https://archive.apache.org/dist/hadoop/common/hadoop-3.1.2/hadoop-3.1.2.tar.gz
.... 
100%[====================================================================================================================================================================>] 332,433,589 1.20MB/s   in 2m 4s

2021-02-24 14:41:25 (2.56 MB/s) - ‘hadoop-3.1.2.tar.gz’ saved [332433589/332433589]

```
# 5. Распаковать содержимое архива в /opt/hadoop-3.1.2/
```bash
[exam@localhost downloads]$ sudo tar -xvf hadoop-3.1.2.tar.gz -C /opt

[exam@localhost downloads]$ ls -la /opt
total 0
drwxr-xr-x.  3 root root  26 Feb 24 14:58 .
dr-xr-xr-x. 17 root root 224 Feb 23 09:49 ..
drwxr-xr-x.  9 1001 1002 149 Jan 28  2019 hadoop-3.1.2
```
# 6. Сделать симлинк /usr/local/hadoop/current/ на директорию /opt/hadoop-3.1.2/
```bash
[exam@localhost downloads]$ sudo mkdir -p /usr/local/hadoop/current && sudo ln -s /opt/hadoop-3.1.2/ /usr/local/hadoop/current/
[exam@localhost downloads]$ ls -la
total 324644
drwxrwxr-x. 2 exam exam        33 Feb 24 14:39 .
drwx------. 3 exam exam       100 Feb 24 14:37 ..
-rw-r--r--. 1 root root 332433589 Feb  5  2019 hadoop-3.1.2.tar.gz
[exam@localhost downloads]$ ls -la /usr/local/hadoop/current
total 0
drwxr-xr-x. 2 root root 26 Feb 24 15:12 .
drwxr-xr-x. 3 root root 21 Feb 24 15:12 ..
lrwxrwxrwx. 1 root root 18 Feb 24 15:12 hadoop-3.1.2 -> /opt/hadoop-3.1.2/
```
# 7. Создать пользователей hadoop, yarn и hdfs, а также группу hadoop, в которую необходимо
добавить всех этих пользователей
```bash
[exam@localhost ~]$ sudo groupadd hadoop && sudo useradd -g hadoop hadoop && sudo useradd -g hadoop yarn && sudo useradd -g hadoop hdfs
[exam@localhost ~]$ groups hadoop
hadoop : hadoop
[exam@localhost ~]$ groups yarn
yarn : hadoop
[exam@localhost ~]$ groups hdfs
hdfs : hadoop

# Optional: set password
sudo passwd hadoop
sudo passwd hdfs
sudo passwd yarn

```
# 8. Создать для обоих дополнительных дисков разделы размером в 100% диска.
```bash
[exam@localhost downloads]$ sudo fdisk -l

Disk /dev/sdb: 5368 MB, 5368709120 bytes, 10485760 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes


Disk /dev/sda: 21.5 GB, 21474836480 bytes, 41943040 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk label type: dos
Disk identifier: 0x000a5905

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048     2099199     1048576   83  Linux
/dev/sda2         2099200    41943039    19921920   8e  Linux LVM

Disk /dev/sdc: 5368 MB, 5368709120 bytes, 10485760 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes


Disk /dev/mapper/centos-root: 18.2 GB, 18249416704 bytes, 35643392 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes


Disk /dev/mapper/centos-swap: 2147 MB, 2147483648 bytes, 4194304 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes

# Наши диски /dev/sdb и /dev/sdc
# Первый диск
[exam@localhost downloads]$ sudo parted /dev/sdb
GNU Parted 3.1
Using /dev/sdb
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) print
Error: /dev/sdb: unrecognised disk label
Model: Msft Virtual Disk (scsi)
Disk /dev/sdb: 5369MB
Sector size (logical/physical): 512B/4096B
Partition Table: unknown
Disk Flags:
(parted) mklabel gpt
(parted) mkpart hdd1_Scylla
File system type?  [ext2]? ext4
Start? 0%
End? 100%
(parted) print
Model: Msft Virtual Disk (scsi)
Disk /dev/sdb: 5369MB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name         Flags
 1      1049kB  5368MB  5367MB               hdd1_Scylla

# Второй диск
[exam@localhost downloads]$ sudo parted /dev/sdc
GNU Parted 3.1
Using /dev/sdc
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) mklabel gpt
(parted) mkpart hdd2_Scylla
File system type?  [ext2]? ext4
Start? 0%
End? 100%
(parted) print
Model: Msft Virtual Disk (scsi)
Disk /dev/sdc: 5369MB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name         Flags
 1      1049kB  5368MB  5367MB               hdd2_Scylla
```
# 9. Инициализировать разделы из п.8 в качестве физических томов для LVM.
```bash
[exam@localhost downloads]$ sudo parted /dev/sdb
GNU Parted 3.1
Using /dev/sdb
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) print
Model: Msft Virtual Disk (scsi)
Disk /dev/sdb: 5369MB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name         Flags
 1      1049kB  5368MB  5367MB               hdd1_Scylla

(parted) set 1 lvm on
(parted) quit
Information: You may need to update /etc/fstab.

[exam@localhost downloads]$ sudo parted /dev/sdc
GNU Parted 3.1
Using /dev/sdc
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) print
Model: Msft Virtual Disk (scsi)
Disk /dev/sdc: 5369MB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name         Flags
 1      1049kB  5368MB  5367MB               hdd2_Scylla

(parted) set 1 lvm on
(parted) quit
```
```bash
[exam@localhost downloads]$ sudo fdisk /dev/sdb
WARNING: fdisk GPT support is currently new, and therefore in an experimental phase. Use at your own discretion.
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help): n
Partition number (2-128, default 2): 2
First sector (34-10485726, default 10483712):
Last sector, +sectors or +size{K,M,G,T,P} (10483712-10485726, default 10485726):
Created partition 2


Command (m for help): m
Command action
   d   delete a partition
   g   create a new empty GPT partition table
   G   create an IRIX (SGI) partition table
   l   list known partition types
   m   print this menu
   n   add a new partition
   o   create a new empty DOS partition table
   p   print the partition table
   q   quit without saving changes
   s   create a new empty Sun disklabel
   t   change a partition's system id
   v   verify the partition table
   w   write table to disk and exit
   x   extra functionality (experts only)

Command (m for help): t
Partition number (1,2, default 2):
Partition type (type L to list all types): L
  1 EFI System                     C12A7328-F81F-11D2-BA4B-00A0C93EC93B
  2 MBR partition scheme           024DEE41-33E7-11D3-9D69-0008C781F39F
  3 Intel Fast Flash               D3BFE2DE-3DAF-11DF-BA40-E3A556D89593
  4 BIOS boot                      21686148-6449-6E6F-744E-656564454649
  5 Sony boot partition            F4019732-066E-4E12-8273-346C5641494F
  6 Lenovo boot partition          BFBFAFE7-A34F-448A-9A5B-6213EB736C22
  7 PowerPC PReP boot              9E1A2D38-C612-4316-AA26-8B49521E5A8B
  8 ONIE boot                      7412F7D5-A156-4B13-81DC-867174929325
  9 ONIE config                    D4E6E2CD-4469-46F3-B5CB-1BFF57AFC149
 10 Microsoft reserved             E3C9E316-0B5C-4DB8-817D-F92DF00215AE
 11 Microsoft basic data           EBD0A0A2-B9E5-4433-87C0-68B6B72699C7
 12 Microsoft LDM metadata         5808C8AA-7E8F-42E0-85D2-E1E90434CFB3
 13 Microsoft LDM data             AF9B60A0-1431-4F62-BC68-3311714A69AD
 14 Windows recovery environment   DE94BBA4-06D1-4D40-A16A-BFD50179D6AC
 15 IBM General Parallel Fs        37AFFC90-EF7D-4E96-91C3-2D7AE055B174
 16 Microsoft Storage Spaces       E75CAF8F-F680-4CEE-AFA3-B001E56EFC2D
 17 HP-UX data                     75894C1E-3AEB-11D3-B7C1-7B03A0000000
 18 HP-UX service                  E2A1E728-32E3-11D6-A682-7B03A0000000
 19 Linux swap                     0657FD6D-A4AB-43C4-84E5-0933C84B4F4F
 20 Linux filesystem               0FC63DAF-8483-4772-8E79-3D69D8477DE4
 21 Linux server data              3B8F8425-20E0-4F3B-907F-1A25A76F98E8
 22 Linux root (x86)               44479540-F297-41B2-9AF7-D131D5F0458A
 23 Linux root (ARM)               69DAD710-2CE4-4E3C-B16C-21A1D49ABED3
 24 Linux root (x86-64)            4F68BCE3-E8CD-4DB1-96E7-FBCAF984B709
 25 Linux root (ARM-64)            B921B045-1DF0-41C3-AF44-4C6F280D3FAE
 26 Linux root  (IA-64)             993D8D3D-F80E-4225-855A-9DAF8ED7EA97
 27 Linux reserved                 8DA63339-0007-60C0-C436-083AC8230908
 28 Linux home                     933AC7E1-2EB4-4F13-B844-0E14E2AEF915
 29 Linux RAID                     A19D880F-05FC-4D3B-A006-743F0F84911E
 30 Linux extended boot            BC13C2FF-59E6-4262-A352-B275FD6F7172
 31 Linux LVM                      E6D6D379-F507-44C2-A23C-238F2A3DF928
 32 FreeBSD data                   516E7CB4-6ECF-11D6-8FF8-00022D09712B
 33 FreeBSD boot                   83BD6B9D-7F41-11DC-BE0B-001560B84F0F
 34 FreeBSD swap                   516E7CB5-6ECF-11D6-8FF8-00022D09712B
 35 FreeBSD UFS                    516E7CB6-6ECF-11D6-8FF8-00022D09712B
 36 FreeBSD ZFS                    516E7CBA-6ECF-11D6-8FF8-00022D09712B
 37 FreeBSD Vinum                  516E7CB8-6ECF-11D6-8FF8-00022D09712B
 38 Apple HFS/HFS+                 48465300-0000-11AA-AA11-00306543ECAC
 39 Apple UFS                      55465300-0000-11AA-AA11-00306543ECAC
 40 Apple RAID                     52414944-0000-11AA-AA11-00306543ECAC
 41 Apple RAID offline             52414944-5F4F-11AA-AA11-00306543ECAC
 42 Apple boot                     426F6F74-0000-11AA-AA11-00306543ECAC
 43 Apple label                    4C616265-6C00-11AA-AA11-00306543ECAC
 44 Apple TV recovery              5265636F-7665-11AA-AA11-00306543ECAC
 45 Apple Core storage             53746F72-6167-11AA-AA11-00306543ECAC
 46 Solaris boot                   6A82CB45-1DD2-11B2-99A6-080020736631
 47 Solaris root                   6A85CF4D-1DD2-11B2-99A6-080020736631
 48 Solaris /usr & Apple ZFS       6A898CC3-1DD2-11B2-99A6-080020736631
 49 Solaris swap                   6A87C46F-1DD2-11B2-99A6-080020736631
 50 Solaris backup                 6A8B642B-1DD2-11B2-99A6-080020736631
 51 Solaris /var                   6A8EF2E9-1DD2-11B2-99A6-080020736631
 52 Solaris /home                  6A90BA39-1DD2-11B2-99A6-080020736631
 53 Solaris alternate sector       6A9283A5-1DD2-11B2-99A6-080020736631
 54 Solaris reserved 1             6A945A3B-1DD2-11B2-99A6-080020736631
 55 Solaris reserved 2             6A9630D1-1DD2-11B2-99A6-080020736631
 56 Solaris reserved 3             6A980767-1DD2-11B2-99A6-080020736631
 57 Solaris reserved 4             6A96237F-1DD2-11B2-99A6-080020736631
 58 Solaris reserved 5             6A8D2AC7-1DD2-11B2-99A6-080020736631
 59 NetBSD swap                    49F48D32-B10E-11DC-B99B-0019D1879648
 60 NetBSD FFS                     49F48D5A-B10E-11DC-B99B-0019D1879648
 61 NetBSD LFS                     49F48D82-B10E-11DC-B99B-0019D1879648
 62 NetBSD concatenated            2DB519C4-B10E-11DC-B99B-0019D1879648
 63 NetBSD encrypted               2DB519EC-B10E-11DC-B99B-0019D1879648
 64 NetBSD RAID                    49F48DAA-B10E-11DC-B99B-0019D1879648
 65 ChromeOS kernel                FE3A2A5D-4F32-41A7-B725-ACCC3285A309
 66 ChromeOS root fs               3CB8E202-3B7E-47DD-8A3C-7FF2A13CFCEC
 67 ChromeOS reserved              2E0A753D-9E48-43B0-8337-B15192CB1B5E
 68 MidnightBSD data               85D5E45A-237C-11E1-B4B3-E89A8F7FC3A7
 69 MidnightBSD boot               85D5E45E-237C-11E1-B4B3-E89A8F7FC3A7
 70 MidnightBSD swap               85D5E45B-237C-11E1-B4B3-E89A8F7FC3A7
 71 MidnightBSD UFS                0394EF8B-237E-11E1-B4B3-E89A8F7FC3A7
 72 MidnightBSD ZFS                85D5E45D-237C-11E1-B4B3-E89A8F7FC3A7
 73 MidnightBSD Vinum              85D5E45C-237C-11E1-B4B3-E89A8F7FC3A7
 74 Ceph Journal                   45B0969E-9B03-4F30-B4C6-B4B80CEFF106
 75 Ceph Encrypted Journal         45B0969E-9B03-4F30-B4C6-5EC00CEFF106
 76 Ceph OSD                       4FBD7E29-9D25-41B8-AFD0-062C0CEFF05D
 77 Ceph crypt OSD                 4FBD7E29-9D25-41B8-AFD0-5EC00CEFF05D
 78 Ceph disk in creation          89C57F98-2FE5-4DC0-89C1-F3AD0CEFF2BE
 79 Ceph crypt disk in creation    89C57F98-2FE5-4DC0-89C1-5EC00CEFF2BE
 80 OpenBSD data                   824CC7A0-36A8-11E3-890A-952519AD3F61
 81 QNX6 file system               CEF5A9AD-73BC-4601-89F3-CDEEEEE321A1
 82 Plan 9 partition               C91818F9-8025-47AF-89D2-F030D7000C2C

Partition type (type L to list all types):
Partition type (type L to list all types): 31
Changed type of partition 'Linux filesystem' to 'Linux LVM'

```
```bash
[exam@localhost downloads]$ sudo mkfs.ext4 /dev/sdb
mke2fs 1.42.9 (28-Dec-2013)
/dev/sdb is entire device, not just one partition!
Proceed anyway? (y,n) y
Discarding device blocks: done
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
327680 inodes, 1310720 blocks
65536 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=1342177280
40 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736

Allocating group tables: done
Writing inode tables: done
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done

[exam@localhost downloads]$ sudo mkfs.ext4 /dev/sdc
mke2fs 1.42.9 (28-Dec-2013)
/dev/sdc is entire device, not just one partition!
Proceed anyway? (y,n) y
Discarding device blocks: done
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
327680 inodes, 1310720 blocks
65536 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=1342177280
40 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736

Allocating group tables: done
Writing inode tables: done
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done

[exam@localhost downloads]$ sudo pvcreate /dev/sdb
WARNING: ext4 signature detected on /dev/sdb at offset 1080. Wipe it? [y/n]: y
  Wiping ext4 signature on /dev/sdb.
  Physical volume "/dev/sdb" successfully created.
[exam@localhost downloads]$ sudo pvcreate /dev/sdc
WARNING: ext4 signature detected on /dev/sdc at offset 1080. Wipe it? [y/n]: y
  Wiping ext4 signature on /dev/sdc.
  Physical volume "/dev/sdc" successfully created.
[exam@localhost downloads]$ sudo pvscan
  PV /dev/sda2   VG centos          lvm2 [<19.00 GiB / 0    free]
  PV /dev/sdc                       lvm2 [5.00 GiB]
  PV /dev/sdb                       lvm2 [5.00 GiB]
  Total: 3 [<29.00 GiB] / in use: 1 [<19.00 GiB] / in no VG: 2 [10.00 GiB]
[exam@localhost downloads]$ sudo pvdisplay
  --- Physical volume ---
  PV Name               /dev/sda2
  VG Name               centos
  PV Size               <19.00 GiB / not usable 3.00 MiB
  Allocatable           yes (but full)
  PE Size               4.00 MiB
  Total PE              4863
  Free PE               0
  Allocated PE          4863
  PV UUID               ui2xxq-kaF8-HYWE-9WN8-7jnM-3deA-25e8Kj

  "/dev/sdc" is a new physical volume of "5.00 GiB"
  --- NEW Physical volume ---
  PV Name               /dev/sdc
  VG Name
  PV Size               5.00 GiB
  Allocatable           NO
  PE Size               0
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               HgXZV2-Fu9W-zNr5-wStp-W2R6-P7fg-LacZJy

  "/dev/sdb" is a new physical volume of "5.00 GiB"
  --- NEW Physical volume ---
  PV Name               /dev/sdb
  VG Name
  PV Size               5.00 GiB
  Allocatable           NO
  PE Size               0
  Total PE              0
  Free PE               0
  Allocated PE          0


```
# 10. Создать две группы LVM и добавить в каждую из них по одному физическому тому из п.9.
```bash

[exam@localhost ~]$ sudo vgcreate LVM_group1 /dev/sdb
  Volume group "LVM_group1" successfully created
[exam@localhost ~]$ sudo vgcreate LVM_group2 /dev/sdc
  Volume group "LVM_group2" successfully created
[exam@localhost ~]$ sudo vgdisplay
  --- Volume group ---
  VG Name               LVM_group1
  System ID
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <5.00 GiB
  PE Size               4.00 MiB
  Total PE              1279
  Alloc PE / Size       0 / 0
  Free  PE / Size       1279 / <5.00 GiB
  VG UUID               FFIQM4-RZJr-IHqL-JZMd-v2xH-0UG2-4QKWOQ

  --- Volume group ---
  VG Name               LVM_group2
  System ID
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <5.00 GiB
  PE Size               4.00 MiB
  Total PE              1279
  Alloc PE / Size       0 / 0
  Free  PE / Size       1279 / <5.00 GiB
  VG UUID               qk1OBf-ZBUl-1j0S-KcNG-QZqr-Mt4s-Mfh1Hs

  --- Volume group ---
  VG Name               centos
  System ID
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  3
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <19.00 GiB
  PE Size               4.00 MiB
  Total PE              4863
  Alloc PE / Size       4863 / <19.00 GiB
  Free  PE / Size       0 / 0
  VG UUID               OxTThu-I0WV-7jje-ilwW-u3yH-l8mn-aeKQg1

```
# 11. В каждой из групп из п.10 создать логический том LVM размером 100% группы.
```bash
[exam@localhost ~]$ sudo lvcreate -l 100%FREE -n log_vol1 LVM_group1
  Logical volume "log_vol1" created.
[exam@localhost ~]$ sudo lvcreate -l 100%FREE -n log_vol2 LVM_group2
  Logical volume "log_vol2" created.

# Test
[exam@localhost ~]$ sudo lvdisplay
  --- Logical volume ---
  LV Path                /dev/LVM_group1/log_vol1
  LV Name                log_vol1
  VG Name                LVM_group1
  LV UUID                ZUnNlz-lcnh-L9qJ-f9hz-a8RM-46vd-YiKowp
  LV Write Access        read/write
  LV Creation host, time localhost.localdomain, 2021-02-25 12:34:07 -0500
  LV Status              available
  # open                 0
  LV Size                <5.00 GiB
  Current LE             1279
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           253:2

  --- Logical volume ---
  LV Path                /dev/LVM_group2/log_vol2
  LV Name                log_vol2
  VG Name                LVM_group2
  LV UUID                9Trumx-Hym3-E2XB-qhch-5JWc-ILW9-ukEX5y
  LV Write Access        read/write
  LV Creation host, time localhost.localdomain, 2021-02-25 12:34:15 -0500
  LV Status              available
  # open                 0
  LV Size                <5.00 GiB
  Current LE             1279
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           253:3

  --- Logical volume ---
  LV Path                /dev/centos/swap
  LV Name                swap
  VG Name                centos
  LV UUID                VUFJnZ-KUSl-CPMW-vaOc-PdMm-CoJs-PgfpKX
  LV Write Access        read/write
  LV Creation host, time localhost, 2021-02-23 09:46:09 -0500
  LV Status              available
  # open                 2
  LV Size                2.00 GiB
  Current LE             512
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           253:1

  --- Logical volume ---
  LV Path                /dev/centos/root
  LV Name                root
  VG Name                centos
  LV UUID                CJFPul-QCGk-y5Sn-Nnia-9MK9-0q3R-fmm2g2
  LV Write Access        read/write
  LV Creation host, time localhost, 2021-02-23 09:46:10 -0500
  LV Status              available
  # open                 1
  LV Size                <17.00 GiB
  Current LE             4351
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           253:0
```
# 12. На каждом логическом томе LVM создать файловую систему ext4.
```bash
[exam@localhost ~]$ sudo mkfs.ext4 /dev/LVM_group2/log_vol2
mke2fs 1.42.9 (28-Dec-2013)
Discarding device blocks: done
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
327680 inodes, 1309696 blocks
65484 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=1342177280
40 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736

Allocating group tables: done
Writing inode tables: done
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done

[exam@localhost ~]$ sudo mkfs.ext4 /dev/LVM_group1/log_vol1
mke2fs 1.42.9 (28-Dec-2013)
Discarding device blocks: done
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
327680 inodes, 1309696 blocks
65484 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=1342177280
40 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736

Allocating group tables: done
Writing inode tables: done
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done
```
# 13. Создать директории и использовать их в качестве точек монтирования файловых систем из
п.12:
• /opt/mount1
• /opt/mount2
```bash
[exam@localhost ~]$ sudo mkdir /opt/mount1 && sudo mount /dev/LVM_group1/log_vol1 /opt/mount1
[exam@localhost ~]$ sudo mkdir /opt/mount2 && sudo mount /dev/LVM_group2/log_vol2 /opt/mount2

#Test
[exam@localhost ~]$ df -h
Filesystem                       Size  Used Avail Use% Mounted on
devtmpfs                         1.9G     0  1.9G   0% /dev
tmpfs                            1.9G     0  1.9G   0% /dev/shm
tmpfs                            1.9G  9.0M  1.9G   1% /run
tmpfs                            1.9G     0  1.9G   0% /sys/fs/cgroup
/dev/mapper/centos-root           17G  2.8G   15G  17% /
/dev/sda1                       1014M  150M  865M  15% /boot
tmpfs                            379M     0  379M   0% /run/user/1000
tmpfs                            379M     0  379M   0% /run/user/0
/dev/mapper/LVM_group1-log_vol1  4.8G   20M  4.6G   1% /opt/mount1
/dev/mapper/LVM_group2-log_vol2  4.8G   20M  4.6G   1% /opt/mount2

```
# 14. Настроить систему так, чтобы монтирование происходило автоматически при запуске системы.
Произвести монтирование новых файловых систем.
```bash
[exam@localhost ~]$ lsblk -f
NAME                  FSTYPE      LABEL UUID                                   MOUNTPOINT
fd0
sda
├─sda1                xfs               fde672d4-4ee8-44f5-bb09-54a16272545f   /boot
└─sda2                LVM2_member       ui2xxq-kaF8-HYWE-9WN8-7jnM-3deA-25e8Kj
  ├─centos-root       xfs               50097d23-79a9-4511-a342-3de8994e7fdf   /
  └─centos-swap       swap              887f08af-e5d8-418b-9001-6451480e1176   [SWAP]
sdb                   LVM2_member       xnaOVb-URfc-Ythg-53px-be0L-PbJY-ohIlEe
└─LVM_group1-log_vol1 ext4              523ecdd7-43b0-4fa0-b2ac-0b7a100146eb   /opt/mount1
sdc                   LVM2_member       HgXZV2-Fu9W-zNr5-wStp-W2R6-P7fg-LacZJy
└─LVM_group2-log_vol2 ext4              6702c40d-ad44-4721-afa5-929288de7588   /opt/mount2

[exam@localhost ~]$ sudo vi /etc/fstab
[exam@localhost ~]$ cat /etc/fstab | grep mount
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
UUID=523ecdd7-43b0-4fa0-b2ac-0b7a100146eb /opt/mount1           ext4    defaults        0 0
UUID=6702c40d-ad44-4721-afa5-929288de7588 /opt/mount2           ext4    defaults        0 0


# Для Charybdis (VM2)

[exam@localhost ~]$ lsblk -f
NAME                  FSTYPE      LABEL UUID                                   MOUNTPOINT
fd0
sda
├─sda1                xfs               574a94c5-efb4-4350-8ecf-50e038d78954   /boot
└─sda2                LVM2_member       fI0cTK-DbzR-UdCg-q8W1-YtFi-fXQw-gFV3aN
  ├─centos-root       xfs               f9c8d26f-468f-4481-9c3f-86e3496f8ad0   /
  └─centos-swap       swap              58608058-1089-404b-80fa-01e62bae8a35   [SWAP]
sdb                   LVM2_member       O1hpvl-YGMg-qOO8-JQXT-RV2b-lQTI-vwdjLo
└─LVM_group1-log_vol1 ext4              d35367e7-bc3a-4ae6-a54c-391ad4e33842   /opt/mount1
sdc                   LVM2_member       pgIcS0-oSny-IodZ-R6JE-5DQC-5ASe-3XEfAl
└─LVM_group2-log_vol2 ext4              7142c0f6-c76f-49cb-b122-a643de10cd18   /opt/mount2
[exam@localhost ~]$ cat /etc/fstab | grep mount
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
UUID=d35367e7-bc3a-4ae6-a54c-391ad4e33842 /opt/mount1           ext4    defaults        0 0
UUID=7142c0f6-c76f-49cb-b122-a643de10cd18 /opt/mount2           ext4    defaults        0 0

```
# Для VM1 (Scylla) (шаги 15-16):
#### 15. После монтирования создать 2 директории для хранения файлов Namenode сервиса HDFS:
• /opt/mount1/namenode-dir  
• /opt/mount2/namenode-dir  
```bash
[exam@localhost ~]$ sudo mkdir /opt/mount1/namenode-dir
[exam@localhost ~]$ sudo mkdir /opt/mount2/namenode-dir
```
#### 16. Сделать пользователя hdfs и группу hadoop владельцами этих директорий.
```bash
[exam@localhost ~]$ sudo chown hdfs:hadoop /opt/mount1/namenode-dir
[exam@localhost ~]$ ls -ld /opt/mount1/namenode-dir
drwxr-xr-x. 2 hdfs hadoop 4096 Feb 25 13:39 /opt/mount1/namenode-dir
[exam@localhost ~]$ sudo chown hdfs:hadoop /opt/mount2/namenode-dir
[exam@localhost ~]$ ls -ld /opt/mount1/namenode-dir
drwxr-xr-x. 2 hdfs hadoop 4096 Feb 25 13:39 /opt/mount1/namenode-dir
```
# Для VM2 (Charybdis) (шаги 17-20):
#### 17. После монтирования создать 2 директории для хранения файлов Datanode сервиса HDFS:
• /opt/mount1/datanode-dir  
• /opt/mount2/datanode-dir  
```bash
[exam@localhost ~]$ sudo mkdir /opt/mount1/datanode-dir
[exam@localhost ~]$ sudo mkdir /opt/mount2/datanode-dir
```
#### 18. Сделать пользователя hdfs и группу hadoop владельцами директорий из п.17.
```bash
[exam@localhost ~]$ sudo chown hdfs:hadoop /opt/mount1/datanode-dir
[exam@localhost ~]$ sudo chown hdfs:hadoop /opt/mount2/datanode-dir
[exam@localhost ~]$ ls -ld /opt/mount1
drwxr-xr-x. 4 root root 4096 Feb 25 13:57 /opt/mount1
[exam@localhost ~]$ ls -ld /opt/mount1/datanode-dir
drwxr-xr-x. 2 hdfs hadoop 4096 Feb 25 13:57 /opt/mount1/datanode-dir
[exam@localhost ~]$ ls -ld /opt/mount2/datanode-dir
drwxr-xr-x. 2 hdfs hadoop 4096 Feb 25 13:57 /opt/mount2/datanode-dir
```
#### 19. Создать дополнительные 4 директории для Nodemanager сервиса YARN:
• /opt/mount1/nodemanager-local-dir  
• /opt/mount2/nodemanager-local-dir  
• /opt/mount1/nodemanager-log-dir  
• /opt/mount2/nodemanager-log-dir  
```bash
[exam@localhost ~]$ sudo mkdir /opt/mount{1..2}/nodemanager-local-dir && sudo mkdir /opt/mount{1..2}/nodemanager-log-dir
```
#### 20. Сделать пользователя yarn и группу hadoop владельцами директорий из п.19.
```bash
[exam@localhost ~]$ sudo chown hdfs:hadoop /opt/mount{1..2}/nodemanager-local-dir && sudo chown hdfs:hadoop /opt/mount{1..2}/nodemanager-log-dir
[exam@localhost ~]$ sudo ls -ld /opt/mount{1..2}/nodemanager-local-dir && sudo ls -ld /opt/mount{1..2}/nodemanager-log-dir
drwxr-xr-x. 2 hdfs hadoop 4096 Feb 25 14:07 /opt/mount1/nodemanager-local-dir
drwxr-xr-x. 2 hdfs hadoop 4096 Feb 25 14:07 /opt/mount2/nodemanager-local-dir
drwxr-xr-x. 2 hdfs hadoop 4096 Feb 25 14:07 /opt/mount1/nodemanager-log-dir
drwxr-xr-x. 2 hdfs hadoop 4096 Feb 25 14:07 /opt/mount2/nodemanager-log-dir
```
# Для обеих машин:
#### 21. Настроить доступ по SSH, используя ключи для пользователя hadoop.
```bash
# Scylla (VM1)

[hadoop@localhost ~]$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/hadoop/.ssh/id_rsa): /home/hadoop/.ssh/hadoop_scylla_key
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/hadoop/.ssh/hadoop_scylla_key.
Your public key has been saved in /home/hadoop/.ssh/hadoop_scylla_key.pub.
The key fingerprint is:
SHA256:FIu0m10GpNA+rNgaJYH52/eDdJmWcYhTp6UZ2vIqBQ0 hadoop@localhost.localdomain
The key's randomart image is:
+---[RSA 2048]----+
| o  ....+        |
|o . Eo.+o+o      |
| . . =+=oOo      |
|  o o X=Bo.      |
|   B oo=S*       |
|  + + + B        |
|   o + *         |
|  . . o o        |
|     .   .       |
+----[SHA256]-----+
[hadoop@localhost ~]$ ssh-copy-id -i ~/.ssh/hadoop_scylla_key.pub hadoop@192.168.0.121
/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/hadoop/.ssh/hadoop_scylla_key.pub"
The authenticity of host '192.168.0.121 (192.168.0.121)' can't be established.
ECDSA key fingerprint is SHA256:vBPO74t/K41Hvy7/bbZXJYItqVEe+M+cNPfoek293P8.
ECDSA key fingerprint is MD5:06:3c:6f:fe:74:19:ef:93:a2:1a:70:c5:0a:b5:c2:8f.
Are you sure you want to continue connecting (yes/no)? yes
/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
hadoop@192.168.0.121's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'hadoop@192.168.0.121'"
and check to make sure that only the key(s) you wanted were added.

[hadoop@localhost ~]$ ssh -i /home/hadoop/.ssh/hadoop_scylla_key hadoop@192.168.0.121
Last login: Thu Feb 25 14:37:37 2021 from 192.168.0.120
[hadoop@localhost ~]$ exit


# Charybdis (VM2)
[hadoop@localhost ~]$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/hadoop/.ssh/id_rsa): /home/hadoop/.ssh/hadoop_key
Created directory '/home/hadoop/.ssh'.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/hadoop/.ssh/hadoop_key.
Your public key has been saved in /home/hadoop/.ssh/hadoop_key.pub.
The key fingerprint is:
SHA256:5vtUEBt9XmK1+5dr3XweUxCY0SJpXnvb2zi6YeFmJr0 hadoop@localhost.localdomain
The key's randomart image is:
+---[RSA 2048]----+
|          oo.=...|
|          ++* =.o|
|         ooo *.+ |
|          ... o..|
|        S   o. +.|
|       o   + .. =|
|        . o O  *B|
|         o * ooo@|
|        ... Eo.+o|
+----[SHA256]-----+

[hadoop@localhost ~]$ ssh-copy-id -i ~/.ssh/hadoop_key.pub hadoop@192.168.0.120
/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/hadoop/.ssh/hadoop_key.pub"
The authenticity of host '192.168.0.120 (192.168.0.120)' can't be established.
ECDSA key fingerprint is SHA256:4zD+E3eVNkf8KC2u3yoBowfXPnG1Sx7BT/xmYcJ7nCQ.
ECDSA key fingerprint is MD5:55:fb:bb:36:2d:d3:1d:eb:f5:9a:32:b9:73:e1:0a:ec.
Are you sure you want to continue connecting (yes/no)? yes
/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
hadoop@192.168.0.120's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'hadoop@192.168.0.120'"
and check to make sure that only the key(s) you wanted were added.

[hadoop@localhost ~]$ ssh -i /home/hadoop/.ssh/hadoop_key hadoop@192.168.0.120
Last login: Thu Feb 25 14:28:02 2021 from 192.168.0.121
[hadoop@localhost ~]$ exit
logout
Connection to 192.168.0.120 closed.


```
#### 22. Добавить VM1 и VM2 в /etc/hosts.
```bash
# Scylla
[exam@localhost ~]$ cat /etc/hosts
127.0.0.1   localhost scylla localhost4 localhost4.localdomain4
::1         localhost scylla localhost6 localhost6.localdomain6
192.168.0.121  charybdis
192.168.0.120  scylla

# Charybdis
[exam@localhost ~]$ cat /etc/hosts
127.0.0.1   localhost charybdis localhost4 localhost4.localdomain4
::1         localhost charybdis localhost6 localhost6.localdomain6
192.168.0.120  scylla
192.168.0.121  charybdis

```
#### 23. Скачать файлы по ссылкам в /usr/local/hadoop/current/etc/hadoop/{hadoop-env.sh,core-site.xml,hdfs-site.xml,yarn-site.xml}. При помощи sed заменить
заглушки на необходимые значения
```bash
# Скачать через Raw ссылку
[exam@scylla ~]$ sudo wget https://gist.githubusercontent.com/rdaadr/2f42f248f02aeda18105805493bb0e9b/raw/6303e424373b3459bcf3720b253c01373666fe7c/hadoop-env.sh -O /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/hadoop-env.sh
[exam@scylla ~]$ sudo wget https://gist.githubusercontent.com/rdaadr/64b9abd1700e15f04147ea48bc72b3c7/raw/2d416bf137cba81b107508153621ee548e2c877d/core-site.xml -O /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/core-site.xml
[exam@scylla ~]$ sudo wget https://gist.githubusercontent.com/rdaadr/2bedf24fd2721bad276e416b57d63e38/raw/640ee95adafa31a70869b54767104b826964af48/hdfs-site.xml -O /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/hdfs-site.xml
[exam@scylla ~]$ sudo wget https://gist.githubusercontent.com/Stupnikov-NA/ba87c0072cd51aa85c9ee6334cc99158/raw/bda0f760878d97213196d634be9b53a089e796ea/yarn-site.xml -O /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/yarn-site.xml

[exam@scylla ~]$ ls -la /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop
total 176
drwxrwsr-x. 3 hadoop hadoop  4096 Jan 28  2019 .
drwxrwsr-x. 3 hadoop hadoop    20 Jan 28  2019 ..
-rw-rwSr--. 1 hadoop hadoop  8260 Jan 28  2019 capacity-scheduler.xml
-rw-rwSr--. 1 hadoop hadoop  1335 Jan 28  2019 configuration.xsl
-rw-rwSr--. 1 hadoop hadoop  1940 Jan 28  2019 container-executor.cfg
-rw-rwSr--. 1 hadoop hadoop   908 Feb 27 16:39 core-site.xml
-rw-rwSr--. 1 hadoop hadoop  3999 Jan 28  2019 hadoop-env.cmd
-rw-rwSr--. 1 hadoop hadoop 15980 Feb 27 16:39 hadoop-env.sh
-rw-rwSr--. 1 hadoop hadoop  3323 Jan 28  2019 hadoop-metrics2.properties
-rw-rwSr--. 1 hadoop hadoop 11392 Jan 28  2019 hadoop-policy.xml
-rw-rwSr--. 1 hadoop hadoop  3414 Jan 28  2019 hadoop-user-functions.sh.example
-rw-rwSr--. 1 hadoop hadoop  1081 Feb 27 16:39 hdfs-site.xml
-rw-rwSr--. 1 hadoop hadoop  1484 Jan 28  2019 httpfs-env.sh
-rw-rwSr--. 1 hadoop hadoop  1657 Jan 28  2019 httpfs-log4j.properties
-rw-rwSr--. 1 hadoop hadoop    21 Jan 28  2019 httpfs-signature.secret
-rw-rwSr--. 1 hadoop hadoop   620 Jan 28  2019 httpfs-site.xml
-rw-rwSr--. 1 hadoop hadoop  3518 Jan 28  2019 kms-acls.xml
-rw-rwSr--. 1 hadoop hadoop  1351 Jan 28  2019 kms-env.sh
-rw-rwSr--. 1 hadoop hadoop  1747 Jan 28  2019 kms-log4j.properties
-rw-rwSr--. 1 hadoop hadoop   682 Jan 28  2019 kms-site.xml
-rw-rwSr--. 1 hadoop hadoop 13326 Jan 28  2019 log4j.properties
-rw-rwSr--. 1 hadoop hadoop   951 Jan 28  2019 mapred-env.cmd
-rw-rwSr--. 1 hadoop hadoop  1764 Jan 28  2019 mapred-env.sh
-rw-rwSr--. 1 hadoop hadoop  4113 Jan 28  2019 mapred-queues.xml.template
-rw-rwSr--. 1 hadoop hadoop   758 Jan 28  2019 mapred-site.xml
drwxrwsr-x. 2 hadoop hadoop    24 Jan 28  2019 shellprofile.d
-rw-rwSr--. 1 hadoop hadoop  2316 Jan 28  2019 ssl-client.xml.example
-rw-rwSr--. 1 hadoop hadoop  2697 Jan 28  2019 ssl-server.xml.example
-rw-rwSr--. 1 hadoop hadoop  2642 Jan 28  2019 user_ec_policies.xml.template
-rw-rwSr--. 1 hadoop hadoop    10 Jan 28  2019 workers
-rw-rwSr--. 1 hadoop hadoop  2250 Jan 28  2019 yarn-env.cmd
-rw-rwSr--. 1 hadoop hadoop  6056 Jan 28  2019 yarn-env.sh
-rw-rwSr--. 1 hadoop hadoop  2591 Jan 28  2019 yarnservice-log4j.properties
-rw-rwSr--. 1 hadoop hadoop  1499 Feb 27 16:39 yarn-site.xml

```
• hadoop-env.sh (https://gist.github.com/rdaadr/2f42f248f02aeda18105805493bb0e9b)  
Необходимо определить переменные JAVA_HOME (путь до директории с OpenJDK8,  
установленную в п.3), HADOOP_HOME (необходимо указать путь к симлинку из п.6) и  
HADOOP_HEAPSIZE_MAX (укажите значение в 512M)  
```bash
[exam@scylla ~]$ sudo sed -i '/^export JAVA_HOME/s/=.*$/=\/usr\/lib\/jvm\/java-1\.8\.0-openjdk/' /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/hadoop-env.sh
[exam@scylla ~]$ sudo sed -i '/^export HADOOP_HOME/s/=.*$/=\/usr\/local\/hadoop\/current\/hadoop-3\.1\.2/' /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/hadoop-env.sh       [exam@scylla ~]$ sudo sed -i '/^export HADOOP_HEAPSIZE_MAX/s/=.*$/=512M/' /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/hadoop-env.sh 
```
• core-site.xml (https://gist.github.com/rdaadr/64b9abd1700e15f04147ea48bc72b3c7)  
Необходимо указать имя хоста, на котором будет запущена HDFS Namenode (VM1)  
```bash
# Test
[exam@scylla ~]$ sed -E 's/([\%])\w+[\%]/scylla/g;t;d' /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/core-site.xml
[exam@scylla ~]$ sudo sed -Ei 's/([\%])\w+[\%]/scylla/g' /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/core-site.xml
```
• hdfs-site.xml (https://gist.github.com/rdaadr/2bedf24fd2721bad276e416b57d63e38)  
Необходимо указать директории namenode-dir, а также datanode-dir, каждый раз через  
запятую (например, /opt/mount1/namenode-dir,/opt/mount2/namenode-dir)  
```bash
• /opt/mount1/namenode-dir  
• /opt/mount2/namenode-dir 
• /opt/mount1/datanode-dir  
• /opt/mount2/datanode-dir
[exam@scylla ~]$ sudo sed -Ei 's/([\%])DATANODE_DIRS[\%]/\/opt\/mount1\/datanode-dir\,\/opt\/mount2\/datanode-dir/g ; s/([\%])NAMENODE_DIRS[\%]/\/opt\/mount1\/namenode-dir\,\/opt\/mount2\/namenode-dir/g' /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/hdfs-site.xml

```
• yarn-site.xml (https://gist.github.com/Stupnikov-NA/ba87c0072cd51aa85c9ee6334cc99158)  
Необходимо подставить имя хоста, на котором будет развернут YARN Resource Manager (VM1), а  
также пути до директорий nodemanager-local-dir и nodemanager-log-dir (если  
необходимо указать несколько директорий, то необходимо их разделить запятыми)  
```bash
scylla
• /opt/mount1/nodemanager-local-dir  
• /opt/mount2/nodemanager-local-dir  
• /opt/mount1/nodemanager-log-dir  
• /opt/mount2/nodemanager-log-dir 
YARN_RESOURCE_MANAGER_HOSTNAME
NODE_MANAGER_LOCAL_DIR
%NODE_MANAGER_LOG_DIR%
[exam@scylla ~]$ sudo sed -Ei 's/([\%])YARN_RESOURCE_MANAGER_HOSTNAME[\%]/scylla/g ; s/([\%])NODE_MANAGER_LOCAL_DIR[\%]/\/opt\/mount1\/nodemanager-local-dir\,\/opt\/mount2\/nodemanager-local-dir/g ; s/([\%])NODE_MANAGER_LOG_DIR[\%]/\/opt\/mount1\/nodemanager-log-dir\,\/opt\/mount2\/nodemanager-log-dir/g' /usr/local/hadoop/current/hadoop-3.1.2/etc/hadoop/yarn-site.xml
```
#### 24. Задать переменную окружения HADOOP_HOME через /etc/profile
```bash
[exam@scylla ~]$ sudo cat /etc/profile | grep HADOOP
HADOOP_HOME=/opt/hadoop-3.1.2
export HADOOP_HOME

# Обновить и тест
[exam@scylla ~]$ source /etc/profile
[exam@scylla ~]$ echo $HADOOP_HOME
/opt/hadoop-3.1.2
```
# Для VM1 (шаги 25-26):
#### 25. Произвести форматирование HDFS (от имени пользователя hdfs):
• $HADOOP_HOME/bin/hdfs namenode -format cluster1  
```bash
# Была ошибка
[hdfs@scylla ~]$ $HADOOP_HOME/bin/hdfs namenode -format cluster1
ERROR: JAVA_HOME is not set and could not be found.

# Добавили сюда путь. 
[exam@scylla ~]$ sudo cat /etc/profile | grep JAVA
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
export PATH=$JAVA_HOME/bin:$PATH

# Добавили права
[exam@scylla ~]$ sudo chmod g+s -R /opt/hadoop-3.1.2
[exam@scylla ~]$ ls -ld /opt/hadoop-3.1.2
drwxr-sr-x. 9 hadoop hadoop 149 Jan 28  2019 /opt/hadoop-3.1.2
[exam@scylla ~]$ sudo chmod g+w -R /opt/hadoop-3.1.2

[exam@scylla ~]$ ls -ld /opt/hadoop-3.1.2
drwxrwsr-x. 9 hadoop hadoop 149 Jan 28  2019 /opt/hadoop-3.1.2

# Пуск
[hdfs@scylla ~]$ $HADOOP_HOME/bin/hdfs namenode -format cluster1
WARNING: /opt/hadoop-3.1.2/logs does not exist. Creating.
2021-02-27 15:47:30,563 INFO namenode.NameNode: STARTUP_MSG:
/************************************************************
STARTUP_MSG: Starting NameNode
STARTUP_MSG:   host = localhost/127.0.0.1
STARTUP_MSG:   args = [-format, cluster1]
STARTUP_MSG:   version = 3.1.2
.....
2021-02-27 15:47:31,514 INFO common.Storage: Storage directory /tmp/hadoop-hdfs/dfs/name has been successfully formatted.
2021-02-27 15:47:31,519 INFO namenode.FSImageFormatProtobuf: Saving image file /tmp/hadoop-hdfs/dfs/name/current/fsimage.ckpt_0000000000000000000 using no compression
2021-02-27 15:47:31,584 INFO namenode.FSImageFormatProtobuf: Image file /tmp/hadoop-hdfs/dfs/name/current/fsimage.ckpt_0000000000000000000 of size 391 bytes saved in 0 seconds .
2021-02-27 15:47:31,596 INFO namenode.NNStorageRetentionManager: Going to retain 1 images with txid >= 0
2021-02-27 15:47:31,599 INFO namenode.NameNode: SHUTDOWN_MSG:
/************************************************************
SHUTDOWN_MSG: Shutting down NameNode at localhost/127.0.0.1
************************************************************/
```
#### 26. Запустить демоны сервисов Hadoop:
Для запуска Namenode (от имени пользователя hdfs):  
• $HADOOP_HOME/bin/hdfs --daemon start namenode  
```bash
[hdfs@scylla ~]$ $HADOOP_HOME/bin/hdfs --daemon start namenode
[hdfs@scylla ~]$ ps -ef | grep namenode
hdfs      2487  2345  0 16:10 pts/0    00:00:00 grep --color=auto namenode
```
Для запуска Resource Manager (от имени пользователя yarn):  
• $HADOOP_HOME/bin/yarn --daemon start resourcemanager  
```bash
[exam@scylla ~]$ sudo chmod g+w -R /opt/hadoop-3.1.2
[exam@scylla ~]$ sudo chgrp -R hadoop /opt/hadoop-3.1.2

[yarn@scylla ~]$ $HADOOP_HOME/bin/yarn --daemon start resourcemanager
[yarn@scylla ~]$ ps -ef | grep resourcemanager
yarn      2956     1 11 16:16 pts/0    00:00:03 /usr/lib/jvm/java-1.8.0-openjdk/bin/java -Dproc_resourcemanager -Djava.net.preferIPv4Stack=true -Dservice.libdir=/opt/hadoop-3.1.2/share/hadoop/yarn,/opt/hadoop-3.1.2/share/hadoop/yarn/lib,/opt/hadoop-3.1.2/share/hadoop/hdfs,/opt/hadoop-3.1.2/share/hadoop/hdfs/lib,/opt/hadoop-3.1.2/share/hadoop/common,/opt/hadoop-3.1.2/share/hadoop/common/lib -Dyarn.log.dir=/opt/hadoop-3.1.2/logs -Dyarn.log.file=hadoop-yarn-resourcemanager-scylla.log -Dyarn.home.dir=/opt/hadoop-3.1.2 -Dyarn.root.logger=INFO,console -Djava.library.path=/opt/hadoop-3.1.2/lib/native -Dhadoop.log.dir=/opt/hadoop-3.1.2/logs -Dhadoop.log.file=hadoop-yarn-resourcemanager-scylla.log -Dhadoop.home.dir=/opt/hadoop-3.1.2 -Dhadoop.id.str=yarn -Dhadoop.root.logger=INFO,RFA -Dhadoop.policy.file=hadoop-policy.xml -Dhadoop.security.logger=INFO,NullAppender org.apache.hadoop.yarn.server.resourcemanager.ResourceManager
yarn      3175  2901  0 16:16 pts/0    00:00:00 grep --color=auto resourcemanager
```
# Для VM2 Charybdis (шаг 27):
#### 27. Запустить демоны сервисов:
Для запуска Datanode (от имени hdfs):  
• $HADOOP_HOME/bin/hdfs --daemon start datanode  
```bash
[hdfs@charybdis ~]$ $HADOOP_HOME/bin/hdfs --daemon start datanode
WARNING: /usr/local/hadoop/current/hadoop-3.1.2/logs does not exist. Creating.
[hdfs@charybdis ~]$ ps -ef | grep datanode
hdfs      1861     1  8 17:02 pts/0    00:00:02 /usr/lib/jvm/java-1.8.0-openjdk/bin/java -Dproc_datanode -Djava.net.preferIPv4Stack=true -Dhadoop.security.logger=ERROR,RFAS -Dyarn.log.dir=/usr/local/hadoop/current/hadoop-3.1.2/logs -Dyarn.log.file=hadoop-hdfs-datanode-charybdis.log -Dyarn.home.dir=/usr/local/hadoop/current/hadoop-3.1.2 -Dyarn.root.logger=INFO,console -Djava.library.path=/usr/local/hadoop/current/hadoop-3.1.2/lib/native -Xmx512M -Dhadoop.log.dir=/usr/local/hadoop/current/hadoop-3.1.2/logs -Dhadoop.log.file=hadoop-hdfs-datanode-charybdis.log -Dhadoop.home.dir=/usr/local/hadoop/current/hadoop-3.1.2 -Dhadoop.id.str=hdfs -Dhadoop.root.logger=INFO,RFA -Dhadoop.policy.file=hadoop-policy.xml org.apache.hadoop.hdfs.server.datanode.DataNode
hdfs      1911  1806  0 17:02 pts/0    00:00:00 grep --color=auto datanode
```
Для запуска Node Manager (от имени yarn):  
• $HADOOP_HOME/bin/yarn --daemon start nodemanager  
```bash
[yarn@charybdis ~]$ $HADOOP_HOME/bin/yarn --daemon start nodemanager
[yarn@charybdis ~]$ ps -ef | grep nodemanager
yarn      2035     1 10 17:04 pts/0    00:00:02 /usr/lib/jvm/java-1.8.0-openjdk/bin/java -Dproc_nodemanager -Djava.net.preferIPv4Stack=true -Dyarn.log.dir=/usr/local/hadoop/current/hadoop-3.1.2/logs -Dyarn.log.file=hadoop-yarn-nodemanager-charybdis.log -Dyarn.home.dir=/usr/local/hadoop/current/hadoop-3.1.2 -Dyarn.root.logger=INFO,console -Djava.library.path=/usr/local/hadoop/current/hadoop-3.1.2/lib/native -Xmx512M -Dhadoop.log.dir=/usr/local/hadoop/current/hadoop-3.1.2/logs -Dhadoop.log.file=hadoop-yarn-nodemanager-charybdis.log -Dhadoop.home.dir=/usr/local/hadoop/current/hadoop-3.1.2 -Dhadoop.id.str=yarn -Dhadoop.root.logger=INFO,RFA -Dhadoop.policy.file=hadoop-policy.xml -Dhadoop.security.logger=INFO,NullAppender org.apache.hadoop.yarn.server.nodemanager.NodeManager
yarn      2116  1980  0 17:04 pts/0    00:00:00 grep --color=auto nodemanager
```
# Для VM1 и VM2
#### 28. Проверить доступность Web-интефейсов HDFS Namenode и YARN Resource Manager по портам
9870 и 8088 соответственно (VM1). << порты должны быть доступны с хостовой системы.  
```bash
[exam@scylla ~]$ sudo iptables -F
[exam@scylla ~]$ sudo systemctl stop firewalld
[exam@scylla ~]$ sudo systemctl disable firewalld
[exam@scylla ~]$ sudo systemctl enable iptables
[exam@scylla ~]$ sudo iptables -I INPUT -p tcp --dport 8088 -m state --state NEW -j ACCEPT
[exam@scylla ~]$ sudo iptables -I INPUT -p tcp --dport 9870 -m state --state NEW -j ACCEPT

[exam@scylla ~]$ sudo service iptables save
iptables: Saving firewall rules to /etc/sysconfig/iptables:[  OK  ]
[exam@scylla ~]$ systemctl restart iptables

[exam@scylla ~]$ sudo iptables -L -v -n
Chain INPUT (policy ACCEPT 218 packets, 13509 bytes)
 pkts bytes target     prot opt in     out     source               destination
    2    88 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:63000 state NEW
   28  1648 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:9870 state NEW
    0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:8088 state NEW

Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 237 packets, 16996 bytes)
 pkts bytes target     prot opt in     out     source               destination
    0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:8088 state NEW
    0     0 ACCEPT     tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:9870 state NEW



# Test
[exam@charybdis ~]$ sudo nmap -sV -PN -p 9870 scylla

Starting Nmap 6.40 ( http://nmap.org ) at 2021-02-27 17:48 EST
Nmap scan report for scylla (192.168.0.120)
Host is up (0.00027s latency).
PORT     STATE SERVICE VERSION
9870/tcp open  unknown
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at http://www.insecure.org/cgi-bin/servicefp-submit.cgi :
SF-Port9870-TCP:V=6.40%I=7%D=2/27%Time=603ACC55%P=x86_64-redhat-linux-gnu%
SF:r(GetRequest,5F3,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Sat,\x2027\x20Feb\
SF:x202021\x2022:48:53\x20GMT\r\nCache-Control:\x20no-cache\r\nExpires:\x2
SF:0Sat,\x2027\x20Feb\x202021\x2022:48:53\x20GMT\r\nDate:\x20Sat,\x2027\x2
SF:0Feb\x202021\x2022:48:53\x20GMT\r\nPragma:\x20no-cache\r\nContent-Type:
SF:\x20text/html\r\nX-FRAME-OPTIONS:\x20SAMEORIGIN\r\nExpires:\x20Sat,\x20
SF:27\x20Feb\x202021\x2022:48:53\x20GMT\r\nDate:\x20Sat,\x2027\x20Feb\x202
SF:021\x2022:48:53\x20GMT\r\nPragma:\x20no-cache\r\nX-FRAME-OPTIONS:\x20SA
SF:MEORIGIN\r\nLast-Modified:\x20Tue,\x2029\x20Jan\x202019\x2003:35:58\x20
SF:GMT\r\nAccept-Ranges:\x20bytes\r\nContent-Length:\x201079\r\n\r\n<!--\n
SF:\x20\x20\x20Licensed\x20to\x20the\x20Apache\x20Software\x20Foundation\x
SF:20\(ASF\)\x20under\x20one\x20or\x20more\n\x20\x20\x20contributor\x20lic
SF:ense\x20agreements\.\x20\x20See\x20the\x20NOTICE\x20file\x20distributed
SF:\x20with\n\x20\x20\x20this\x20work\x20for\x20additional\x20information\
SF:x20regarding\x20copyright\x20ownership\.\n\x20\x20\x20The\x20ASF\x20lic
SF:enses\x20this\x20file\x20to\x20You\x20under\x20the\x20Apache\x20License
SF:,\x20Version\x202\.0\n\x20\x20\x20\(the\x20\"License\"\);\x20you\x20may
SF:\x20not\x20use\x20this\x20file\x20except\x20in\x20compliance\x20with\n\
SF:x20\x20\x20the\x20License\.\x20\x20You\x20may\x20obtain\x20a\x20copy\x2
SF:0of\x20the\x20License\x20at\n\n\x20\x20\x20\x20\x20\x20\x20http://www\.
SF:apache\.org/lic")%r(HTTPOptions,126,"HTTP/1\.1\x20200\x20OK\r\nDate:\x2
SF:0Sat,\x2027\x20Feb\x202021\x2022:48:53\x20GMT\r\nCache-Control:\x20no-c
SF:ache\r\nExpires:\x20Sat,\x2027\x20Feb\x202021\x2022:48:53\x20GMT\r\nDat
SF:e:\x20Sat,\x2027\x20Feb\x202021\x2022:48:53\x20GMT\r\nPragma:\x20no-cac
SF:he\r\nContent-Type:\x20text/plain;charset=utf-8\r\nX-FRAME-OPTIONS:\x20
SF:SAMEORIGIN\r\nAllow:\x20GET,HEAD,POST,OPTIONS\r\nContent-Length:\x200\r
SF:\n\r\n")%r(RTSPRequest,46,"HTTP/1\.1\x20400\x20Unknown\x20Version\r\nCo
SF:ntent-Length:\x200\r\nConnection:\x20close\r\n\r\n")%r(RPCCheck,43,"HTT
SF:P/1\.1\x20400\x20Bad\x20preamble\r\nContent-Length:\x200\r\nConnection:
SF:\x20close\r\n\r\n")%r(DNSVersionBindReq,4C,"HTTP/1\.1\x20400\x20Illegal
SF:\x20character\x200x0\r\nContent-Length:\x200\r\nConnection:\x20close\r\
SF:n\r\n");
MAC Address: 00:15:5D:00:6B:00 (Microsoft)

Service detection performed. Please report any incorrect results at http://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.53 seconds

[exam@charybdis ~]$ sudo nmap -sV -PN -p 8088 scylla

Starting Nmap 6.40 ( http://nmap.org ) at 2021-02-27 17:49 EST
Nmap scan report for scylla (192.168.0.120)
Host is up (0.00026s latency).
PORT     STATE  SERVICE    VERSION
8088/tcp closed radan-http
MAC Address: 00:15:5D:00:6B:00 (Microsoft)

Service detection performed. Please report any incorrect results at http://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.47 seconds


```
#### 29. Настроить управление запуском каждого компонента Hadoop при помощи systemd (используя
юниты-сервисы).
```bash
[exam@scylla ~]$ sudo cat $HADOOP_HOME/sbin/hdfs_start.sh
#!/bin/bash

$HADOOP_HOME/bin/hdfs --daemon start namenode

[exam@scylla ~]$ sudo cat $HADOOP_HOME/sbin/hdfs_stop.sh
#!/bin/bash

$HADOOP_HOME/bin/hdfs --daemon stop namenode

[exam@scylla ~]$ sudo cat /etc/systemd/system/hdfs-daemon.service
[Unit]
Description=Hdfs

[Service]
User=hdfs
Group=hadoop
ExecStart=/bin/bash $HADOOP_HOME/sbin/hdfs_start.sh
ExecStop=/bin/bash $HADOOP_HOME/sbin/hdfs_stop.sh

[Install]
WantedBy=multi-user.target
```
```bash
[exam@scylla ~]$ sudo cat $HADOOP_HOME/sbin/yarn_start.sh
#!/bin/bash

$HADOOP_HOME/bin/yarn --daemon start resourcemanager
[exam@scylla ~]$ sudo cat $HADOOP_HOME/sbin/yarn_stop.sh
#!/bin/bash

$HADOOP_HOME/bin/yarn --daemon stop resourcemanager

[exam@scylla ~]$ sudo cat /etc/systemd/system/yarn-daemon.service
[Unit]
Description=Hdfs

[Service]
User=yarn
Group=hadoop
ExecStart=/bin/bash $HADOOP_HOME/sbin/yarn_start.sh
ExecStop=/bin/bash $HADOOP_HOME/sbin/yarn_stop.sh

[Install]
WantedBy=multi-user.target

```
```bash
[exam@charybdis ~]$ sudo cat $HADOOP_HOME/sbin/hdfs_start.sh
#!/bin/bash

$HADOOP_HOME/bin/hdfs --daemon start datanode

[exam@charybdis ~]$ sudo cat $HADOOP_HOME/sbin/hdfs_stop.sh
#!/bin/bash

$HADOOP_HOME/bin/hdfs --daemon stop datanode

[exam@charybdis ~]$ sudo cat $HADOOP_HOME/sbin/hdfs_stop.sh
#!/bin/bash

$HADOOP_HOME/bin/hdfs --daemon stop datanode

[exam@charybdis ~]$ sudo cat /etc/systemd/system/hdfs-daemon.service
[Unit]
Description=Hdfs

[Service]
User=hdfs
Group=hadoop
ExecStart=/bin/bash $HADOOP_HOME/sbin/hdfs_start.sh
ExecStop=/bin/bash $HADOOP_HOME/sbin/hdfs_stop.sh

[Install]
WantedBy=multi-user.target
```
```bash
[exam@charybdis ~]$ sudo cat $HADOOP_HOME/sbin/yarn_start.sh
#!/bin/bash

$HADOOP_HOME/bin/yarn --daemon start nodemanager
[exam@charybdis ~]$ sudo cat $HADOOP_HOME/sbin/yarn_stop.sh
#!/bin/bash

$HADOOP_HOME/bin/yarn --daemon stop nodemanager

[exam@charybdis ~]$ sudo cat /etc/systemd/system/yarn-daemon.service
[Unit]
Description=Hdfs

[Service]
User=yarn
Group=hadoop
ExecStart=/bin/bash $HADOOP_HOME/sbin/yarn_start.sh
ExecStop=/bin/bash $HADOOP_HOME/sbin/yarn_stop.sh

[Install]
WantedBy=multi-user.target
```
