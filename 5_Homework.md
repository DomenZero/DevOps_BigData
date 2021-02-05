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

