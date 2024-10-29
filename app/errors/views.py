from . import errors
from flask import render_template

@errors.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@errors.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@errors.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403
