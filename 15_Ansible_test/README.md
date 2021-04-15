# Ansible 

#### Need to have >=3 VMs1.
__ansible__ 192.168.0.133  
__charybdis__ 192.168.0.121 
__scylla__ 192.168.0.120  

#### 1. On ansible install Ansible and create a user  
```bash
[root@localhost ~]# sudo yum install epel-release
[root@localhost ~]# sudo yum repolist
[root@localhost ~]# sudo yum install ansible
```
#### 1.1 Ansible install ssh key
```bash
[root@localhost ~]# ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa): /root/.ssh/ansible
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /root/.ssh/ansible.
Your public key has been saved in /root/.ssh/ansible.pub.
The key fingerprint is:
SHA256:3z6UKRPQW0KVthCvuFwR4r+6jhYX19lcwwtroHMwo9U root@localhost.localdomain
The key's randomart image is:
+---[RSA 2048]----+
|        .o=o...  |
|       ..*+E+. o.|
|        +.*Bo=o.o|
|       ..=+++oo. |
|        So*..o   |
|      ...+oo+    |
|       oo o+.    |
|      .. . ..    |
|     ...+.  ..   |
+----[SHA256]-----+
[root@localhost ~]# ssh-copy-id -i /root/.ssh/ansible.pub root@192.168.0.121
/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/root/.ssh/ansible.pub"
/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
root@192.168.0.121's password:
Permission denied, please try again.
root@192.168.0.121's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'root@192.168.0.121'"
and check to make sure that only the key(s) you wanted were added.

[root@localhost ~]# ssh-copy-id -i /root/.ssh/ansible.pub root@192.168.0.120
/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/root/.ssh/ansible.pub"
/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
root@192.168.0.120's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'root@192.168.0.120'"
and check to make sure that only the key(s) you wanted were added.

[root@localhost ~]# ansible -i hosts all -m ping
charybdis | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
scylla | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
```
#### 2.Using ansible ad-hoc create the same user on the rest of machines
```bash
[root@localhost ~]# ansible -i hosts all -m ansible.builtin.user -a "name=admin password={{ pass|password_hash('sha512') }}" -b -e "pass=0"
scylla | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": true,
    "comment": "",
    "create_home": true,
    "group": 1004,
    "home": "/home/admin",
    "name": "admin",
    "password": "NOT_LOGGING_PASSWORD",
    "shell": "/bin/bash",
    "state": "present",
    "system": false,
    "uid": 1004
}
charybdis | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": true,
    "comment": "",
    "create_home": true,
    "group": 1004,
    "home": "/home/admin",
    "name": "admin",
    "password": "NOT_LOGGING_PASSWORD",
    "shell": "/bin/bash",
    "state": "present",
    "system": false,
    "uid": 1004
}

```
#### 3.Setup SSH keys and sudo for that user
Created playbook for it [setup_admin.yml](https://raw.githubusercontent.com/DomenZero/DevOps_BigData/Ansible_test/15_Ansible_test/setup_admin.yml)  
```bash
[root@localhost ~]# touch admin_pass.yml
[root@localhost ~]# mkdir admin_dir
[root@localhost ~]# mv admin_pass.yml admin_dir
[root@localhost ~]# ssh-keygen -t rsa -f ./admin_dir/admin_rsa -q -N ''
[root@localhost ~]# ls -a ./admin_dir
.  ..  admin_pass.yml  admin_rsa  admin_rsa.pub

# Зашифровал

[root@localhost ~]# ansible-vault encrypt ./admin_dir/admin_pass.yml
New Vault password:
Confirm New Vault password:
Encryption successful
[root@localhost ~]# cat ./admin_dir/admin_pass.yml
$ANSIBLE_VAULT;1.1;AES256
30656539316365613163643134623138303961636262393064313634396234323735396134376335
3934666165656232363166363331663264313662303936610a376534373366373732376563373265
36343234613932366262326331633966316332653032333137646539316539386663383662616464
3634383834353037380a653430333662316261376566643037353335343034623966633232383031
3836
```
#### Write a playbook which:
Made playbook [install_admin.yml](https://raw.githubusercontent.com/DomenZero/DevOps_BigData/Ansible_test/15_Ansible_test/install_admin.yml)
- updates all packages on the systems
```yml
        - name: Update all software
          yum:
              name: '*'
              state: latest 
```
- installs NTP, Nginx and MySQL
```yml
        - name: Install the nginx, mysql
          yum:
              name: 
               - epel-release
               - nginx
               - mysql
               - python3
              state: latest  
        - name: Install nodejs
          yum:
              name: nodejs
              state: latest
        - name: Package mysql download
          get_url:
              url: https://dev.mysql.com/get/mysql80-community-release-el7-3.noarch.rpm
              dest: /tmp/mysql80-community-release-el7-3.noarch.rpm
              mode: 0660
              force_basic_auth: yes
        - name: RPM prepare
          yum:
              name: /tmp/mysql80-community-release-el7-3.noarch.rpm
              state: present
        - name: Install the MySQL packages
          yum:
              name:
                - mysql-server
                - mysql-community-server
                - mysql-community-client
                - python3-PyMySQL
                - python2-PyMySQL
```
- for NTP replaces default config with your own (you can find NTP server configs on the internet)
```yml
        - name: Replace ntp default config
          template:
              src: data/nginx.conf
              dest: /etc/nginx/nginx.conf
        - name: install pymysql
```
- or MySQL creates user and database (using corresponding module)
```yml
        - name: Setting up root credentials
          mysql_user:
              name: root
              host_all: yes
              password: '{{ db_root_old_pass }}'
              check_implicit_admin: true
        - name: Create a database
          mysql_db:
              login_user: root
              login_password: 'elf7!Alien'
              name: '{{ db_name }}'
              state: present
        - name: Create a database user
          mysql_user:
              name: admin
              password: '{{ db_admin_pass }}'
              priv: "{{ db_name }}.*:ALL"
              state: present
```
