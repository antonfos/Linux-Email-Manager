from appsrc import dbconfig
import crypt
from appsrc.mailpwd import pwdutil
import mysql.connector

#===============================================================================
# Configure Logging
#===============================================================================
import logging
logger = logging.getLogger(__name__)

#
#+-------+-------------+------+-----+---------+----------------+
#| Field | Type        | Null | Key | Default | Extra          |
#+-------+-------------+------+-----+---------+----------------+
#| id    | int(11)     | NO   | PRI | NULL    | auto_increment |
#| name  | varchar(50) | NO   |     | NULL    |                |
#+-------+-------------+------+-----+---------+----------------+

class virtual_domains:
    table = "virtual_domains"
    con = None
    id = None
    name = None
    db = None

    def __init__(self):
        self.db = mysql.connector.connect(**dbconfig)
        self.con = self.db.cursor()
        logger.debug("[virtual_domains::__init__] INIT" )

    def getDomains(self, order = None, where = None):
        try:
            query = "SELECT `id`, `name`  FROM `%s` " % self.table
            if (where):
                query = query + " WHERE %s " % where 
            if (order):
                query = query + " ORDER BY `%s` " % order 

            #logger.debug("[virtual_domains::getDomains] Query : %s " % query)
            self.con.execute(query)    
            return self.con.fetchall()    
        except mysql.connector.Error as e:
            logger.debug("[virtual_domains::getDomains] failed %s" % str(e))
            return []


    def Insert(self, domain_name):
        # Insert a new record
        logger.debug("[virtual_domains::Insert] Domain : %s " % domain_name)
        if not self.checkDuplicatedomain(domain_name) or not domain_name :
            logger.debug("[virtual_domains::Insert] domain not unique or blank")
            return None
        try:
            query = "INSERT INTO `%s` (`name`) VALUES ('%s')" % (self.table, domain_name)
            logger.debug("[virtual_domains::Insert] Query : %s " % query)
            self.con.execute(query)
            dom_id = self.con.lastrowid
            self.db.commit()
            return dom_id
        except mysql.connector.Error as e:
            logger.debug("[virtual_domains::Insert] failed %s" % str(e))
            return None
       
    def Update(self, did, domain):
        logger.debug("[virtual_domains::Update] Domain : %s with ID %s" % (domain, did))
        try:
            query = "UPDATE `%s` SET `name` = '%s' WHERE `id` = %d" % (self.table, domain, did)
            logger.debug("[virtual_domains::Update] Query : %s " % query)
            self.con.execute(query)
            self.db.commit()
            return did
        except mysql.connector.Error as e:
            logger.debug("[virtual_domains::Update] failed %s" % str(e))
            return None

    def Delete(self, domain_id):
        logger.debug("[virtual_domains::Delete] Domain Id : %d " % domain_id)
        vuser = virtual_users()
        hasEmails = vuser.DomainHasEmails(domain_id)
        if hasEmails > 0:
            return hasEmails

        try:
            query = "DELETE FROM `%s` WHERE `id` = %d" % (self.table, domain_id)
            logger.debug("[virtual_domains::Delete] Query : %s " % query)
            self.con.execute(query)
            self.db.commit()
            return 0
        except mysql.connector.Error as e:
            logger.debug("[virtual_domains::Delete] failed %s" % str(e))
            return None



    def checkDuplicatedomain(self, domain_name):
        # check for an existing email
        logger.debug("[virtual_domains::checkDuplicateEmail] name %s " % domain_name)
        #query = "SELECT `id`, `email` FROM `virtual_users` WHERE `email` = '%s' " % email
        query = "SELECT count(*) as `cnt` FROM `%s` WHERE `name` = '%s' " % (self.table, domain_name)
        try:
            logger.debug("[virtual_domains::checkDuplicateEmail] Query : %s" % query)
            self.con.execute(query)
            res = self.con.fetchall()
            logger.debug("[virtual_domains::checkDuplicateEmail] result %s " % res)
            if res[0][0] > 0:
                return False
            return True
        except mysql.connector.Error as e:
            logger.debug("[virtual_domains::checkDuplicateEmail] failed %s" % str(e))
            return False

    def FetchDomain(self, domain_id, order):
        self.id = int(domain_id)
        if (self.id is 0):
            query = "SELECT * FROM `virtual_domains` " 
        else:
            query = "SELECT * FROM `virtual_domains` WHERE `id` = %d " % self.id
        
        if (order):
            query = query + " ORDER BY %s " % order

        try:
            logger.debug("[virtual_domains::FetchDomain] query : %s" % query)
            self.con.execute(query)
            logger.debug("2")
            res = self.con.fetchall()
            logger.debug("[virtual_domains::FetchDomain] result %s" % res)
            return res
            
        except mysql.connector.Error as e:
            logger.debug("[virtual_domains::FetchDomain] failed %s" % str(e))
            return None

    
