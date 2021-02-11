# 15: Yum & RPM
### Подключить репозиторий docker community edition
```bash
[root@mitnik ~]# sudo yum install -y yum-utils
[root@mitnik ~]# sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
Loaded plugins: fastestmirror
adding repo from: https://download.docker.com/linux/centos/docker-ce.repo
grabbing file https://download.docker.com/linux/centos/docker-ce.repo to /etc/yum.repos.d/docker-ce.repo
repo saved to /etc/yum.repos.d/docker-ce.repo
```
### Установить docker-ce версии 19.03.14
```bash
[root@mitnik ~]# sudo yum -y install docker-ce-19.03.1-3.el7.x86_64
```
### Убедиться, что установлена нужная версия
```bash
[root@mitnik bash_test]# yum list installed docker-ce
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirror.awanti.com
 * extras: mirror.docker.ru
 * updates: mirror.axelname.ru
Installed Packages
docker-ce.x86_64                3:19.03.1-3.el7                @docker-ce-stable

[root@mitnik bash_test]# yum info docker-ce
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirror.awanti.com
 * extras: mirror.docker.ru
 * updates: mirror.axelname.ru
Installed Packages
Name        : docker-ce
Arch        : x86_64
Epoch       : 3
Version     : 19.03.1
Release     : 3.el7
Size        : 104 M
Repo        : installed
From repo   : docker-ce-stable
Summary     : The open-source application container engine
URL         : https://www.docker.com
License     : ASL 2.0
Description : Docker is a product for you to build, ship and run any application
            : as a lightweight container.
            :
            : Docker containers are both hardware-agnostic and
            : platform-agnostic. This means they can run anywhere, from your
            : laptop to the largest cloud compute instance and everything in
            : between - and they don't require you to use a particular language,
            : framework or packaging system. That makes them great building
            : blocks for deploying and scaling web apps, databases, and backend
            : services without depending on a particular stack or provider.

Available Packages
Name        : docker-ce
Arch        : x86_64
Epoch       : 3
Version     : 20.10.3
Release     : 3.el7
Size        : 27 M
Repo        : docker-ce-stable/7/x86_64
Summary     : The open-source application container engine
URL         : https://www.docker.com
License     : ASL 2.0
Description : Docker is a product for you to build, ship and run any application
            : as a lightweight container.
            :
            : Docker containers are both hardware-agnostic and
            : platform-agnostic. This means they can run anywhere, from your
            : laptop to the largest cloud compute instance and everything in
            : between - and they don't require you to use a particular language,
            : framework or packaging system. That makes them great building
            : blocks for deploying and scaling web apps, databases, and backend
            : services without depending on a particular stack or provider.

[root@mitnik ~]# yum list docker-ce
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirror.awanti.com
 * extras: mirror.docker.ru
 * updates: mirror.axelname.ru
Installed Packages
docker-ce.x86_64                                            3:19.03.1-3.el7                                             @docker-ce-stable
Available Packages
docker-ce.x86_64                                            3:20.10.3-3.el7                                             docker-ce-stable
```
### Обновить docker-ce до последней версии
```bash
[root@mitnik bash_test]# yum list installed docker-ce

Test
[root@mitnik bash_test]# yum list docker-ce
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirror.awanti.com
 * extras: mirror.docker.ru
 * updates: mirror.axelname.ru
Installed Packages
docker-ce.x86_64                3:20.10.3-3.el7                @docker-ce-stable
```
### Вывести список последних операций yum
```bash
[root@mitnik bash_test]# yum history
Loaded plugins: fastestmirror
ID     | Login user               | Date and time    | Action(s)      | Altered
-------------------------------------------------------------------------------
    13 | root <root>              | 2021-02-11 16:00 | I, U           |    5
    12 | root <root>              | 2021-02-10 21:19 | Install        |   12
    11 | root <root>              | 2021-02-10 21:18 | Install        |    4
    10 | root <root>              | 2021-02-07 21:16 | Install        |    2
     9 | root <root>              | 2021-02-07 20:00 | Install        |    1
     8 | root <root>              | 2021-02-07 18:08 | Install        |    2
     7 | root <root>              | 2021-02-07 18:07 | Install        |    6
     6 | root <root>              | 2021-02-07 17:57 | I, U           |   78
     5 | root <root>              | 2021-02-04 19:30 | Install        |    1
     4 | root <root>              | 2021-01-29 03:16 | Install        |    1
     3 | root <root>              | 2021-01-11 20:09 | Install        |    1
     2 | root <root>              | 2021-01-11 20:09 | Install        |    1
     1 | System <unset>           | 2021-01-11 22:12 | Install        |  299
history list
```
### Вывести полную информацию об установленном ранее пакете
```bash
[root@mitnik bash_test]# yumdb info docker-ce
Loaded plugins: fastestmirror
3:docker-ce-20.10.3-3.el7.x86_64
     changed_by = 0
     checksum_data = 4af0191d6b80f5a0b35cf7ffd02ab90caa6528f62c720cb62666183196b76be3
     checksum_type = sha256
     command_line = update docker-ce
     from_repo = docker-ce-stable
     from_repo_revision = 1612219782
     from_repo_timestamp = 1612219782
     installed_by = 0
     origin_url = https://download.docker.com/linux/centos/7/x86_64/stable/Packages/docker-ce-20.10.3-3.el7.x86_64.rpm
     reason = user
     releasever = 7
     var_contentdir = centos
     var_infra = stock
     var_uuid = 4ea227b4-c6d1-4840-a337-30f5fabbfc25
```
### Удалить docker-ce
```bash
[root@mitnik bash_test]# yum remove docker-ce

[root@mitnik bash_test]# yum list installed docker-ce
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirror.awanti.com
 * extras: mirror.docker.ru
 * updates: mirror.axelname.ru
Error: No matching Packages to list
```
# 16. File Systems
### Переместить mlocate.db в новое место
```bash
[root@mitnik ~]# mv /var/lib/mlocate/mlocate.db ~/new_lib_mlocate
[root@mitnik ~]# ls -la ~/new_lib_mlocate/
total 744
drwxr-xr-x. 2 root root        24 Feb 11 22:50 .
dr-xr-x---. 7 root root      4096 Feb 11 20:02 ..
-rw-r-----. 1 root slocate 755501 Feb 11 22:50 mlocate.db

[root@mitnik ~]# cat /var/lib/mlocate/mlocate.db
cat: /var/lib/mlocate/mlocate.db: No such file or directory
```
### Создать новый файл file_task16.txt с любым содержанием и добавить информацию о нём в новый mlocate.db
```bash
[root@mitnik ~]# touch ~/file_task16.txt | echo "Hello" > file_task16.txt
[root@mitnik ~]# cat file_task16.txt
Hello
[root@mitnik ~]# updatedb -o ~/new_lib_mlocate/mlocate.db

[root@mitnik ~]# locate --database ~/new_lib_mlocate/mlocate.db file_task16.txt | grep -i file_task16.txt
/root/file_task16.txt
```
### Найти файл file_task16.txt через locate и вывести его содержимое на экран (без явного указания полного пути к файлу)
```bash
[root@mitnik ~]# locate --database ~/new_lib_mlocate/mlocate.db file_task16.txt | cat file_task16.txt
Hello
```
### Создать хардлинк на file_task16.txt, назвать его file_task16_hard.txt
```bash
[root@mitnik ~]# ln file_task16.txt file_task16_hard.txt
[root@mitnik ~]# ls -lai | grep 16
33576103 -rw-r--r--.  2 root root     6 Feb 11 22:53 file_task16_hard.txt
33576103 -rw-r--r--.  2 root root     6 Feb 11 22:53 file_task16.txt
```
### Внести любые изменения в file_task16.txt
```bash
[root@mitnik ~]# echo World >> file_task16.txt
[root@mitnik ~]# cat file_task16.txt
Hello
World
```
### Удалить file_task16.txt
```bash
[root@mitnik ~]# rm file_task16.txt
rm: remove regular file ‘file_task16.txt’? y
```
### Вывести на экран file_task16_hard.txt, убедиться, что в нём отражены изменения
```bash
[root@mitnik ~]# cat file_task16_hard.txt
Hello
World
```
* Создать именованный пайп pipe01
В первом терминале запустить считывание с pipe01 (любым способом, можно перечислить несколько)
Создать софтлинк на пайп, назвать его pipe01-s
Во втором терминале отправить в pipe01-s данные (любым способом, можно перечислить несколько)
Убедиться, что данные были считаны первым терминалом
# mkfifo
** Сделать то же самое, используя файл Unix socket (подсказка: используйте пакеты netcat и socat)
