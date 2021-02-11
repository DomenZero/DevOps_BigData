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
el_count=0
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
                        ((el_count+=1));
                        break;
                elif [[ len -eq 1 ]] && [[ x != $check  ]]; then
                        break;
                fi
                sum=0
        done
        x=$b
        sum=0

done
echo $el_count
```
```bash
Test without debug
[root@mitnik bash_test]# ./2.sh > 7_hw_2_lucky.log
```
[7_hw_2_lucky.log](/log/7_hw_2_lucky.log)
### 3.  Write a script that takes a list of words (or even phrases) as an arguments. 
Script should ask a user to write something to stdin until user won't provide one of argument phrases.
```bash 
#!/bin/bash -x

declare -a StringArray=($1 $2 $3)
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

[root@mitnik bash_test]# ./3.sh linux windows macos
+ StringArray=($1 $2 $3)
+ declare -a StringArray
+ check=0
+ '[' 0 '!=' 1 ']'
+ read -p 'Enter my favourite word or phrase: ' line
Enter my favourite word or phrase: ubuntu
+ for word in '${StringArray[@]}'
+ [[ linux == ubuntu ]]
+ echo 'No, it'\''s not what I want!'
No, it's not what I want!
+ for word in '${StringArray[@]}'
+ [[ windows == ubuntu ]]
+ echo 'No, it'\''s not what I want!'
No, it's not what I want!
+ for word in '${StringArray[@]}'
+ [[ macos == ubuntu ]]
+ echo 'No, it'\''s not what I want!'
No, it's not what I want!
+ [[ check -eq 1 ]]
+ '[' 0 '!=' 1 ']'
+ read -p 'Enter my favourite word or phrase: ' line
Enter my favourite word or phrase: linux
+ for word in '${StringArray[@]}'
+ [[ linux == linux ]]
+ check=1
+ echo 'Yes, this is my favourite word! Thank you, bye! linux'
Yes, this is my favourite word! Thank you, bye! linux
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
