# Task 1
### 1.1. SSH to remotehost using username and password provided to you in Slack. Log out from remotehost.
```bash
[root@localhost ~]# ssh Maksim_Merkulov@40.68.74.188
The authenticity of host '40.68.74.188 (40.68.74.188)' can't be established.
ECDSA key fingerprint is SHA256:4r72O0/zt+DU9bsD85l3ZeMMYDlDRTv9h4KWBMoekKY.
ECDSA key fingerprint is MD5:51:49:b2:e4:ae:c8:cf:8f:27:20:93:52:a1:41:14:75.
Are you sure you want to continue connecting (yes/no)? y
Please type 'yes' or 'no': yes
Warning: Permanently added '40.68.74.188' (ECDSA) to the list of known hosts.
Password:
[Maksim_Merkulov@vm-one ~]$ hostname
vm-one
```
### 1.2. Generate new SSH key-pair on your localhost with name "hw-5" (keys should be created in ~/.ssh folder).
```bash
[admin@localhost ~]$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/admin/.ssh/id_rsa): /home/admin/.ssh/hw_5
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/admin/.ssh/hw_5.
Your public key has been saved in /home/admin/.ssh/hw_5.pub.
The key fingerprint is:
SHA256:cmjWJpSVqva1MD6va81u0XYrWcVftb4PC7vqnf+9yvY admin@localhost.localdomain
The key's randomart image is:
+---[RSA 2048]----+
|        ..       |
|       o.       .|
|      o.     .  o|
|     ..o      o..|
|     .* S.   ....|
|    ooo=o o o  ..|
|   . o * + +... .|
|      = = o.o= +.|
|     .oBo.oo*==E*|
+----[SHA256]-----+
[admin@localhost ~]$ ls /home/admin/.ssh
hw_5  hw_5.pub  known_hosts
```
### 1.3. Set up key-based authentication, so that you can SSH to remotehost without password.
```bash
[admin@localhost ~]$ cat ~/.ssh/hw_5.pub | ssh Maksim_Merkulov@40.68.74.188 "mkdir -p ~/.ssh && chmod 0700 ~/.ssh && cat >  ~/.ssh/authorized_keys"
Password:

#!!!!! OR
[admin@localhost ~]$ ssh-copy-id -i ~/.ssh/hw_5.pub Maksim_Merkulov@40.68.74.188
/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/admin/.ssh/hw_5.pub"
/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
Password:

[admin@localhost ~]$ ssh Maksim_Merkulov@40.68.74.188                                                      Password:
Last login: Fri Jan 29 20:42:44 2021 from pppoe.178-66-159-93.dynamic.avangarddsl.ru
[Maksim_Merkulov@vm-one ~]$ cat ~/.ssh/authorized_keys
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC95eNJ+8xOYkJMq1HyRYrbPcrjIppir2oHxU+CvAdlBmXIgGMPAZ3ihgapWy8wG1EpPIoFrIl9QxhxKXv2NlrsD5n7cBFpJBx7qcuUE0QulUZJwGs6Ie92/ET8oPiZRtkGDMj9UXjW4yj+hW+aHv5iY0n1fs6HszKArOL6TWXc1Jw39vT28RwKfP1Z2HK3xNerjTt7i06qU4GasxMJEVUqCxz0qeLipPYhDj/uOWTmi6stUYO6IpdOSgCBGF6eEih2WmKCin8NAYEJ7iAyBoOMAfp2Ey3smyGsvnYMwu4yDVGcJYns+jstmdZ1t23jLLXyVC2YxIygGjRscpw/c/0X admin@localhost.localdomain
[Maksim_Merkulov@vm-one ~]$ chmod 700 ~/.ssh
[Maksim_Merkulov@vm-one ~]$ chmod 600 ~/.ssh/authorized_keys
[Maksim_Merkulov@vm-one ~]$ ls -la ~/.ssh/authorized_keys
-rw-------. 1 Maksim_Merkulov Maksim_Merkulov 409 Jan 29 21:03 /home/Maksim_Merkulov/.ssh/authorized_keys
[Maksim_Merkulov@vm-one ~]$ ls -la ~/.ssh
total 4
drwx------. 2 Maksim_Merkulov Maksim_Merkulov  29 Jan 29 20:40 .
drwx------. 5 Maksim_Merkulov Maksim_Merkulov 124 Jan 29 20:39 ..
-rw-------. 1 Maksim_Merkulov Maksim_Merkulov 409 Jan 29 21:03 authorized_keys
```
1.4. SSH to remotehost without password. Log out from remotehost.
```bash
[admin@localhost root]$ sudo ssh -i /home/admin/.ssh/hw_5 Maksim_Merkulov@40.68.74.188
Last login: Fri Jan 29 21:10:28 2021 from pppoe.178-66-159-93.dynamic.avangarddsl.ru
```
1.5. Create SSH config file, so that you can SSH to remotehost simply running `ssh remotehost` command. As a result, provide output of command `cat ~/.ssh/config`.
```bash
[admin@localhost root]$ cat ~/.ssh/config

Host hw_5
    HostName 40.68.74.188
    User Maksim_Merkulov
    IdentityFile /home/admin/.ssh/hw_5

[admin@localhost root]$ ll ~/.ssh/config
-rw-rw-r--. 1 admin admin 62 Jan 30 00:22 /home/admin/.ssh/config
[admin@localhost root]$ chmod 0700 ~/.ssh/config
[admin@localhost root]$ ssh hw_5
Last login: Fri Jan 29 21:20:29 2021 from pppoe.178-66-159-93.dynamic.avangarddsl.ru
[Maksim_Merkulov@vm-one ~]$ exit
logout

```
### 1.6. Using command line utility (curl or telnet) verify that there are some webserver running on port 80 of webserver.  
Notice that webserver has a private network IP, so you can access it only from the same network (when you are on remotehost  
that runs in the same private network). Log out from remotehost.
```bash
[Maksim_Merkulov@vm-one ~]$ curl --head 10.0.0.5:80
HTTP/1.1 200 OK
Server: nginx/1.16.1
Date: Fri, 05 Feb 2021 16:44:18 GMT
Content-Type: text/html
Content-Length: 786
Last-Modified: Tue, 29 May 2018 16:55:02 GMT
Connection: keep-alive
ETag: "5b0d85e6-312"
Accept-Ranges: bytes

[Maksim_Merkulov@vm-one ~]$ curl -ksS --head 10.0.0.5:80 | grep Server
Server: nginx/1.16.1

# -kss = --insecure --silent --show-error
```
### 1.7. Using SSH setup port forwarding, so that you can reach webserver from your localhost (choose any free local port you like).
```bash
[admin@localhost root]$ ssh -L 2021:10.0.0.5:80 Maksim_Merkulov@40.68.74.188
Password:
Last login: Fri Feb  5 19:41:28 2021 from pppoe.178-66-131-179.dynamic.avangarddsl.ru
[Maksim_Merkulov@vm-one ~]$
```
### 1.8. Like in 1.6, but on localhost using command line utility verify that localhost and port you have specified act like webserver, returning same result as in 1.6.
```bash
[admin@localhost .ssh]$ curl --head 127.0.0.1:2021 | grep Server
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0   786    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
Server: nginx/1.16.1
```
### 1.9. Open webserver webpage in browser of your Host machine of VirtualBox (Windows, or Mac, or whatever else you use). You may need to setup port forwarding in settings of VirtualBox.
![5_1_9_Test_Forwarding_to_HomeOS](/images/5_1_9_network_test.jpg)
#### 1. SSH connection from a SSH_Client to a Web_Server located on a SSH_Server
```bash
[admin@localhost root]$ ssh -L 2021:10.0.0.5:80 Maksim_Merkulov@40.68.74.188
```
#### 2. Test connection on the SSH_Client
```bash
[admin@localhost .ssh]$ curl --head 127.0.0.1:2021 | grep Server
```
#### 3. SSH connection from a Home_OS to the Web_Server located on the SSH_Server
```cmd
C:\Users\Domen0>ssh -L 2021:127.0.0.1:2021 admin@192.168.0.104
The authenticity of host '192.168.0.104 (192.168.0.104)' can't be established.
ECDSA key fingerprint is SHA256:/QcqKs/v0NmQbViHEyPi8Sy3vF7hAeTUJQRXhb8Jn5E.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.0.104' (ECDSA) to the list of known hosts.
admin@192.168.0.104's password:
Last login: Fri Feb  5 22:11:52 2021
[admin@localhost ~]$
```
#### 4. Test connection and open a web page on the Home_OS

