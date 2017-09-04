from appsrc import app, dbconfig, user, Session
from flask import request, redirect, jsonify, session, make_response, flash, render_template, url_for  #, Blueprint
from jinja2 import TemplateNotFound
import json
from models.datamodels import virtual_domains, virtual_users, virtual_aliases
from appsrc.mailpwd import pwdutil
import pprint
from appsrc.decorators import user_validated
from flask.ext.session import Session 
import mysql.connector

sess = Session()
sess.init_app(app) 

static_folder ="static"
template_folder="templates"

#===============================================================================
# Configure Logging
#===============================================================================
import logging
logger = logging.getLogger(__name__)

################# Authentication ##################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Sign In') 
        
    pwdset = pwdutil()
    pwdok = pwdset.chkSHA512( app.config['ADMIN_PASSWORD'], request.form['password'])
    if pwdok and request.form['username'] == app.config['ADMIN_USER']:
        user = {"name": "Adminsitrator", "user_id": 0, app.config['ADMIN_USER'] : True, "authenticated" : True}
        session.permanent = False
        session.clear()
        
        session['name'] = "Administrator"
        session['user_id'] = 0
        session['admin'] = True
        session["authenticated"] = True
        return redirect("/")
    
    logger.debug("Login UNSuccessfull Username %s : pass %s, PassOk %s" % (request.form['username'], request.form['password'], pwdok))
    flash("Invaild Login", "error")
    return redirect("/login")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    logger.debug("[views::logout] Session keys %s" % session.keys())
    session.pop('name', None)
    session.pop('user_id', None)
    session.pop('admin', None)
    session.pop('authenticated', None)
    session.clear()
    user = {}
    return redirect("/")

################# Auth End #########################

# Main Page
@app.route('/')
@app.route('/index')
# @user_validated
def index():
    logger.debug("[views::index] Session authenticated %s" % session.get('authenticated'))
    logger.debug("[views::index] Session perm %s" % session.get('_permanent'))
    vtable = virtual_domains()
    domn = vtable.getDomains('name', None)
    #logger.debug("domains : %s" % domn)

    vtable = virtual_users()
    emails = vtable.getUsers('domain_id', None)
    #logger.debug("Emails : %s" % emails)

    vtable = virtual_aliases()
    alias = vtable.getAliias('source', None)
    #logger.debug("Aliases : %s" % alias)
    
    #logger.debug("Render template index.html")

    try:
        return render_template('index.html', title='Home', emails = emails, domn = domn, alias = alias) 
        # return redirect(url_for("index"))
    except TemplateNotFound:
        logger.error("[index] Template not Found")
        return "Template not Found ... "

# Route to manage domains view

@app.route('/managedomains', methods=['GET'])
@user_validated
def mandom():
    vtable = virtual_domains()
    domn = vtable.getDomains('name', None)
    logger.debug("domains : %s" % domn)

    js = ["/js/domains.js"]
    try:
        return render_template('domain.html', title='Domains', domn = domn, js = js) 
    except TemplateNotFound:
        logger.error("[index] Template not Found")
        return "Template not Found ... "

# Ajax Route to retriev a single domain
@app.route('/domain/id/<int:domain_id>', methods=['GET'])
#@user_validated
def getDomain(domain_id):
    ip = request.remote_addr
    logger.debug("getDomain %s " % domain_id)
    if id is None:
        return jsonify({"status": False, "data": None})
    if (int(domain_id) == 0):
        where  = None
    else:
        where = "id = %s" % domain_id

    vtable = virtual_domains()
    
    try:

        domn = vtable.getDomains('name', where)
        logger.debug("domains : %s" % domn)

        if domn :
            return jsonify({"status": True, "data": domn})
        else :
            return jsonify({"status": True, "data": None})
    except:
        logger.debug("getDomain with domain_id of %s failed " % domain_id)
        return jsonify({"status": False, "data": None})
    

