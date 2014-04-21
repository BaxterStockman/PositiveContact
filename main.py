import webapp2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("<div background-color='black' color='white'><h1 "
                            "color='green'>Hey, buddy!</h1></div>")

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
