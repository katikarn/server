import functools
import xmlrpc.client
HOST = 'localhost'
PORT = 8069
DB = 'demo'
USER = 'admin@mail.com'
PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST,PORT)

uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB,USER,PASS)
print("Logged in as %s (uid:%d)" % (USER,uid))