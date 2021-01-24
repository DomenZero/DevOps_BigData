# 1.

### 1.1. Создание группы sales с GID 4000
```bash
[root@localhost shared-folder]# groupadd -g 4000 sales
[root@localhost shared-folder]# cat /etc/group | tail -1
sales:x:4000:
```
### 1.2. Создание пользователей bob, alice, evec основной группой sales
```bash

```
### 1.3. Правило смены пароля, каждые 30 дней
Изменить PASS_MAX_DAYS на 30 в файле 
