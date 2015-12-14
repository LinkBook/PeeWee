import os
from peewee import *
from tornado.web import RequestHandler

# Connect to the database URL defined in the environment, falling
# # back to a local Sqlite database if no database URL is specified.
# MySQl_DB_URL = os.environ.get('OPENSHIFT_MYSQL_DB_URL') \
# 	if os.environ.get('OPENSHIFT_MYSQL_DB_URL') \
# 	else 'MySQL://localhost:3306/'
# db = connect(os.environ.get('DATABASE') or ':///default.db')

db = MySQLDatabase("lbdb", host="localhost", port=3306, user="root", passwd="")


class PeeweeRequestHandler(RequestHandler):
	def prepare(self):
		db.connect()
		return super(PeeweeRequestHandler, self).prepare()

	def on_finish(self):
		if not db.is_closed():
			db.close()
		return super(PeeweeRequestHandler, self).on_finish()
