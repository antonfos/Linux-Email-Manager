import crypt
import bcrypt

#===============================================================================
# Configure Logging
#===============================================================================
import logging
logger = logging.getLogger(__name__)


class pwdutil:

    enc = "$6$"
    salt = None

    def genSHA512(self, password):
        self.genSalt()
        return crypt.crypt(password, self.enc + self.salt)

    def chkSHA512(self, phash, passwd):
        return crypt.crypt(passwd, phash) == phash

    def genSalt(self):
        s = bcrypt.gensalt(20)
        x = s.split("$")
        salt = x[3][:16]
        self.salt = salt
        return salt