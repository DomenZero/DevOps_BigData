	# 15:
	- Подключить репозиторий docker community edition
```bash
[root@mitnik ~]# sudo yum install -y yum-utils
[root@mitnik ~]# sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
Loaded plugins: fastestmirror
adding repo from: https://download.docker.com/linux/centos/docker-ce.repo
grabbing file https://download.docker.com/linux/centos/docker-ce.repo to /etc/yum.repos.d/docker-ce.repo
repo saved to /etc/yum.repos.d/docker-ce.repo
```
	- Установить docker-ce версии 19.03.14
```bash
[root@mitnik ~]# sudo yum -y install docker-ce-19.03.1-3.el7.x86_64
```
	- Убедиться, что установлена нужная версия
```bash
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
	- Обновить docker-ce до последней версии
	- Вывести список последних операций yum
	- Вывести полную информацию об установленном ранее пакете
	- Удалить docker-ce
