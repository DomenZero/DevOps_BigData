# Boot process
#### 1.	* Self-study: find a utility to inspect initrd file contents. Find all files that are related to XFS filesystem and give a short description for every file.
#### 2.	* Self-study: explain the difference between ordinary and rescue initrd images.
#### 3.	* Self-study: study dracut utility that is used for rebuilding initrd image. Give an example for adding driver/kernel module for your initrd and recreating it.

#### 4.	Enable recovery options for grub, update main configuration file and find new item in GRUB2 config in /boot.

#### 5.	Modify option vm.dirty_ratio:
a.	using sysctl utility
b.	using sysctl configuration file

#### 6. Disable selinux using kernel cmdline

# iptables
With enabled firewalld:
#### 1.	Add rule using firewall-cmd that will allow SSH access to your server *only* from network 192.168.56.0/24 and interface enp0s8 (if your network and/on interface name differs - change it accordingly).
```bash

```
#### 2.	Shutdown firewalld and add the same rules via iptables.
```bash
[root@mitnik ~]# systemctl stop firewalld  
[root@mitnik ~]# firewall-cmd --state
not running

[root@mitnik ~]# iptables -A INPUT -p tcp --dport ssh -d 192.168.56.0/24 -i eth0 -j ACCEPT
```