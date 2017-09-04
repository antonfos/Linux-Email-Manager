import os
from flask import Flask, Response
import logging
from logging.handlers import RotatingFileHandler 
# import mysql.connector
import config
from flask.ext.session import Session

app = Flask(__name__, static_url_path='')
app.config.from_object(config.DevelopmentConfig)
# app.secret_key = '\xbbac_\x057\x8d\xe2[E\xd0\xac\xb4[\x98\x18a{\xc3i\xf0\xe7i\x19'

#Session(app)
# print Session()

user = {}

dbconfig = {
    'user': app.config['MYSQL_DATABASE_USER'],
    'password': app.config['MYSQL_DATABASE_PASSWORD'],
    'host': app.config['MYSQL_DATABASE_HOST'],
    'database': app.config['MYSQL_DATABASE_DB'],
    'raise_on_warnings': True,
    'use_pure': False,
}
#===============================================================================
# Configure Logging
#===============================================================================
# Logging
logger = logging.getLogger(__name__)
logger.setLevel(4)
# create a logging format
handler = RotatingFileHandler("log/app.log", maxBytes=1000000, backupCount=5)
handler.setLevel(4)
# add the handlers to the logger
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Logger initilised")

# logger.debug("APP Variables %s " % app.config )

# db = mysql.connector.connect(**dbconfig)

#===============================================================================
# Import all the Views 
#===============================================================================
import master_views

#from appsrc.master_views import main
#app.register_blueprint(main)

@app.errorhandler(404)
def not_found(error):
    return Response(response="Oops, the page you are looking for does not exist", status=404)
    
@app.errorhandler(500)
def failure(error):
    return Response(response="Opps.. you have discovered an undocumented feature -- sorry!", status=500)

@app.errorhandler(401)
def err401(error):
    return Response(response="Not Authorised!", status=401)


logger.debug("APP Initialised ")

# sess = Session()
# sess.init_app(app)