# Domain Form submit
@app.route('/domain', methods=['POST', 'DELETE'])
@user_validated
def setDomain():
    IsAjax = request.is_xhr
    vdomain = virtual_domains()
    method = request.form.get('_method', "POST")
    domain_id = int(request.form.get('id', "0"))
    domain = request.form.get('name', None)
    logger.debug("Saving %s of id %d with Method: %s" %(domain, domain_id, method) )
    # con = db.cursor()
    if method == "DELETE":
        #domain_id = int(request.form.get('id', "0"))
        #vdomain = virtual_domains()
        res = vdomain.Delete(domain_id)
        logger.debug("[views::delDomain] res %d" %res)

        if res is 0:
            flash("Domain Deleted ok", "success")

        if res > 0:
            flash("Can not delete domain, still %s active email address!" % res, "error")

        if res < 0:
            flash("Delete failed", "error")
        return redirect("/managedomains")

    if method == "POST":
        if (domain_id is 0):
            # Insert New Domain
            print "Insert Domain"
            try:
                r = vdomain.Insert(domain)
                if not r:
                    logger.debug("Insert failed %s " % r)
                    return redirect("/managedomains")     

                flash('domain Insert successfull', "success")
                return redirect("/managedomains")
            except :
                logger.debug("Error Inserting virtual_domains ")
                print "Error on Insert"
                flash('domain Insert unsuccessfull', "error")
                return redirect("/managedomains")
        else:
            # Update the Domain
            logger.debug( "Update domain | Domain ID : %s, Domain Name : %s" % (domain_id, domain) )
            try:
                r = vdomain.Update(domain_id, domain)
                flash('domain Update successfull', "success")
                return redirect("/managedomains")
            except :
                logger.debug("Error Updating virtual_domains ")
                flash('domain Update unsuccessfull', "error")
                return redirect("/managedomains")
    flash('domain Update/Insert unsuccessfull', "error")
    return redirect("/managedomains")

# Emails #

@app.route('/emails', methods=['GET'])
@user_validated
def Emails():
    db = mysql.connector.connect(**dbconfig)
    con = db.cursor()
    query = "select id, name, email from virtual_users order by email" 
    con.execute(query)
    emails = con.fetchall()
    query = "select id, name from virtual_domains order by name" 
    con.execute(query)
    domn = con.fetchall()
    js = ["/js/emails.js"]
    try:
        return render_template('emails.html', title='Emails', emails = emails, js = js, domn = domn) 
    except TemplateNotFound:
        logger.error("[index] Template not Found")
        return "Template not Found ... "

@app.route('/emails/<int:email_id>', methods=['GET'])
@user_validated
def GetEmails(email_id):
    # logger.debug("Getting Email list %d", email_id)
    if (int(email_id) == 0):
        where = None
    else:
        where = " `id` = %d" % int(email_id)

    vtable = virtual_users()

    try:
        email = vtable.getUsers('email', where)
        # logger.debug("[views::GetEmails] emails : %s" % email)
        if email :
            return jsonify({"status": True, "data": email})
        else :
            return jsonify({"status": True, "data": None})
    except :
        return jsonify({"status": False, "data": None})
    
    

@app.route('/email/<int:domain_id>/domain', methods=['GET'])
@user_validated
def GetEmailByDomain(domain_id):
    logger.debug("Domain ID %s" % domain_id)
    db = mysql.connector.connect(**dbconfig)
    con = db.cursor()
    if (int(domain_id) == 0):
        query = "SELECT `id`, `domain_id` ,`name`, `email` FROM `virtual_users` ORDER BY email"
    else:
        query = "SELECT `id`, `domain_id` ,`name`, `email` FROM `virtual_users` WHERE `domain_id` = %d ORDER BY `email`" % int(domain_id) 
    logger.debug("URL : %s" % query)
    try:
        con.execute(query)
        emails = con.fetchall()
        if emails :
            return jsonify({"status": True, "data": emails})
        else :
            return jsonify({"status": True, "data": None})
    except:
        logger.error("GetEmailsByDomain Error")
        return jsonify({"status": False, "data": None})

@app.route('/savemail', methods=['POST'])
@user_validated
def setEmail():
    virtuser = virtual_users()
    method = request.form.get('_method', "POST")
    email_id = int(request.form.get('id', "0"))
    domain_id = int(request.form.get('domain_id', "0"))
    email = request.form.get('email', None)
    name = request.form.get('name', None)
    password = request.form.get('password', None)

    if method == "DELETE":
        # logger.debug("Deleting email id %d" % email_id)
        
        res = virtuser.Delete(email_id)
        # logger.debug("[views::DelEmail] res %d" %res)

        if res is 0:
            flash("Email Deleted ok", "success")

        if res < 0:
            flash("Delete email failed", "error")

        if res > 0:
            flash("Failed to delete email, there are still %d aliases pointing to this email address" % res, "error")

        return redirect("/emails")

    # logger.debug("[views::setEmail] Saving email address %s for user %s with password %s (domain: %s)" %(email, name,password, domain_id ) )

    if (domain_id is 0 or not email or not name):
        logger.debug("[views::setEmail] invalid parameters")
        flash('Email Insert unsuccessfull - Invalid / incomplete data', "error")
        return redirect("/emails")

    if (email_id is 0):
        if (len(password) < 8 or not password ):
            flash('Email Insert unsuccessfull - Invalid Password, password must be 8 characters or more', "error")
            return redirect("/emails")

        newemail = virtuser.Insert(domain_id, email, name, password)
        # logger.debug("[views::setEmail] New Email user id %s " % newemail)
        if (newemail < 0):
            flash('Email Insert unsuccessfull - Duplicate Email / Alias', "error")
        else:
            flash("Email save successfull", 'success')
        return redirect("/emails")
    elif (email_id > 0):
        up = virtuser.Update(email_id, name, password)
        if (up < 0):
            flash("Email Update unsuccessfull ", "error")
        else :
            flash("Email save successfull", 'success')
            return redirect("/emails")
    else :
        flash("Email save unsuccessfull!!", 'error')
        return redirect("/emails")


