# 1. Processes
### 1.1 Run a sleep command three times at different intervals
```bash
[jones@localhost share]$ sleep 2
[jones@localhost share]$ sleep 0.5s
[jones@localhost share]$ sleep 3m
```
### 1.2. Send a SIGSTOP signal to all of them in three different ways.
```bash
[jones@localhost share]$ sleep 2m >/dev/null &
[1] 1886
[jones@localhost share]$ ps aux | awk '/sleep/{print $2}' | xargs kill -19
kill: sending signal to 1883 failed: No such process

[1]+  Stopped                 sleep 2m > /dev/null
[jones@localhost share]$ sleep 2m >/dev/null &
[2] 1886
[jones@localhost share]$ ps aux | awk '/sleep/{print $2}' | xargs kill -STOP
kill: sending signal to 1888 failed: No such process

[2]+  Stopped                 sleep 2m > /dev/null
[jones@localhost share]$ ps aux | grep "sleep"
jones     1781  0.0  0.0 108052   352 pts/0    S    23:28   0:00 sleep 2m
jones     1784  0.0  0.1 112808   968 pts/0    R+   23:28   0:00 grep --color=auto sleep
[jones@localhost share]$ kill -19 1781
[jones@localhost share]$ ps aux | grep "sleep"
jones     1786  0.0  0.1 112808   968 pts/0    R+   23:29   0:00 grep --color=auto sleep
[1]+  Killed                  sleep 2m > /dev/null
[jones@localhost share]$ pkill sleep
[1]+  Terminated              sleep 2m > /dev/null
```
### 1.3. Check their statuses with a job command
```bash
[jones@localhost share]$ pmap 1870
[1]+  Done                    sleep 2m > /dev/null
```
### 1.4. Terminate one of them. (Any)
```bash
[jones@localhost share]$ ps aux | awk '/sleep/{print $2}' | xargs kill -9
kill: sending signal to 1924 failed: No such process
[1]   Killed                  sleep 2m > /dev/null
[2]-  Killed                  sleep 2m > /dev/null
[3]+  Killed                  sleep 2m > /dev/null
```
### 1.5. To other send a SIGCONT in two different ways.
```bash
[jones@localhost share]$ kill -19 1940
[jones@localhost share]$

[1]+  Stopped                 sleep 2m > /dev/null
[jones@localhost share]$ ps aufx | grep "sleep"
jones     1940  0.0  0.0 108052   356 pts/0    T    00:11   0:00  |                                   \_ sleep 2m
jones     1950  0.0  0.1 112808   968 pts/0    S+   00:13   0:00  |                                   \_ grep --color=auto sleep
[jones@localhost share]$ kill -SIGCONT 1940
[jones@localhost share]$ ps aufx | grep "sleep"
jones     1940  0.0  0.0 108052   356 pts/0    S    00:11   0:00  |                                   \_ sleep 2m
jones     1952  0.0  0.1 112808   968 pts/0    S+   00:13   0:00  |                                   \_ grep --color=auto sleep
____
[jones@localhost share]$ kill -19 1954
[jones@localhost share]$ ps aufx | grep "sleep"
jones     1954  0.0  0.0 108052   356 pts/0    T    00:14   0:00  |                                   \_ sleep 2m
jones     1956  0.0  0.1 112808   968 pts/0    S+   00:14   0:00  |                                   \_ grep --color=auto sleep

[1]+  Stopped                 sleep 2m > /dev/null
[jones@localhost share]$ kill -18 1954
[jones@localhost share]$ ps aufx | grep "sleep"
jones     1954  0.0  0.0 108052   356 pts/0    S    00:14   0:00  |                                   \_ sleep 2m
jones     1958  0.0  0.1 112808   968 pts/0    S+   00:15   0:00  |                                   \_ grep --color=auto sleep
```
### 1.6. Kill one by PID and the second one by job ID
```bash
[jones@localhost share]$ jobs -l
[1]+  1960 Running                 sleep 2m > /dev/null &
[jones@localhost share]$ kill %1
[jones@localhost share]$ jobs -l
[1]+  1960 Terminated              sleep 2m > /dev/null
[jones@localhost share]$ sleep 2m >/dev/null &
[1] 1963
[jones@localhost share]$ kill -9 1963
[jones@localhost share]$ ps aufx | grep "sleep"
jones     1967  0.0  0.1 112808   968 pts/0    S+   00:21   0:00  |                                   \_ grep --color=auto sleep
[1]+  Killed                  sleep 2m > /dev/null
```
# 2. Systemd
### 2.1. Write two daemons 
```bash
[root@localhost ~]# cat /usr/bin/scripts/sleep_service.sh
#!/bin/bash
sleep 30
echo 1 > /tmp/homework
[root@localhost ~]# sudo touch /etc/systemd/system/sleep-daemon.service
[root@localhost ~]# sudo chmod +x /etc/systemd/system/sleep-daemon.service
-rwxr-xr-x.  1 root root    0 Jan 28 01:09 sleep-daemon.service
[root@localhost ~]# cat /etc/systemd/system/sleep-daemon.service
[Unit]
Description=a simple daemon

[Service]
ExecStart=/bin/bash /usr/bin/scripts/sleep_service.sh

[Install]
WantedBy=multi-user.target
```
### 2.2. Make the second depended on the first one (should start only after the first)
```bash
[root@localhost ~]# cat /usr/bin/scripts/sleep_second.sh
#!/bin/bash
echo 2 > /tmp/homework
[root@localhost ~]# cat /etc/systemd/system/sleep-daemon_2.service
[Unit]
Description=the second oneshot
After=sleep-daemon.service

[Service]
Type=oneshot
ExecStart=/usr/bin/scripts/sleep_second.sh

[Install]
WantedBy=multi-user.target
```
### 2.3. Write a timer for the second one and configure it to run on 01.01.2019 at 00:00
```bash
[root@localhost ~]# cat  /etc/systemd/system/sleep-daemon_2.timer
[Unit]
Description=Timer for the sleep_daemon_2

[Timer]
OnCalendar=2019-01-01 00:00:0/1
AccuracySec=1s

[Install]
WantedBy=timers.target
```
### 2.4. Start all daemons and timer, check their statuses, timer list and /tmp/homework
```bash
[root@localhost ~]# systemctl daemon-reload
[root@localhost ~]# systemctl enable sleep-daemon_2.timer
Created symlink from /etc/systemd/system/timers.target.wants/sleep-daemon_2.timer to /etc/systemd/system/sleep-daemon_2.timer.
[root@localhost ~]# systemctl start sleep-daemon_2.timer
[root@localhost ~]# systemctl start sleep-daemon.service
[root@localhost ~]# systemctl status sleep-daemon_2.timer sleep-daemon_2.service
● sleep-daemon_2.timer - Timer for the sleep_daemon_2
   Loaded: loaded (/etc/systemd/system/sleep-daemon_2.timer; enabled; vendor preset: disabled)
   Active: active (elapsed) since Fri 2021-01-29 00:42:15 MSK; 1min 21s ago

Jan 29 00:42:15 localhost.localdomain systemd[1]: Started Timer for the sleep_daemon_2.

● sleep-daemon_2.service - the second oneshot
   Loaded: loaded (/etc/systemd/system/sleep-daemon_2.service; disabled; vendor preset: disabled)
   Active: inactive (dead)
[root@localhost ~]# systemctl status sleep-daemon.service
● sleep-daemon.service - a simple daemon
   Loaded: loaded (/etc/systemd/system/sleep-daemon.service; disabled; vendor preset: disabled)
   Active: active (running) since Fri 2021-01-29 00:43:34 MSK; 15s ago
 Main PID: 2101 (bash)
   CGroup: /system.slice/sleep-daemon.service
           ├─2101 /bin/bash /usr/bin/scripts/sleep_service.sh
           └─2102 sleep 30

Jan 29 00:43:34 localhost.localdomain systemd[1]: Started a simple daemon.
[root@localhost ~]# systemctl list-timers
NEXT                         LEFT     LAST                         PASSED       UNIT                         ACTIVATES
n/a                          n/a      n/a                          n/a          sleep-daemon_2.timer         sleep-daemon_2.service
Fri 2021-01-29 20:52:18 MSK  20h left Wed 2021-01-27 23:41:30 MSK  1 day 1h ago systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service
[root@localhost ~]# cat /tmp/homework
1
```
### 2.5. Stop all daemons and timer
```bash
[root@localhost ~]# systemctl stop sleep-daemon_2.service
[root@localhost ~]# systemctl stop sleep-daemon.service
[root@localhost ~]# systemctl stop sleep-daemon_2.timer
[root@localhost ~]# systemctl list-timers
NEXT                         LEFT     LAST                         PASSED       UNIT                         ACTIVATES
Fri 2021-01-29 20:52:18 MSK  19h left Wed 2021-01-27 23:41:30 MSK  1 day 2h ago systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service

1 timers listed.
Pass --all to see loaded but inactive timers, too.
```

