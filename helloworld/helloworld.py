import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Goodbye, Cruel World!')

app = webapp2.WSGIApplication([
    ('/helloworld', MainPage),
], debug=True)
