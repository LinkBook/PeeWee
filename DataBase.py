# coding=utf-8

from peewee import *

db = MySQLDatabase("lbdb", host="localhost", port=3306, user="root", passwd="")


class MySQLModel(Model):
	id = PrimaryKeyField(unique=True)

	class Meta:
		database = db


class User(MySQLModel):
	name = CharField()
	family = CharField()
	username = CharField(null=False, unique=True)
	usertype = CharField()
	picture = CharField()
	email = CharField(index=True, null=False)
	password = CharField(null=False)


class Web(MySQLModel):
	FestTitle = CharField()
	FestLogo = CharField()
	FestText = TextField()
	FestURL = CharField(unique=True)
	FestDate = DateField()
	WebTitle = CharField()
	WebLogo = CharField()
	WebURL = CharField(unique=True)
	WebCat = CharField()
	WebSub = CharField()


class Contacts(MySQLModel):
	Name = CharField()
	Email = CharField(null=False)
	Message = TextField(null=False)


db.connect()
if __name__ == '__main__':
	db.create_tables([User, Web, Contacts], safe=True)
