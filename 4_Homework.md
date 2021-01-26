# 1. Processes
1.1 Run a sleep command three times at different intervals
```bash
[jones@localhost share]$ sleep 2
[jones@localhost share]$ sleep 0.5s
[jones@localhost share]$ sleep 3m
```
1.2. Send a SIGSTOP signal to all of them in three different ways.
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
1.3. Check their statuses with a job command
```bash
[jones@localhost share]$ pmap 1870
[1]+  Done                    sleep 2m > /dev/null
```
1.4. Terminate one of them. (Any)
```bash
[jones@localhost share]$ ps aux | awk '/sleep/{print $2}' | xargs kill -9
kill: sending signal to 1924 failed: No such process
[1]   Killed                  sleep 2m > /dev/null
[2]-  Killed                  sleep 2m > /dev/null
[3]+  Killed                  sleep 2m > /dev/null
```
1.5. To other send a SIGCONT in two different ways.
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
1.6. Kill one by PID and the second one by job ID

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
