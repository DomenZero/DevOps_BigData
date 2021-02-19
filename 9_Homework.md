# DD
#### 1. Imagine you was asked to add new partition to your host for backup purposes. To simulate appearance of new physical disk in your server, please create new disk in Virtual Box (5 GB) and attach it to your virtual machine.
Also imagine your system started experiencing RAM leak in one of the applications, thus while developers try to debug and fix it, you need to mitigate OutOfMemory errors; you will do it by adding some swap space.
/dev/sdc - 5GB disk, that you just attached to the VM (in your case it may appear as /dev/sdb, /dev/sdc or other, it doesn't matter)

```bash
[root@mitnik ~]# sudo fdisk -l

Disk /dev/sda: 21.5 GB, 21474836480 bytes, 41943040 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk label type: dos
Disk identifier: 0x000702b2

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048     2099199     1048576   83  Linux
/dev/sda2         2099200    41943039    19921920   8e  Linux LVM

Disk /dev/sdb: 5368 MB, 5368709120 bytes, 10485760 sectors
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

[root@mitnik ~]# sudo parted /dev/sdb
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

```
#### 1.1. Create a 2GB   !!! GPT !!!   partition on /dev/sdc of type "Linux filesystem" (means all the following partitions created in the following steps on /dev/sdc will be GPT as well)
```bash
# Create
[root@mitnik ~]# sudo parted /dev/sdb
GNU Parted 3.1
Using /dev/sdb
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) mklabel gpt
Warning: The existing disk label on /dev/sdb will be destroyed and all data on
this disk will be lost. Do you want to continue?
Yes/No? yes
(parted) print
Model: Msft Virtual Disk (scsi)
Disk /dev/sdb: 5369MB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags:

Number  Start  End  Size  File system  Name  Flags

(parted) mkpart Linux_filesystem
File system type?  [ext2]? ext4
Start? 0%
End? 45%

# Resize
(parted) resizepart
Partition number? 1
End?  [2002MB]? 2001
Warning: Shrinking a partition can cause data loss, are you sure you want to
continue?
Yes/No? yes
(parted) print
Model: Msft Virtual Disk (scsi)
Disk /dev/sdb: 5369MB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name              Flags
 1      1049kB  2001MB  2000MB               Linux_filesystem

```
#### 1.2. Create a 512MB partition on /dev/sdc of type "Linux swap"
```bash
(parted) mkpart Linux_swap
File system type?  [ext2]? ext4
Start? 2002MB
End? 2512MB
(parted) print
Model: Msft Virtual Disk (scsi)
Disk /dev/sdb: 5369MB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name              Flags
 1      1049kB  2001MB  2000MB               Linux_filesystem
 2      2002MB  2512MB  511MB                Linux_swap

(parted) print
Model: Msft Virtual Disk (scsi)
Disk /dev/sdb: 5369MB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name              Flags
 1      1049kB  2001MB  2000MB               Linux_filesystem
 2      2002MB  2514MB  512MB                Linux_swap

```
#### 1.3. Format the 2GB partition with an XFS file system
```bash
[root@mitnik ~]# mkfs -t xfs /dev/sdb1
Discarding blocks...Done.
meta-data=/dev/sdb1              isize=512    agcount=4, agsize=122068 blks
         =                       sectsz=4096  attr=2, projid32bit=1
         =                       crc=1        finobt=0, sparse=0
data     =                       bsize=4096   blocks=488269, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0 ftype=1
log      =internal log           bsize=4096   blocks=2560, version=2
         =                       sectsz=4096  sunit=1 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
[root@mitnik ~]# sudo parted /dev/sdb
GNU Parted 3.1
Using /dev/sdb
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) print
Model: Msft Virtual Disk (scsi)
Disk /dev/sdb: 5369MB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name              Flags
 1      1049kB  2001MB  2000MB  xfs          Linux_filesystem
 2      2002MB  2514MB  512MB                Linux_swap

```
#### 1.4. Initialize 512MB partition as swap space
```bash
[root@mitnik ~]# mkswap /dev/sdb2
Setting up swapspace version 1, size = 500256 KiB
no label, UUID=1e73facc-bee3-43e1-8944-b947eeef1421
[root@mitnik ~]# lsblk -f
NAME   FSTYPE    LABEL UUID                                   MOUNTPOINT
fd0
sda
├─sda1 xfs             c2d48651-fb36-4d59-89f6-133f0a7fe8d7   /boot
└─sda2 LVM2_memb       la12fb-34s9-6Lxb-v4w5-0we1-cQ0O-dFf370
  ├─centos-root
       xfs             0fca2a58-afb3-43b1-83a3-71e0c974f37b   /
  └─centos-swap
       swap            31e20c07-091a-4042-a061-b8b0a1dd89c6   [SWAP]
sdb
├─sdb1 xfs             fc9d68ce-6fa4-4c40-90f2-4ecbed65bfd7   /backup
└─sdb2 swap            1e73facc-bee3-43e1-8944-b947eeef1421
sr0

```
#### 1.5. Configure the newly created XFS file system to persistently mount at /backup
```bash
[root@mitnik ~]# mount /dev/sdb1 /backup
[root@mitnik ~]# df -h
Filesystem               Size  Used Avail Use% Mounted on
devtmpfs                 453M     0  453M   0% /dev
tmpfs                    464M     0  464M   0% /dev/shm
tmpfs                    464M  6.8M  457M   2% /run
tmpfs                    464M     0  464M   0% /sys/fs/cgroup
/dev/mapper/centos-root   17G  1.8G   16G  11% /
/dev/sda1               1014M  167M  848M  17% /boot
tmpfs                     93M     0   93M   0% /run/user/0
/dev/sdb1                1.9G   33M  1.9G   2% /backup
```
#### 1.6. Configure the newly created swap space to be enabled at boot
```bash
[root@mitnik ~]# blkid /dev/sdb1
/dev/sdb1: UUID="fc9d68ce-6fa4-4c40-90f2-4ecbed65bfd7" TYPE="xfs" PARTLABEL="Linux_filesystem" PARTUUID="c5f322db-b47d-4fe1-b6a6-7ca2937065ca"
[root@mitnik ~]# blkid /dev/sdb2
/dev/sdb2: UUID="1e73facc-bee3-43e1-8944-b947eeef1421" TYPE="swap" PARTLABEL="Linux_swap" PARTUUID="27f0e504-2c28-4677-a28f-90e813d7d142"
[root@mitnik ~]# vi /etc/fstab
....
UUID="fc9d68ce-6fa4-4c40-90f2-4ecbed65bfd7"             /backup        xfs      defaults        0 0
UUID="1e73facc-bee3-43e1-8944-b947eeef1421"             swap           swap     defaults        0 0

```
#### 1.7. Reboot your host and verify that /dev/sdc1 is mounted at /backup and that your swap partition  (/dev/sdc2) is enabled
```bash
[root@mitnik ~]# df -h
Filesystem               Size  Used Avail Use% Mounted on
devtmpfs                 453M     0  453M   0% /dev
tmpfs                    464M     0  464M   0% /dev/shm
tmpfs                    464M  6.8M  457M   2% /run
tmpfs                    464M     0  464M   0% /sys/fs/cgroup
/dev/mapper/centos-root   17G  1.8G   16G  11% /
/dev/sda1               1014M  167M  848M  17% /boot
/dev/sdb1                1.9G   33M  1.9G   2% /backup
tmpfs                     93M     0   93M   0% /run/user/0
[root@mitnik ~]# swapon -s
Filename                                Type            Size    Used    Priority
/dev/sdb2                               partition       500256  0       -2
/dev/dm-1                               partition       2097148 0       -3
```

# LVM
#### 2. LVM. Imagine you're running out of space on your root device. As we found out during the lesson default CentOS installation should already have LVM, means you can easily extend size of your root device. So what are you waiting for? Just do it!
#### 2.1. Create 2GB partition on /dev/sdc of type "Linux LVM"
```bash
(parted) mkpart Linux_LVM
File system type?  [ext2]? ext4
Start? 2515MB
End? 4515MB
Warning: The resulting partition is not properly aligned for best performance.
Ignore/Cancel? i
(parted) print
Model: Msft Virtual Disk (scsi)
Disk /dev/sdb: 5369MB
Sector size (logical/physical): 512B/4096B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system     Name              Flags
 1      1049kB  2001MB  2000MB  xfs             Linux_filesystem
 2      2002MB  2514MB  512MB   linux-swap(v1)  Linux_swap
 3      2515MB  4515MB  2000MB                  Linux_LVM
 
(parted) set 3 lvm on
```
#### 2.2. Initialize the partition as a physical volume (PV)
```bash
[root@mitnik ~]# pvcreate /dev/sdb3
  Physical volume "/dev/sdb3" successfully created.
  
[root@mitnik ~]# pvs
  PV         VG     Fmt  Attr PSize   PFree
  /dev/sda2  centos lvm2 a--  <19.00g    0
  /dev/sdb3         lvm2 ---    1.86g 1.86g

```
#### 2.3. Extend the volume group (VG) of your root device using your newly created PV
```bash
[root@mitnik ~]# pvcreate /dev/sdb3
  Can't initialize physical volume "/dev/sdb3" of volume group "vg_new" without -ff
  /dev/sdb3: physical volume not initialized.
[root@mitnik ~]# pvcreate -ff /dev/sdb3
Really INITIALIZE physical volume "/dev/sdb3" of volume group "vg_new" [y/n]? y
  WARNING: Forcing physical volume creation on /dev/sdb3 of volume group "vg_new"
  Physical volume "/dev/sdb3" successfully created.
[root@mitnik ~]# pvs
  PV         VG     Fmt  Attr PSize   PFree
  /dev/sda2  centos lvm2 a--  <19.00g    0
  /dev/sdb3         lvm2 ---    1.86g 1.86g
[root@mitnik ~]# vgextend centos /dev/sdb3
  Volume group "centos" successfully extended
[root@mitnik ~]# pvs
  PV         VG     Fmt  Attr PSize   PFree
  /dev/sda2  centos lvm2 a--  <19.00g     0
  /dev/sdb3  centos lvm2 a--   <1.86g <1.86g
 [root@mitnik ~]# vgs
  VG     #PV #LV #SN Attr   VSize   VFree
  centos   2   2   0 wz--n- <20.86g <1.86g

```
#### 2.4. , leaving other 1GB unassigned
```bash
# BEFORE CHANGES 
[root@mitnik ~]# lvdisplay
  --- Logical volume ---
  LV Path                /dev/centos/swap
  LV Name                swap
  VG Name                centos
  LV UUID                YvFxTq-t4Pe-se0j-tuVY-mBPW-f7RU-5AAQ1c
  LV Write Access        read/write
  LV Creation host, time localhost, 2021-01-11 22:11:49 +0300
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
  LV UUID                VjdLT2-KQcq-46wv-tytr-roM6-abUD-YEJwLk
  LV Write Access        read/write
  LV Creation host, time localhost, 2021-01-11 22:11:50 +0300
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
```bash
[root@mitnik ~]# vgdisplay
  --- Volume group ---
  VG Name               centos
  System ID
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  4
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               <20.86 GiB
  PE Size               4.00 MiB
  Total PE              5339
  Alloc PE / Size       4863 / <19.00 GiB
  Free  PE / Size       476 / <1.86 GiB
  VG UUID               mMGVhz-V5GM-G5SZ-ENQ1-Ad00-P2DG-o0SFXl

[root@mitnik ~]# lvextend -L+1G /dev/centos/root
  Size of logical volume centos/root changed from <17.00 GiB (4351 extents) to <18.00 GiB (4607 extents).
  Logical volume centos/root successfully resized.


```
#### 2.5. Check current disk space usage of your root device
```bash
[root@mitnik ~]# lvdisplay
  --- Logical volume ---
  LV Path                /dev/centos/swap
  LV Name                swap
  VG Name                centos
  LV UUID                YvFxTq-t4Pe-se0j-tuVY-mBPW-f7RU-5AAQ1c
  LV Write Access        read/write
  LV Creation host, time localhost, 2021-01-11 22:11:49 +0300
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
  LV UUID                VjdLT2-KQcq-46wv-tytr-roM6-abUD-YEJwLk
  LV Write Access        read/write
  LV Creation host, time localhost, 2021-01-11 22:11:50 +0300
  LV Status              available
  # open                 1
  LV Size                <18.00 GiB
  Current LE             4607
  Segments               2
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           253:0

```
#### 2.6. Extend your root device filesystem to be able to use additional free space of root LV
```bash
[root@mitnik ~]# resize2fs /dev/centos/root


[root@mitnik ~]# lvextend -i1 -l+100%FREE /dev/centos/root
  Size of logical volume centos/root changed from <18.00 GiB (4607 extents) to <18.86 GiB (4827 extents).
  Logical volume centos/root successfully resized.


```
#### 2.7. Verify that after reboot your root device is still 1GB bigger than at 2.5.
```bash
[root@mitnik ~]# lvdisplay
  --- Logical volume ---
  LV Path                /dev/centos/swap
  LV Name                swap
  VG Name                centos
  LV UUID                YvFxTq-t4Pe-se0j-tuVY-mBPW-f7RU-5AAQ1c
  LV Write Access        read/write
  LV Creation host, time localhost, 2021-01-11 22:11:49 +0300
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
  LV UUID                VjdLT2-KQcq-46wv-tytr-roM6-abUD-YEJwLk
  LV Write Access        read/write
  LV Creation host, time localhost, 2021-01-11 22:11:50 +0300
  LV Status              available
  # open                 1
  LV Size                <18.86 GiB
  Current LE             4827
  Segments               2
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           253:0
```