#
#+-----------+--------------+------+-----+---------+----------------+
#| Field     | Type         | Null | Key | Default | Extra          |
#+-----------+--------------+------+-----+---------+----------------+
#| id        | int(11)      | NO   | PRI | NULL    | auto_increment |
#| domain_id | int(11)      | NO   | MUL | NULL    |                |
#| password  | varchar(106) | NO   |     | NULL    |                |
#| email     | varchar(100) | NO   | UNI | NULL    |                |
#| name      | varchar(100) | NO   |     | NULL    |                |
#+-----------+--------------+------+-----+---------+----------------+
class virtual_users:
    table = "virtual_users"
    con = None
    db = None

    def __init__(self):
        self.db = mysql.connector.connect(**dbconfig)
        self.con = self.db.cursor()
        logger.debug("[virtual_users::__init__] INIT" )

    def getUsers(self, order = None, where = None):
        try:
            query = "SELECT `id`, `domain_id`, `email`, `name`  FROM `%s` " % self.table
            if (where):
                query = query + " WHERE %s " % where 
            if (order):
                query = query + " ORDER BY `%s` " % order 

            #logger.debug("[virtual_users::getUsers] Query : %s " % query)
            self.con.execute(query)    
            return self.con.fetchall()    
        except mysql.connector.Error as e:
            logger.debug("[virtual_users::getUsers] failed %s" % str(e))
            return []
    

    def Insert(self, domain_id, emailname, username, password):
        logger.debug("[virtual_users::Insert] Domain_id : %s , emailname: %s , username: %s, password: %s" % (domain_id, emailname, username, password))
        # Insert a new record
        email = self.BuildEmailAddress(domain_id, emailname)
        logger.debug("[virtual_users::Insert] EMail Address %s " % email)

        logger.debug("[virtual_users::Insert] Is the email not duplicate %s" % self.checkDuplicateEmail(email))
        
        if not email or self.checkDuplicateEmail(email) > 0:
            return -1
        
        if password:
            pwdset = pwdutil()
            pwd = pwdset.genSHA512(password)
            query = "INSERT INTO `%s` (domain_id, email, password, name) VALUES (%d, '%s', '%s', '%s')" %(self.table,domain_id, email, pwd, username)
            logger.debug("[virtual_users::Insert] Query : %s " % query)
            self.con.execute(query)
            dom_id = self.con.lastrowid
            self.db.commit()
            return dom_id

       
    def Update(self, eid, name, password):
        logger.debug("[virtual_users::Update] email user : %s with ID %s , password %s" % (eid, eid, password))
        try:
            if (password):
                pwdset = pwdutil()
                pwd = pwdset.genSHA512(password)
            query = "UPDATE `%s` SET `name` = '%s' " % (self.table, name)

            if (password):
                pwdset = pwdutil()
                pwd = pwdset.genSHA512(password)
                query = query + ", `password` = '%s' " % pwd

            query = query + " WHERE `id` = %d " %  eid

            logger.debug("[virtual_users::Update] Query : %s " % query)
            self.con.execute(query)
            self.db.commit()
            return eid
        except mysql.connector.Error as e:
            logger.debug("[virtual_users::Update] failed %s" % str(e))
            # print "Error code:", e.errno        # error number
            # print "SQLSTATE value:", e.sqlstate # SQLSTATE value
            # print "Error message:", e.msg       # error message
            # print "Error:", e                   # errno, sqlstate, msg values
            # s = str(e)
            # print "Error:", s                   # errno, sqlstate, msg values
            # logging.warn('[virtual_users::Update] The MySQL database could not be read and returned the following error %s' % str(e))
            return -1


    def checkDuplicateEmail(self, email):
        # check for an existing email
        logger.debug("[virtual_users::checkDuplicateEmail] email %s " % email)
        #query = "SELECT `id`, `email` FROM `virtual_users` WHERE `email` = '%s' " % email
        #query = "SELECT count(*) as `cnt` FROM `%s` WHERE `email` = '%s' " % (self.table, email)
        query = "SELECT id FROM `%s` WHERE `email` = '%s' " % (self.table, email)
        try:
            logger.debug("[virtual_users::checkDuplicateEmail] Query : %s" % query)
            self.con.execute(query)
            s = self.con.fetchall()
            numrows = len(s)
            logger.debug("[virtual_users::checkDuplicateEmail] rowcount %s" % numrows)
            return numrows

        except mysql.connector.Error as e:
            # print "Error code:", e.errno        # error number
            # print "SQLSTATE value:", e.sqlstate # SQLSTATE value
            # print "Error message:", e.msg       # error message
            # print "Error:", e                   # errno, sqlstate, msg values
            # s = str(e)
            # print "Error:", s                   # errno, sqlstate, msg values
            logger.debug("[virtual_users::checkDuplicateEmail] failed : %s" % str(e))
            return False

    def DomainHasEmails(self, domain_id):
        # check for an existing email
        logger.debug("[virtual_users::DomainHasEmails] domain_id %s " % domain_id)
        query = "SELECT count(*) as `cnt` FROM `%s` WHERE `domain_id` = %s " % (self.table, domain_id)
        try:
            logger.debug("[virtual_users::DomainHasEmails] Query : %s" % query)
            self.con.execute(query)
            logger.debug("[virtual_users::DomainHasEmails] 2")
            res = self.con.fetchall()
            logger.debug("[virtual_users::DomainHasEmails] result %s " % res)
            if res[0][0] > 0:
                return res[0][0]
            return 0
        except mysql.connector.Error as e:
            logger.debug("[virtual_users::DomainHasEmails] failed %s" % str(e))
            return 0
        

    def BuildEmailAddress(self, domain_id, emailname):
        # Build an email address
        domain = self.getDomain(domain_id)
        logger.debug("[virtual_users::BuildEmailAddress] domain %s" % domain)
        if domain :
            return emailname+"@"+domain[0][1]
        return None

    def getDomain(self, domain_id):
        # Fetch The Domain
        vmod = virtual_domains()
        domain = vmod.FetchDomain(domain_id, None)
        return domain

    def emailsByDomain(self, domain_id):
        logger.debug("[virtual_users::emailsByDomain] domain_id %s " % domain_id)
        query = "SELECT `id`, `domain_id`, `email`, `name` FROM `%s` WHERE `domain_id` = %s " % (self.table, domain_id)
        try:
            logger.debug("[virtual_users::emailsByDomain] Query : %s" % query)
            self.con.execute(query)
            res = self.con.fetchall()
            logger.debug("[virtual_users::emailsByDomain] result %s " % res)
            return res
        except mysql.connector.Error as e:
            logger.debug("[virtual_users::emailsByDomain] failed %s" % str(e))
            return []


    def Delete(self, email_id):
        logger.debug("[virtual_users::Delete] email Id : %d " % email_id)
        vuser = virtual_users()
        
        try:
            query = "DELETE FROM `%s` WHERE `id` = %d" % (self.table, email_id)
            logger.debug("[virtual_users::Delete] Query : %s " % query)
            self.con.execute(query)
            self.db.commit()
            return 0
        except mysql.connector.Error as e:
            logger.debug("[virtual_users::Delete] failed %s" % str(e))
            return -1

    def DeleteDomainUsers(self, domain_id):
        logger.debug("[virtual_users::DeleteDomainUsers] Domain Id : %d " % domain_id)
        vuser = virtual_users()
        
        try:
            query = "DELETE FROM `%s` WHERE `domain_id` = %d" % (self.table, domain_id)
            logger.debug("[virtual_users::DeleteDomainUsers] Query : %s " % query)
            self.con.execute(query)
            self.db.commit()
            return 0
        except mysql.connector.Error as e:
            logger.debug("[virtual_users::DeleteDomainUsers] failed %s" % str(e))
            return None

