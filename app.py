#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from random import randint
from contextlib import closing
import glob
from flask import send_from_directory
import MySQLdb
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

app.config.from_object('config')


# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    
        fi = os.listdir(os.path.abspath("uploads"))
        ab=os.path.abspath("uploads");
       
        return render_template('pages/placeholder.home.html', fi=fi , ab=ab)


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.root_path, 'uploads/')
        
    return send_from_directory(directory=uploads, filename=filename)

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')
@app.route('/uploads{}')
def uploads():
    with open(fname, 'r') as fin:
        allf =  fin.read()    
    return render_template('pages/placeholder.view.html', allf=allf)

@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
        fname = ""
        # Open database connection
        db = MySQLdb.connect("127.0.0.1","root","","elucidata_second_task" )
        
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        sql = "SELECT id FROM fasta "
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
                name = row[0]
                
        if request.method == 'POST':
                f = request.files['file']
        f.save("uploads/"+f.filename)
        fname=("uploads/"+f.filename)
        with open("uploads/"+f.filename, 'r')as f:
            content1=""
            for line in f:
                content1 += line + '\n'
        sql = "INSERT INTO fasta(fasta, \
                                       filename) \
                                       VALUES ('%s', '%s')" % \
                                       (content1, fname)
        try:
                                # Execute the SQL command
                                cursor.execute(sql)
                                # Commit your changes in the database
                                db.commit()
        except:
                                # Rollback in case there is any error
                                db.rollback()                
                
        return render_template('pages/placeholder.view.html',content1=content1, mimetype='text/plain',name=name)


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
