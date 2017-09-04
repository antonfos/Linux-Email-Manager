from functools import wraps
from flask import g, flash, redirect, url_for, request, session
from appsrc import user

#===============================================================================
# Configure Logging
#===============================================================================
import logging
logger = logging.getLogger(__name__)

#===============================================================================
# Is user validated decorator
#===============================================================================
def user_validated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.debug("[@user_validated] Session keys %s" % session.keys())
        if 'authenticated' in session.keys() :
            logger.debug("[@user_validated] Session keyAuth %s" % session.get('authenticated', False) )
            if not session.get('authenticated', False):
                flash(u'The page you are requested is restricted.')
                return redirect("/login")
        else:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# def user_validated(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         logger.debug("[@user_validated] User keys %s" % user.keys())
#         if 'authenticated' in user.keys() :
#             logger.debug("[@user_validated] User keyAuth %s" % user.get('authenticated', False) )
#             if not user.get('authenticated', False):
#                 flash(u'The page you are requested is restricted.')
#                 return redirect("/login")
#         else:
#             return redirect("/login")
#         return f(*args, **kwargs)
#     return decorated_function