# 3. cron/anacron
### 3.1. Create an anacron job which executes a script with echo Hello > /opt/hello and runs every 2 days
```bash
[root@localhost ~]# cd /etc/cron.daily
[root@localhost cron.daily]# touch anacron_job

[root@localhost cron.daily]# cat anacron_job
#!/bin/bash
echo Hello > /opt/hello

[root@localhost cron.daily]# cat /etc/anacrontab
# /etc/anacrontab: configuration file for anacron

# See anacron(8) and anacrontab(5) for details.

SHELL=/bin/sh
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root
# the maximal random delay added to the base delay of the jobs
RANDOM_DELAY=45
# the jobs will be started during the following hours only
START_HOURS_RANGE=3-22

#period in days   delay in minutes   job-identifier   command
1       5       cron.daily              nice run-parts /etc/cron.daily
7       25      cron.weekly             nice run-parts /etc/cron.weekly
@monthly 45     cron.monthly            nice run-parts /etc/cron.monthly
2       10      test.daily      /bin/sh /etc/cron.daily/anacron_job

[root@localhost cron.daily]# ll /var/spool/anacron
total 12
-rw-------. 1 root root 9 Jan 26 19:09 cron.daily
-rw-------. 1 root root 9 Jan 11 21:59 cron.monthly
-rw-------. 1 root root 9 Jan 25 13:10 cron.weekly
[root@localhost cron.daily]# sudo anacron -f
[root@localhost cron.daily]# ll /var/spool/anacron
total 12
-rw-------. 1 root root 9 Jan 26 19:09 cron.daily
-rw-------. 1 root root 9 Jan 11 21:59 cron.monthly
-rw-------. 1 root root 9 Jan 25 13:10 cron.weekly
-rw-------. 1 root root 0 Jan 29 02:23 test.daily
```
### 3.2. Create a cron job which executes the same command (will be better to create a script for this) and runs it in 1 minute after system boot.
```bash
[root@localhost ~]# cat /path/minute_test.sh
#!/bin/bash
echo Hello Cron > /opt/hello

[root@localhost cron.daily]# sudo crontab -e
crontab: installing new crontab
[root@localhost ~]# crontab -l
@reboot sleep 60;/path/minute_test.sh
```
### 3.3. Restart your virtual machine and check previous job proper execution
```bash
Last login: Fri Jan 29 02:40:24 2021
[root@localhost ~]# cat /opt/hello
Hello
[root@localhost ~]# cat /opt/hello
Hello
[root@localhost ~]# cat /opt/hello
Hello
[root@localhost ~]# cat /opt/hello
Hello
[root@localhost ~]# cat /opt/hello
Hello
[root@localhost ~]# cat /opt/hello
Hello Cron
```

