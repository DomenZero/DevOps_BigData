# Boot process
#### 1.	* Self-study: find a utility to inspect initrd file contents. Find all files that are related to XFS filesystem and give a short description for every file.
```bash
[root@mitnik temp]# uname -r
3.10.0-1160.15.2.el7.x86_64
[root@mitnik temp]# mkinitrd
usage: mkinitrd [--version] [--help] [-v] [-f] [--preload <module>]
       [--image-version] [--with=<module>]
       [--nocompress]
       <initrd-image> <kernel-version>

       (ex: mkinitrd /boot/initramfs-3.10.0-1160.15.2.el7.x86_64.img 3.10.0-1160.15.2.el7.x86_64)
[root@mitnik temp]# mkinitrd /boot/initrd_test.img 3.10.0-1160.15.2.el7.x86_64 

[root@mitnik temp]# cpio -civt < /boot/initrd_test.img
drwxr-xr-x   3 root     root            0 Feb 17 19:01 .
drwxr-xr-x   3 root     root            0 Feb 17 19:01 kernel
drwxr-xr-x   3 root     root            0 Feb 17 19:01 kernel/x86
drwxr-xr-x   2 root     root            0 Feb 17 19:01 kernel/x86/microcode
-rw-r--r--   1 root     root        19456 Feb 17 19:01 kernel/x86/microcode/GenuineIntel.bin
-rw-r--r--   1 root     root            2 Feb 17 19:01 early_cpio
40 blocks
```
#### 2.	* Self-study: explain the difference between ordinary and rescue initrd images.
initrd - обеспечивает доступность всех необходимых ресурсов (модулей), чтобы ядро могло смонтировать корневую файловую систему.
initrd rescue - будет использовать устройство
initrd ordinary - распаковывается в файловую систему
#### 3.	* Self-study: study dracut utility that is used for rebuilding initrd image. Give an example for adding driver/kernel module for your initrd and recreating it.
```bash
[root@mitnik temp]# dracut new_dracut.img 3.10.0-1160.15.2.el7.x86_64
[root@mitnik temp]# ls -la
total 55480
drwxrwxrwx  3 root root       93 Feb 17 19:07 .
dr-xr-x---. 8 root root     4096 Feb 17 17:49 ..
drwxr-xr-x  7 root root     4096 Feb 17 18:04 3.10.0-1160.15.2.el7.x86_64
-rw-r--r--  1 root root 36005177 Feb 17 18:11 initrd_3_10_0_test.img
-rw-------  1 root root 20795275 Feb 17 19:07 new_dracut.img

[root@mitnik temp]# lsinitrd new_dracut.img
Image: new_dracut.img: 20M
========================================================================
Early CPIO image
========================================================================
drwxr-xr-x   3 root     root            0 Feb 17 19:07 .
-rw-r--r--   1 root     root            2 Feb 17 19:07 early_cpio
drwxr-xr-x   3 root     root            0 Feb 17 19:07 kernel
drwxr-xr-x   3 root     root            0 Feb 17 19:07 kernel/x86
drwxr-xr-x   2 root     root            0 Feb 17 19:07 kernel/x86/microcode
-rw-r--r--   1 root     root        19456 Feb 17 19:07 kernel/x86/microcode/GenuineIntel.bin
========================================================================
Version: dracut-033-572.el7

```

#### 4.	Enable recovery options for grub, update main configuration file and find new item in GRUB2 config in /boot.
```bash
# Commented recovery
[root@mitnik ~]# nano /etc/default/grub
[root@mitnik ~]# cat /etc/default/grub
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console"
GRUB_CMDLINE_LINUX="crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet"
#GRUB_DISABLE_RECOVERY="true"

/boot/grub2/grub.cfg
```
#### 5.	Modify option vm.dirty_ratio:
a.	using sysctl utility
```bash
[root@mitnik ~]# sysctl -w vm.dirty_ratio=50
vm.dirty_ratio = 50
[root@mitnik ~]# sysctl -a | grep dirty
sysctl: reading key "net.ipv6.conf.all.stable_secret"
sysctl: reading key "net.ipv6.conf.default.stable_secret"
sysctl: reading key "net.ipv6.conf.eth0.stable_secret"
sysctl: reading key "net.ipv6.conf.eth1.stable_secret"
sysctl: reading key "net.ipv6.conf.lo.stable_secret"
vm.dirty_background_bytes = 0
vm.dirty_background_ratio = 10
vm.dirty_bytes = 0
vm.dirty_expire_centisecs = 3000
vm.dirty_ratio = 50
vm.dirty_writeback_centisecs = 500
```
b.	using sysctl configuration file
```bash
[root@mitnik ~]# echo 40 > /proc/sys/vm/dirty_ratio
[root@mitnik ~]# cat /proc/sys/vm/dirty_ratio
40
```

#### 6. Disable selinux using kernel cmdline
```bash
# Set disabled to SELINUX and reboot

[root@mitnik ~]# cat /etc/selinux/config

# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=disabled
# SELINUXTYPE= can take one of three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected.
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted

[root@mitnik ~]# getenforce
Disabled

```
# iptables
With enabled firewalld:
#### 1.	Add rule using firewall-cmd that will allow SSH access to your server *only* from network 192.168.56.0/24 and interface enp0s8 (if your network and/on interface name differs - change it accordingly).
```bash
[root@mitnik ~]# firewall-cmd --zone=trusted --add-source=192.168.56.0/24
success
[root@mitnik ~]# firewall-cmd --zone=trusted --add-service=ssh
success
[root@mitnik ~]# firewall-cmd --permanent --zone=trusted --add-interface=eth1   
The interface is under control of NetworkManager, setting zone to 'trusted'.
success
[root@mitnik ~]# firewall-cmd --zone=trusted --list-all
trusted (active)
  target: ACCEPT
  icmp-block-inversion: no
  interfaces: eth1
  sources: 192.168.56.0/24
  services: ssh
  ports:
  protocols:
  masquerade: no
  forward-ports:
  source-ports:
  icmp-blocks:
  rich rules:
```
#### 2.	Shutdown firewalld and add the same rules via iptables.
```bash
[root@mitnik ~]# systemctl stop firewalld  
[root@mitnik ~]# firewall-cmd --state
not running

[root@mitnik ~]# iptables -A INPUT -p tcp --dport ssh -d 192.168.56.0/24 -i eth0 -j ACCEPT
```