# Task 2.

### 2.1 Imagine your localhost has been relocated to Havana. Change the time zone on the localhost to Havana and verify the time zone has been changed properly (may be multiple commands).
```bash
[admin@localhost .ssh]$ timedatectl
      Local time: Fri 2021-02-05 23:57:16 MSK
  Universal time: Fri 2021-02-05 20:57:16 UTC
        RTC time: Fri 2021-02-05 23:57:14
       Time zone: Europe/Moscow (MSK, +0300)
     NTP enabled: n/a
NTP synchronized: no
 RTC in local TZ: no
      DST active: n/a
[admin@localhost .ssh]$ timedatectl list-timezones | grep Havana
America/Havana
[admin@localhost .ssh]$ sudo timedatectl set-timezone America/Havana
[admin@localhost .ssh]$ timedatectl
      Local time: Fri 2021-02-05 15:58:11 CST
  Universal time: Fri 2021-02-05 20:58:11 UTC
        RTC time: Fri 2021-02-05 23:58:09
       Time zone: America/Havana (CST, -0500)
     NTP enabled: n/a
NTP synchronized: no
 RTC in local TZ: no
      DST active: no
 Last DST change: DST ended at
                  Sun 2020-11-01 00:59:59 CDT
                  Sun 2020-11-01 00:00:00 CST
 Next DST change: DST begins (the clock jumps one hour forward) at
                  Sat 2021-03-13 23:59:59 CST
                  Sun 2021-03-14 01:00:00 CDT
```
### 2.2 Find all systemd journal messages on localhost, that were recorded in the last 50 minutes and originate from a system service started with user id 81 (single command).
```bash
journalctl -b --since "50 min ago" _UID=81

-b - records from a last boot
--since - date
_UID  - User_ID (check like: id -u )
```
### 2.3 Configure rsyslogd by adding a rule to the newly created configuration file /etc/rsyslog.d/auth-errors.conf to log all security and authentication messages with the priority alert and higher to the /var/log/auth-errors file. Test the newly added log directive with the logger command (multiple commands).
```bash
[admin@localhost rsyslog.d]$ sudo cat auth-errors.conf
auth,authpriv.*         /var/log/auth-errors

#Test

[admin@localhost rsyslog.d]$ sudo cat /var/log/auth-errors
Feb  6 00:46:27 localhost sudo: pam_unix(sudo:session): session closed for user root
Feb  6 00:46:27 localhost polkitd[652]: Unregistered Authentication Agent for unix-process:1807:2068488 (system bus name :1.79, object path /org/freedesktop/PolicyKit1/AuthenticationAgent, locale en_US.UTF-8) (disconnected from bus)
Feb  6 00:48:05 localhost sudo:   admin : TTY=pts/0 ; PWD=/etc/rsyslog.d ; USER=root ; COMMAND=/sbin/ss -tulnp
Feb  6 00:48:05 localhost sudo: pam_unix(sudo:session): session opened for user root by root(uid=0)
Feb  6 00:48:05 localhost sudo: pam_unix(sudo:session): session closed for user root
Feb  6 00:48:13 localhost sudo:   admin : TTY=pts/0 ; PWD=/etc/rsyslog.d ; USER=root ; COMMAND=/sbin/ss -tulnp
Feb  6 00:48:13 localhost sudo: pam_unix(sudo:session): session opened for user root by root(uid=0)
Feb  6 00:48:13 localhost sudo: pam_unix(sudo:session): session closed for user root
Feb  6 00:48:32 localhost sudo:   admin : TTY=pts/0 ; PWD=/etc/rsyslog.d ; USER=root ; COMMAND=/bin/systemctl status rsyslog
Feb  6 00:48:32 localhost sudo: pam_unix(sudo:session): session opened for user root by root(uid=0)
Feb  6 00:48:32 localhost sudo: pam_unix(sudo:session): session closed for user root
Feb  6 00:51:13 localhost sudo:   admin : TTY=pts/0 ; PWD=/etc/rsyslog.d ; USER=root ; COMMAND=/bin/cat /var/log/auth-errors
Feb  6 00:51:13 localhost sudo: pam_unix(sudo:session): session opened for user root by root(uid=0)

```
