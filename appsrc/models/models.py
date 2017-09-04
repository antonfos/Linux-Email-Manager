from appsrc import db


class virtual_domains(db.Model):
    __tablename__ = 'virtual_domains'
    out = "std"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    def __init__(self, out, id, name):
        self.id = id
        self.name = name
        self.out = out

    def __repr__(self):
        if self.out == "std":
            return  '{"id": %d , "name": "%s" }'  % (self.id, self.name)
        else:
            return  '<vdom( %d ,  "%s" )'  % (self.id, self.name)
            #return  '(%d ,%s)'  % (self.id, self.name)


class virtual_users(db.Model):
    __tablename__ = 'virtual_users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain_id = db.Column(db.Integer, default=0, nullable=False)
    password = db.Column(db.String(106), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, id, name, domain_id, password, email):
        self.id = id
        self.name = name
        self.domain_id = domain_id
        self.password = password
        self.email = email

    def __repr__(self):
        return '{"id" : %d, "domain_id": %d ,"email": %s, "name": %s}' % (self.id, self.domain_id , self.email, self.name)



class virtual_aliases(db.Model):
    __tablename__ = 'virtual_aliases'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain_id = db.Column(db.Integer, default=0, nullable=False)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)

    def __init__(self, id, domain_id, destination):
        self.id = id
        self.domain_id = domain_id
        self.source = source
        self.destination = destination

    def __repr__(self):
        return '{"id" : %d, "domain_id": %d ,"source": %s, "destination": %s}' % (self.id, self.domain_id , self.source, self.destination)
    