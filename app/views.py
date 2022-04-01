"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from fileinput import filename
import os
from tkinter import image_names
from app import app
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from werkzeug.utils import secure_filename
from .forms import UploadForm

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/contact/')
def contact():
    if not session.get('logged_in'):
        abort(401)
    """Render the website's contact page."""
    return render_template('contact.html')

#filefolder = './files'

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if not session.get('logged_in'):
        abort(401)

    # Instantiate your form class
    myForm = UploadForm()

    # Validate file upload on submit
    if request.method == 'POST' and myForm.validate_on_submit():
        # Get file data and save to your uploads folder
        photo = myForm.photo.data
        # photo = request.files['photo']
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File Saved', 'success')
        return redirect(url_for('home', filename=filename))

    return render_template('upload.html', form=myForm)



@app.route('/static/gallery/<filename>')
def get_image(filename):
    #root_dir = os.getcwd()
    #return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']) + "/" + filename)
    #return send_from_directory(app.config["UPLOAD_FOLDER"] +"/" + filename)
    #return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return (app.config["UPLOAD_FOLDER"] +"/" + filename)

"""
@app.route('/files')
def files():
    if not session.get('logged_in'):
        abort(401)
    
    #root_dir = os.getcwd()
    #print (root_dir)
    #for subdir, dirs, files in os.walk(root_dir + 'UPLOAD_FOLDER'):
        #for file in files:
            #print (os.path.join(subdir, file))

    return render_template('files.html', filename=filename, uploads=(app.config["UPLOAD_FOLDER"]))
"""
"""
@app.route('/static/gallery/<filename>', methods=['POST', 'GET'])
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for(filename= app.config['UPLOAD_FOLDER'] + filename), code=301)

"""
@app.route('/image_master')
def image_master():
    if not session.get('logged_in'):
        abort(401)
    #img_fold = './upload_test'
    image_names = os.listdir(app.config['UPLOAD_FOLDER'])
    #image_names = os.listdir(img_fold)
    #print(image_names)
    return render_template("files.html", image_names=image_names)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['ADMIN_USERNAME'] or request.form['password'] != app.config['ADMIN_PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            
            flash('You were logged in', 'success')
            return redirect(url_for('upload'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('home'))


###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
