# 1. Users and groups

### 1.1. Создание группы sales с GID 4000
```bash
[root@localhost shared-folder]# groupadd -g 4000 sales
[root@localhost shared-folder]# cat /etc/group | tail -1
sales:x:4000:
```
### 1.2. Создание пользователей bob, alice, evec основной группой sales
```bash
[root@localhost ~]# sudo useradd -g 4000 bob
[root@localhost ~]# sudo useradd -g 4000 alice
[root@localhost ~]# sudo useradd -g 4000 eve
[root@localhost ~]# ll /home | sort -k 6 -r
drwx------. 2 eve   sales  62 Jan 25 13:32 eve
drwx------. 2 bob   sales  62 Jan 25 13:32 bob
drwx------. 2 alice sales  62 Jan 25 13:32 alice
[root@localhost ~]# cat /etc/passwd
bob:x:2025:4000::/home/bob:/bin/bash
alice:x:2026:4000::/home/alice:/bin/bash
eve:x:2027:4000::/home/eve:/bin/bash
```
### 1.3. Измените пользователям пароли
```bash
[root@localhost ~]# sudo passwd eve
[root@localhost ~]# sudo passwd bob
[root@localhost ~]# sudo passwd alice
[root@localhost ~]# su alice
[alice@localhost root]$ su bob
Password:
[bob@localhost root]$ su eve
Password:
[eve@localhost root]
```
### 1.4. Правило смены пароля, каждые 30 дней
Изменить PASS_MAX_DAYS на 30 в файле /etc/login.defs
```bash
[root@localhost ~]# cat /etc/shadow
bob:!!:18652:0:30:7:::
alice:!!:18652:0:30:7:::
eve:!!:18652:0:30:7:::
```
### 1.5. Новые аккаунты группы sales должны истечь по окончанию 90
```bash
[root@localhost ~]# sudo chage -E $(date -d +90days +%Y-%m-%d) bob
[root@localhost ~]# sudo chage -E $(date -d +90days +%Y-%m-%d) alice
[root@localhost ~]# sudo chage -E $(date -d +90days +%Y-%m-%d) eve
[root@localhost ~]# chage -l bob
Last password change                                    : Jan 25, 2021
Password expires                                        : Feb 09, 2021
Password inactive                                       : never
Account expires                                         : Apr 25, 2021
Minimum number of days between password change          : 15
Maximum number of days between password change          : 15
Number of days of warning before password expires       : 7
```
### 1.6. bob каждые 15 дней меняет пароль
```bash
[root@localhost ~]# chage -m 15 -M 15 bob
[root@localhost ~]# chage -l bob
Last password change                                    : Jan 25, 2021
Password expires                                        : Feb 09, 2021
Password inactive                                       : never
Account expires                                         : never
Minimum number of days between password change          : 15
Maximum number of days between password change          : 15
Number of days of warning before password expires       : 7
```
### 1.7. Смена пароля после первого логина
```bash
[root@localhost ~]# passwd -e eve
Expiring password for user eve.
passwd: Success
[root@localhost ~]# chage -l eve
Last password change                                    : password must be changed
Password expires                                        : password must be changed
Password inactive                                       : password must be changed
Account expires                                         : never
Minimum number of days between password change          : 0
Maximum number of days between password change          : 30
Number of days of warning before password expires       : 7
[alice@localhost root]$ su eve
Password:
You are required to change your password immediately (root enforced)
Changing password for eve.
(current) UNIX password:
```

# 2. Controlling access to files with Linux file system permissions

