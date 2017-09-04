import os
from flask import Flask, render_template
from flaskext.mysql import MySQL
import logging
from logging.handlers import RotatingFileHandler 
from jinja2 import TemplateNotFound


app = Flask(__name__, static_url_path='')
app.config.from_object(os.environ['APP_SETTINGS'])


#===============================================================================
# Configure Logging
#===============================================================================
#print(app.LOGLEVEL)
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

 
mysql = MySQL()

#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'k3lsam'
#app.config['MYSQL_DATABASE_DB'] = 'mailserver'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



print(os.environ['APP_SETTINGS'])

#===============================================================================
# Import all the Views 
#===============================================================================
from views import master_views

# @app.route('/')
# def hello():
#     return render_template('views.index.html')


# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()




