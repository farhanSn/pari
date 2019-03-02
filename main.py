from flask import Flask, request, make_response,render_template, session, url_for,redirect,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap 
from flask_moment import Moment 
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name =StringField("name",validators=[DataRequired()])
    submit = SubmitField("Submit")
    

app = Flask(__name__)
moment = Moment(app)
bootstrap = Bootstrap(app)
manager = Manager(app)
app.config['SECRET_KEY'] = 'hey hey'
@app.route('/',methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name!=form.name.data:
            flash("Looks like you have changed your name!")
        session['name']= form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',form = form, name =session.get('name'))


@app.route('/user/<name>')
def name(name):
    return render_template('user.html',name = name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500


if __name__=='__main__':
    manager.run()