### 2.1. Создание группы students. Создайте трёх пользователей glen, antony, lesly
```bash
[root@localhost home]# groupadd students
[root@localhost home]# sudo useradd -G students glen
[root@localhost home]# sudo useradd -G students antony
[root@localhost home]# sudo useradd -G students lesly
```
### 2.2. Созданиe /home/students students. 
Где эти три пользователя могут работать совместно с файлами.Должен быть возможен только пользовательский и групповой доступ, создание и удаление файлов в /home/students. Файлы, созданные в этой директории, должны автоматически присваиваться группе студентов students.
```bash
[root@localhost home]# mkdir students
[root@localhost home]# chgrp students students
[root@localhost home]# chmod o-x students
[root@localhost home]# chmod o-r students
[root@localhost home]# chmod g+w students
[root@localhost home]# chmod g+s students
[root@localhost home]# ls -ld students
drwxrws---. 2 root students 6 Jan 25 20:52 students
# Test
[lesly@localhost students]$ ll
total 8
-rw-rw-r--. 1 glen   students 26 Jan 25 21:31 1.md
-rw-rw-r--. 1 antony students  8 Jan 25 21:30 antony.md
[lesly@localhost students]$ rm -r 1.md
[lesly@localhost students]$ ll
total 4
-rw-rw-r--. 1 antony students 8 Jan 25 21:30 antony.md
```

# 3. ACL

### 3.1. От суперпользователя создайте папку /share/cases и создайте внутри 2 файла murders.txt и moriarty.txt
```bash
[root@localhost home]# mkdir -p /share/cases && chmod  2770 /share/cases
[root@localhost home]# ls -ld /share
drwxr-xr-x. 3 root root 19 Jan 25 22:12 /share
[root@localhost home]# ls -ld /share/cases
drwxrws---. 2 root root 6 Jan 25 22:12 /share/cases
[root@localhost home]# touch /share/cases/murders.txt && touch /share/cases/moriarty.txt
```
### 3.2. Создайте группу bakerstreet с пользователями holmes, watson.
Создайте группу scotlandyard с пользователями lestrade, gregson, jones.
Директория и всё её содержимое должно принадлежать группеbakerstreet, при этом файлы должны обновляться для чтения и записи для владельца и группы (bakerstreet). У других пользователей не должно быть никаких разрешений. Вам также необходимо предоставить доступы на чтение и запись для группы scotlandyard, за исключением Jones, который может только читать докуменn
```bash
[root@localhost home]# groupadd bakerstreet && useradd -G bakerstreet holmes && useradd -G bakerstreet watson
[root@localhost home]# groupadd scotlandyard && useradd -G scotlandyard lestrade && useradd -G scotlandyard gregson && useradd -G scotlandyard jones

[root@localhost home]# cat /etc/group | grep -E "bakerstreet*|scotlandyard*"
bakerstreet:x:4002:holmes,watson
scotlandyard:x:4003:lestrade,gregson,jones

[root@localhost home]# chgrp bakerstreet /share/cases
[root@localhost home]# ls -ld /share/cases
drwxrws---. 2 root bakerstreet 45 Jan 25 22:14 /share/cases

[root@localhost ~]# setfacl -dm g:scotlandyard:rwx /share/cases
[root@localhost ~]# su lestrade
[lestrade@localhost root]$ cd /share/cases
[lestrade@localhost cases]$ exit
exit
[root@localhost ~]# setfacl -dm u:jones:rx /share/cases
[root@localhost ~]# su jones
[jones@localhost root]$ cd /share/cases

[root@localhost /]# getfacl share/cases
# file: share/cases
# owner: root
# group: bakerstreet
# flags: ss-
user::rwx
user:jones:r-x
group::rwx
group:scotlandyard:rwx
mask::rwx
other::---
default:user::rwx
default:user:jones:r-x
default:group::rwx
default:group:scotlandyard:rwx
default:mask::rwx
default:other::---

# если файлы были созданы ранее и не унаследовали
[root@localhost /]# getfacl /home/share/cases | setfacl -M- /home/share/cases/murders.txt
[root@localhost /]# getfacl /home/share/cases | setfacl -M- /home/share/cases/moriarty.txt
[root@localhost /]# ls -l /share/cases
total 8
-rwxrwx--T+ 1 root bakerstreet  4 Jan 25 23:28 moriarty.txt
-rwxrwx--T+ 1 root bakerstreet 13 Jan 30 01:17 murders.txt

```
