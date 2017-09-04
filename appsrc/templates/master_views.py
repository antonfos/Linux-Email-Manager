from app import app, mysql
from flask import request, redirect, jsonify, session, make_response, flash, render_template,url_for
from jinja2 import TemplateNotFound

#===============================================================================
# Configure Logging
#===============================================================================
import logging
logger = logging.getLogger(__name__)


@app.route('/')
@app.route('/index')
#@login_required
#@user_validated
def index():
    #br = Browser(request)
    cs = []
    sc = [url_for('', filename="")] 
    logger.debug("sc: %s", sc)
    logger.debug("Render template dashboard.html")

    stats = {"st":"PV", "data":{"page": "dashboard"}}
    
    try:
        return render_template('index.html', title='Home', cs=cs, sc=sc, mod=True) 
    except TemplateNotFound:
        logger.error("[index] Template not Found")
        return "Template not Found"