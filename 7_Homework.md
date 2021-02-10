# Bash
### 1. Find a sum of all running process' PIDs
```bash
[root@mitnik bash_test]# cat 1.sh
#!/bin/bash -x
ps -ef | awk '{ pd=$2 ; sum +=pd} END {print sum}'

[root@mitnik bash_test]# chmod +x 1.sh
[root@mitnik bash_test]# ./1.sh
+ awk '{ pd=$2 ; sum +=pd} END {print sum}'
+ ps -ef
42767

```
### 2. A lucky number is one whose individual digits add up to 7, in successive additions. For example, 62431 is a lucky number (6 + 2 + 4 + 3 + 1 = 16, 1 + 6 = 7). 
Find all the lucky numbers between 1000 and 10000.

```bash
#!/bin/bash -x
check=7
for (( x=1000; x<10000; x++)); do
        b=$x
        len=${#x}
        while [ $x -gt $check ]; do
                for (( i=0; i<len; i++ )); do
                        ((sum+=x%10))
                        ((x/=10))
                done
                x=$sum
                len=${#x}
                if [[ x -lt $check ]]; then
                        break;
                elif [[ x%7 -eq 0 ]] && [[ x -eq $check ]]; then
                        echo "Lucky $b";
                        break;
                elif [[ len -eq 1 ]] && [[ x -lt $check ]] || [[ x%7 -lt $check  ]]; then
                        break;
                fi
                sum=0
        done
        x=$b
        sum=0
done
```
```bash
Test without debug
[root@mitnik bash_test]# ./2.sh
Lucky 1006
Lucky 1015
Lucky 1024
Lucky 1033
Lucky 1042
Lucky 1051
Lucky 1060
Lucky 1105
Lucky 1114
Lucky 1123
Lucky 1132
Lucky 1141
Lucky 1150
Lucky 1204
Lucky 1213
Lucky 1222
Lucky 1231
Lucky 1240
Lucky 1303
Lucky 1312
Lucky 1321
Lucky 1330
Lucky 1402
Lucky 1411
Lucky 1420
Lucky 1501
Lucky 1510
Lucky 1600
Lucky 2005
Lucky 2014
Lucky 2023
Lucky 2032
Lucky 2041
Lucky 2050
Lucky 2104
Lucky 2113
Lucky 2122
Lucky 2131
Lucky 2140
Lucky 2203
Lucky 2212
Lucky 2221
Lucky 2230
Lucky 2302
Lucky 2311
Lucky 2320
Lucky 2401
Lucky 2410
Lucky 2500
Lucky 3004
Lucky 3013
Lucky 3022
Lucky 3031
Lucky 3040
Lucky 3103
Lucky 3112
Lucky 3121
Lucky 3130
Lucky 3202
Lucky 3211
Lucky 3220
Lucky 3301
Lucky 3310
Lucky 3400
Lucky 4003
Lucky 4012
Lucky 4021
Lucky 4030
Lucky 4102
Lucky 4111
Lucky 4120
Lucky 4201
Lucky 4210
Lucky 4300
Lucky 5002
Lucky 5011
Lucky 5020
Lucky 5101
Lucky 5110
Lucky 5200
Lucky 6001
Lucky 6010
Lucky 6100
Lucky 7000

```
### 3.  Write a script that takes a list of words (or even phrases) as an arguments. 
Script should ask a user to write something to stdin until user won't provide one of argument phrases.
```bash 
#!/bin/bash -x

declare -a StringArray=("Linux" "CentOS" "Windows" "Ubuntu" "Debian" )
check=0
while [ $check != 1 ]; do
        read -p 'Enter my favourite word or phrase: ' line
        for word in ${StringArray[@]}; do
                if [[ $word == $line ]]; then
                        check=1;
                        echo "Yes, this is my favourite word! Thank you, bye! $word";
                        break;
                else
                        echo "No, it's not what I want!"
                fi
        done
        if [[ check -eq 1 ]]; then
                break;
                end
        fi
done
```
```bash
Test

[root@mitnik bash_test]# ./3.sh
+ StringArray=("Linux" "CentOS" "Windows" "Ubuntu" "Debian")
+ declare -a StringArray
+ check=0
+ '[' 0 '!=' 1 ']'
+ read -p 'Enter my favourite word or phrase: ' line
Enter my favourite word or phrase: CentOS
+ for word in '${StringArray[@]}'
+ [[ Linux == CentOS ]]
+ echo 'No, it'\''s not what I want!'
No, it's not what I want!
+ for word in '${StringArray[@]}'
+ [[ CentOS == CentOS ]]
+ check=1
+ echo 'Yes, this is my favourite word! Thank you, bye! CentOS'
Yes, this is my favourite word! Thank you, bye! CentOS
+ break
+ [[ check -eq 1 ]]
+ break
```
### 4. As bash doesn't have any syntax standardisation a lot of bash users develop scripts that make further readers very unhappy. Also, these guys often over 
engineers such scripts. This is an example of this script. Please analyse a script and try to make it as readable and functional as possible from your sense of beauty.
```bash
export SUM=0;
for f in $(find src -name "*.java");
    do 
        export SUM=$(($SUM + $(wc -l $f | awk '{ print $1 }')));    
    done; 
echo $SUM
```
### 5. `stat` command shows when a particular file was accessed. Unfortunately, it can't show who it was. 
As a first step, you should study a Shell Variables section of man bash, enable an unlimited history size and time stamping of command execution.
*Solution
Added HISTFILESIZE and HISTSIZE
```bash
[root@mitnik bash_test]# cat ~/.bashrc
cat ~/.bashrc
# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

export HISTFILESIZE=
export HISTSIZE=

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi
```
# RegEx
### 1. Write a sed one-liner that will show stack traces lines in the following fashion:

### 2. Write a RegEx that validates entries under `/etc/passwd`.
```regex
/^[a-z0-9-]*[$]?:[^:]?:[0-9]+:[0-9]+:[^:]*:[^:]*:[^:]*$/
```

### 3. Write a RegEx that will validate URI:
```regex
/(http|https):\/\/[\w]+(\.(\w+).+(\/|))+(\w|\/)?/
```
