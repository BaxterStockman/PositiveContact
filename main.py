from framework import bottle
# from google.appengine.ext.webapp.util import run_wsgi_app
from backend import *
from forms import ContactForm, SimpleForm
import beaker.middleware



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
app = beaker.middleware.SessionMiddleware(bottle.app(), session_opts)


@bottle.hook('before_request')
def setup_request():
    bottle.request.session = bottle.request.environ.get('beaker.session')

@bottle.route('/')
def index():
    return bottle.template('templates/base', {'proj_name': "Positive Contact"})


@bottle.route('/test')
def test():
    s = bottle.request.environ.get('beaker.session')
    s['test'] = s.get('test', 0) + 1
    s.save()
    return "Test counter: {0}".format(s['test'])



class foo():
    bar = "FOOBAR"


@bottle.get('/add')
def add_form():
    form = ContactForm()
    return bottle.template('templates/base', {'proj_name': "Positive Contact",
                                              'action': "Add",
                                              'form': form})


@bottle.post('/add')
def add_submit():
    form = ContactForm(bottle.request.forms.decode())
    if form.validate():
        return "YAY!"
    else:
        my_string = ""
        my_dict = form.data
        for elem in my_dict:
            my_string += "{0}: {1}, ".format(elem, my_dict[elem])
        return my_string


@bottle.route('/edit/<contact_id:int>')
def edit_contact(contact_id):
    form = ContactForm()
    return bottle.template('templates/base', {'contact_id': contact_id,
                                                 'proj_name': "Positive Contact",
                                                 'form': form,
                                                 'action': "Edit"})


@bottle.error(403)
def error403(code):
    return "Invalid code specified"


@bottle.error(404)
def error404(code):
    #return "That resource does not exist"
    return bottle.template('templates/404', {'proj_name': "Positive Contact"})


if __name__ == "__main__":
    bottle.run(server="gae", app=app, debug=True)
