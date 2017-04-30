import webapp2
import os
import json
import uuid

from google.appengine.ext.webapp import template
from webapp2_extras import routes

from google.appengine.ext import ndb


class Request(ndb.Model):
    uuid = ndb.StringProperty()
    data = ndb.StringProperty(indexed=False)
    created_on = ndb.DateProperty(auto_now_add=True)


def render(context):
    path = os.path.join(os.path.dirname(__file__), 'templates/request.html')
    return template.render(path, context)


class Marco(webapp2.RequestHandler):
    def all(self):
        params = dict(self.request.params)
        headers = dict(self.request.headers)
        method = self.request.method
        data = {
            "params": params,
            "headers": headers,
            "method": method
        }
        data_s = json.dumps(data)
        r = Request(uuid=str(uuid.uuid4()), data=data_s)
        r.put()
        data['location'] = webapp2.uri_for('polo', uuid=r.uuid)
        self.response.write(render(data))

    def head(self):
        self.all()

    def get(self):
        self.all()

    def post(self):
        self.all()


class Polo(webapp2.RequestHandler):
    def get(self, uuid):
        r = Request.query(Request.uuid==uuid).get()
        if r:
            context = json.loads(r.data)
            self.response.write(render(context))
        else:
            self.response.write('Not Found')


app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=Marco, name="home"),
    webapp2.Route(r'/polo/<uuid:.*>', handler=Polo, name="polo"),
], debug=False)