@app.route("/aliases", methods=['GET'])
@user_validated
def manageAliases():
    valias = virtual_aliases()
    aliases = valias.getAliias('source', None)
    
    js = ["/js/aliases.js"]
    try:
        return render_template('aliases.html', title='Aliases', aliases = aliases, js = js) 
    except TemplateNotFound:
        logger.error("[index] Template not Found")
        return "Template not Found ... "


@app.route('/emailsbydomain/<int:domain_id>', methods=['GET'])
@user_validated
def getEmailsByDomain(domain_id):
    # logger.debug("Getting Email list for domain  %d", domain_id)
    if domain_id == 0:
        return jsonify({"status": False, "data": None}) 

    vtable = virtual_users()

    try:
        emails = vtable.emailsByDomain(domain_id)
        logger.debug("[views::getEmailsByDomain] emails : %s" % emails)
        if emails :
            return jsonify({"status": True, "data": emails})
        else :
            return jsonify({"status": True, "data": None})
    except :
        return jsonify({"status": False, "data": None})

@app.route('/savealias', methods=['POST'])
@user_validated
def setAlias():
    virtalias = virtual_aliases()
    method = request.form.get('_method', "POST")        # Method (POST / DELETE)
    alias_id = int(request.form.get('id', 0))           # Alias record ID
    domain_id = int(request.form.get('domain_id', 0))   # Domain Id
    source = request.form.get('source', None)           # Email address (Without the domain)
    destination = request.form.get('destination', None) # Destination Email Address
    

    if method == "DELETE":
        logger.debug("Deleting alias id %d" % alias_id)
        
        res = virtalias.Delete(alias_id)
        # logger.debug("[views::Delalias] res %d" %res)

        if res is 0:
            flash("Alias Deleted ok", "success")

        if res < 0:
            flash("Delete alias failed", "error")
        return redirect("/aliases")

    logger.debug("[views::setAlias] Saving alias address %s redirected to  %s for ID: %d (domain: %s)" %(source, destination, alias_id, domain_id ) )

    if (domain_id is 0 or not source or not destination):
        logger.debug("[views::setAlias] invalid parameters")
        flash('Alias add unsuccessfull - Invalid / incomplete data', "error")
        return redirect("/aliases")

    if (alias_id is 0):
       
        newalias = virtalias.Insert(domain_id, source, destination)
        logger.debug("[views::setAlias] New Alias id %s " % newalias)
        if (newalias < 0):
            flash('Alias Insert unsuccessfull - Duplicate Alias / Email', "error")
        else:
            flash("Alias save successfull", 'success')
        return redirect("/aliases")
    elif (alias_id > 0):
        up = virtalias.Update(alias_id, destination)
        if (up < 0):
            flash("Alias Update unsuccessfull ", "error")
        else :
            flash("Alias save successfull", 'success')
            return redirect("/aliases")
    else :
        flash("Alias save unsuccessfull!!", 'error')
        return redirect("/aliases")

@app.route('/fetchalias/<int:alias_id>', methods=['GET'])
@user_validated
def fetchAlias(alias_id):
    # logger.debug("Fetching alias id : %d" % alias_id);
    virtalias = virtual_aliases()
    where = None

    if alias_id > 0:
        where = " id = %d " % alias_id

    aliases = virtalias.getAliias("source", where)

    # logger.debug("[views::fetchAlias] result : %s " % aliases)

    return jsonify({"status": True, "data": aliases })
    # return virtalias.getAliias("source", where)




@app.route('/test', methods=['GET'])
@user_validated
def test():
    return "Success"