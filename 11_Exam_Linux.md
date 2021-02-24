# Задача
Установить, настроить и запустить Hadoop Сore в минимальной конфигурации. Для этого  
потребуется подготовить 2 виртуальные машины: VM1 - headnode; VM2 - worker. Понимание  
принципов работы Hadoop и его компонентов для успешной сдачи задания не требуется.  
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

# 11. В каждой из групп из п.10 создать логический том LVM размером 100% группы.
# 12. На каждом логическом томе LVM создать файловую систему ext4.
# 13. Создать директории и использовать их в качестве точек монтирования файловых систем из
п.12:
• /opt/mount1
• /opt/mount2
# 14. Настроить систему так, чтобы монтирование происходило автоматически при запуске системы.
Произвести монтирование новых файловых систем.
