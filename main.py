from framework import bottle
# from google.appengine.ext.webapp.util import run_wsgi_app
from backend import *
from forms import ContactForm, SimpleForm


app = application = bottle.Bottle()


@app.route('/')
def index():
    return bottle.template('templates/base', {'proj_name': "Positive Contact"})


class foo():
    bar = "FOOBAR"


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
        return "YAY!"
    else:
        my_string = ""
        my_dict = form.data
        for elem in my_dict:
            my_string += "{0}: {1}, ".format(elem, my_dict[elem])
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
    #return "That resource does not exist"
    return bottle.template('templates/404', {'proj_name': "Positive Contact"})


if __name__ == "__main__":
    bottle.run(server="gae", debug=True)
