# Linux-Email-Manager
A small Flask program to manage the MySql database for a Linux Postfix Dovcote mail server configuration based on [Email with Postfix, Dovecot, and MySQL](https://www.linode.com/docs/email/postfix/email-with-postfix-dovecot-and-mysql)

### Database Tables
#### virtual_domains
```
CREATE TABLE virtual_domains (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(50) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
```
#### virtual_users
```
CREATE TABLE virtual_users (
  id int(11) NOT NULL AUTO_INCREMENT,
  domain_id int(11) NOT NULL,
  password varchar(106) NOT NULL,
  email varchar(100) NOT NULL,
  name varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email (email),
  KEY domain_id (domain_id),
  CONSTRAINT virtual_users_ibfk_1 FOREIGN KEY (domain_id) REFERENCES virtual_domains (id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
```

#### virtual_aliases
```
CREATE TABLE virtual_aliases (
  id int(11) NOT NULL AUTO_INCREMENT,
  domain_id int(11) NOT NULL,
  source varchar(100) NOT NULL,
  destination varchar(100) NOT NULL,
  PRIMARY KEY (id),
  KEY domain_id (domain_id),
  CONSTRAINT virtual_aliases_ibfk_1 FOREIGN KEY (domain_id) REFERENCES virtual_domains (id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
```

## Create a user for the application on MySql 

```
CREATE USER 'mailadmin'@'localhost' IDENTIFIED BY 'MySuperSecretPassword';
GRANT ALL PRIVILEGES ON mailserver . * TO 'mailadmin'@'localhost';
FLUSH PRIVILEGES;
```

### Set the password in config.py

```
    MYSQL_DATABASE_USER = 'mailadmin'
    MYSQL_DATABASE_PASSWORD = 'MySuperSecretPassword'
    MYSQL_DATABASE_DB = 'mailserver'
    MYSQL_DATABASE_HOST = 'localhost'
```
## Create the Log and Sessions directories

python run.py