# 4. lsof
### 4.1. Run a sleep command, redirect stdout and stderr into two different files (both of them will be empty).
```bash
[root@localhost ~]# cat /path/redir.sh
sleep 60

[root@localhost ~]# /path/redir.sh & 3>&1 1>/path/stdout.log 2>&3- | tee -a /path/stderr.log
```
### 4.2. Find with the lsof command which files this process uses, also find out where it gets stdout from.
```bash
[root@localhost ~]# lsof -p 1387
COMMAND  PID USER   FD   TYPE DEVICE  SIZE/OFF     NODE NAME
bash    1387 root  cwd    DIR  253,0       204 33575009 /root
bash    1387 root  rtd    DIR  253,0       249       96 /
bash    1387 root  txt    REG  253,0    964536 50548564 /usr/bin/bash
bash    1387 root  mem    REG  253,0 106172832 50548555 /usr/lib/locale/locale-archive
bash    1387 root  mem    REG  253,0     61560    15723 /usr/lib64/libnss_files-2.17.so
bash    1387 root  mem    REG  253,0   2156272    15705 /usr/lib64/libc-2.17.so
bash    1387 root  mem    REG  253,0     19248    15711 /usr/lib64/libdl-2.17.so
bash    1387 root  mem    REG  253,0    174576    16066 /usr/lib64/libtinfo.so.5.9
bash    1387 root  mem    REG  253,0    163312    15698 /usr/lib64/ld-2.17.so
bash    1387 root  mem    REG  253,0     26970    16035 /usr/lib64/gconv/gconv-modules.cache
bash    1387 root    0u   CHR  136,0       0t0        3 /dev/pts/0
bash    1387 root    1u   CHR  136,0       0t0        3 /dev/pts/0
bash    1387 root    2u   CHR  136,0       0t0        3 /dev/pts/0
bash    1387 root  254r   REG  253,0         9     1950 /path/redir.sh
bash    1387 root  255u   CHR  136,0       0t0        3 /dev/pts/0
[root@localhost ~]# lsof -i :1
[1]+  Done                    /path/redir.sh
[root@localhost ~]# lsof | grep redir
bash      1374         root  254r      REG              253,0         9       1950 /path/redir.sh

```
### 4.3. List all ESTABLISHED TCP connections ONLY with lsof
```bash
[root@localhost ~]# lsof -i tcp -s tcp:ESTABLISHED
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
sshd    1277 root    3u  IPv4  18585      0t0  TCP localhost.localdomain:ssh->192.168.0.116:50554 (ESTABLISHED)
sshd    1281 root    3u  IPv4  18649      0t0  TCP localhost.localdomain:ssh->192.168.0.116:50555 (ESTABLISHED)
```
