from framework import bottle
# from google.appengine.ext.webapp.util import run_wsgi_app
from backend import *
from forms import ContactForm, LoginForm, SignupForm
import beaker.middleware
import pprint


'''
Thanks to user larsks for this handy way of dealing with
session variables.  Source:
http://stackoverflow.com/questions/13735333/bottle-py-session-with-beaker
'''

session_opts = {
    'session.type': 'ext:google',
    'session.auto': True,
}


# Set up middleware
app = bottle.app()
site = beaker.middleware.SessionMiddleware(app, session_opts)


@app.hook('before_request')
def setup_request():
    bottle.request.session = bottle.request.environ.get('beaker.session')


@app.route('/')
def index():
    return bottle.template('templates/base', {'proj_name': "Positive Contact"})


@app.route('/test')
def test():
    s = bottle.request.environ.get('beaker.session')
    s['test'] = s.get('test', 0) + 1
    s.save()
    return pprint.pformat(s)


@app.get('/login')
def login_form():
    form = LoginForm()
    return bottle.template('templates/base', {'proj_name': "Positive Contact",
                                              'action': "Login",
                                              'form': form})


@app.post('/login')
def login_submit():
    form = LoginForm(bottle.request.forms.decode())
    if form.validate():
        # bottle.request.session.save()
        bottle.redirect('/')
    else:
        my_string = ""
        my_dict = form.data
        for elem in my_dict:
            my_string += "{0}: {1}, ".format(elem, my_dict[elem])
        return my_string


@app.get('/signup')
def signup_form():
    form = SignupForm()
    return bottle.template('templates/base', {'proj_name': "Positive Contact",
                                              'action': "Sign up",
                                              'form': form})


@app.post('/signup')
def signup_submit():
    form = SignupForm(bottle.request.forms.decode())
    if form.validate():
        # bottle.request.session.save()
        bottle.redirect('/')
    else:
        my_string = ""
        my_dict = form.data
        for elem in my_dict:
            my_string += "{0}: {1}, ".format(elem, my_dict[elem])
        return my_string


@app.get('/add')
def add_form():
    form = ContactForm()
    return bottle.template('templates/base', {'proj_name': "Positive Contact",
                                              'action': "Add",
                                              'form': form})


@app.post('/add')
def add_submit():
    form = ContactForm(bottle.request.forms.decode())
    if form.validate():
        # bottle.request.session.save()
        # bottle.redirect('/')
        return pprint.pformat(bottle.request.session)
    else:
        my_string = ""
        for field in form:
            my_string += "{0}: {1}, ".format(field.label(), field.label())
        return my_string


@app.route('/edit/<contact_id:int>')
def edit_contact(contact_id):
    form = ContactForm()
    return bottle.template('templates/base', {'contact_id': contact_id,
                                              'proj_name': "Positive Contact",
                                              'form': form,
                                              'action': "Edit"})


@app.error(403)
def error403(code):
    return "Invalid code specified"


@app.error(404)
def error404(code):
    return bottle.template('templates/404', {'proj_name': "Positive Contact"})


if __name__ == "__main__":
    bottle.run(server="gae", app=site, debug=True)