#
#+-------------+--------------+------+-----+---------+----------------+
#| Field       | Type         | Null | Key | Default | Extra          |
#+-------------+--------------+------+-----+---------+----------------+
#| id          | int(11)      | NO   | PRI | NULL    | auto_increment |
#| domain_id   | int(11)      | NO   | MUL | NULL    |                |
#| source      | varchar(100) | NO   |     | NULL    |                |
#| destination | varchar(100) | NO   |     | NULL    |                |
#+-------------+--------------+------+-----+---------+----------------+

class virtual_aliases:
    table = "virtual_aliases"
    con = None
    db = None

    def __init__(self):
        self.db = mysql.connector.connect(**dbconfig)
        self.con = self.db.cursor()
        logger.debug("[virtual_aliases::__init__] INIT" )

    def getAliias(self, order = None, where = None):
        try:
            query = "SELECT `id`, `domain_id`, `source`, `destination`  FROM `%s` " % self.table
            if (where):
                query = query + " WHERE %s " % where 
            if (order):
                query = query + " ORDER BY `%s` " % order 

            #logger.debug("[virtual_aliases::getAliias] Query : %s " % query)
            self.con.execute(query)    
            return self.con.fetchall()    
        except mysql.connector.Error as e:
            logger.debug("[virtual_aliases::getAliias] failed")
            logging.debug('The MySQL database could not be read and returned the following error %s' % str(e))
            return []
