# Linux-Email-Manager
A small Flask program to manage the MySql database for a Linux Postfix Dovcote mail server configuration based on [Email with Postfix, Dovecot, and MySQL](https://www.linode.com/docs/email/postfix/email-with-postfix-dovecot-and-mysql)

### Database Tables
#### virtual_domains
'''
+-------+-------------+------+-----+---------+----------------+
| Field | Type        | Null | Key | Default | Extra          |
+-------+-------------+------+-----+---------+----------------+
| id    | int(11)     | NO   | PRI | NULL    | auto_increment |
| name  | varchar(50) | NO   |     | NULL    |                |
+-------+-------------+------+-----+---------+----------------+
'''
#### virtual_users
'''
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| id        | int(11)      | NO   | PRI | NULL    | auto_increment |
| domain_id | int(11)      | NO   | MUL | NULL    |                |
| password  | varchar(106) | NO   |     | NULL    |                |
| email     | varchar(100) | NO   | UNI | NULL    |                |
| name      | varchar(100) | NO   |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+
'''

#### virtual_aliases
'''
+-------------+--------------+------+-----+---------+----------------+
| Field       | Type         | Null | Key | Default | Extra          |
+-------------+--------------+------+-----+---------+----------------+
| id          | int(11)      | NO   | PRI | NULL    | auto_increment |
| domain_id   | int(11)      | NO   | MUL | NULL    |                |
| source      | varchar(100) | NO   |     | NULL    |                |
| destination | varchar(100) | NO   |     | NULL    |                |
+-------------+--------------+------+-----+---------+----------------+
'''

## Create a user for the application on MySql 

'''
CREATE USER 'mailadmin'@'localhost' IDENTIFIED BY 'MySuperSecretPassword';
GRANT ALL PRIVILEGES ON mailserver . * TO 'mailadmin'@'localhost';
FLUSH PRIVILEGES;
'''

### Set the password in config.py

'''
    MYSQL_DATABASE_USER = 'mailadmin'
    MYSQL_DATABASE_PASSWORD = 'MySuperSecretPassword'
    MYSQL_DATABASE_DB = 'mailserver'
    MYSQL_DATABASE_HOST = 'localhost'
'''
## Creeate the Log and Sessions directories

python run.py