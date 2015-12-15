# coding=utf-8

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymysql
import time
import DataBase


class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("username")


class DashBoardHandler(BaseHandler):
	def get(self):
		a = self.get_secure_cookie("username")
		if a:
			self.render("Dashboard.html")
			return

		self.render("Login.html")


class HelpHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('help.html')


class RegisterHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('Register.html')

	def post(self):
		name = self.get_argument("name")
		family = self.get_argument("family")
		username = self.get_argument("username")
		# user_type = self.get_argument("user-type")
		# picture = self.get_argument("flpicture")
		email = self.get_argument("email")
		password = self.get_argument("password")
		try:
			user = DataBase.User()
			user.name = name
			user.username = username
			user.family = family
			# user.usertype = user_type
			user.email = email
			user.password = password
			user.save()
			self.write("<script>alert('اطلاعات ثبت شد')</script>")
			self.render("Login.html")
		except:
			self.write("<script>alert('اطلاعات ثبت نشد')</script>")
			self.redirect("/")


class LoginHandler(BaseHandler):
	def get(self):
		self.render('Login.html')

	def post(self):
		Username = self.get_argument("username")
		Password = self.get_argument("password")
		try:
			user = DataBase.User.get(DataBase.User.username == Username, DataBase.User.password == Password)
		except DataBase.User.DoesNotExist:
			user = None
		if user:
			self.set_secure_cookie("username", self.get_argument("username"))
			self.write("<script>alert('کوکی ست شد... خوش آمدید ')</script>")
			self.render("Dashboard.html")

		else:
			self.write("<script>alert('همچین کاربری نداریم ')</script>")
			self.render('Login.html')


class LogoutHandler(tornado.web.RequestHandler):
	def get(self):
		self.clear_all_cookies()
		self.redirect("/")


class WebpagesHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('Webpages.html', n=1)


class WebshowHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('webshow.html')


class Ahandler(tornado.web.RequestHandler):
	def post(self):
		sql = "INSERT INTO festival(Logoname_fest, url,Title,Body)VALUES(%s, %s,%s, %s)"

		Title = self.get_argument("fest-title")
		Body = self.get_argument("fest-text")
		Logoname_fest = self.get_argument("fest-logo")
		url = self.get_argument("fest-url")
		conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="linkbook")
		cur = conn.cursor()
		cur.execute(sql, (Logoname_fest, url, Title, Body))
		self.redirect("/")
		cur.close()
		conn.commit()
		conn.close()


class IntroductionHandler(tornado.web.RequestHandler):
	def post(self):
		vision = self.get_argument("vision")
		mision = self.get_argument("mision")

		self.write("<script>alert('اطلاعات ثبت شد')</script>")
		self.redirect("/")


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')


class AboutHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('about.html')


class UploadFile(tornado.web.RequestHandler):
	# handle a post request
	def post(self):
		# ... maybe add a check that checks whether the user is allowed to upload anything ...
		# the file(s) that should get uploaded
		files = []
		# check whether the request contains files that should get uploaded
		try:
			files = self.request.files['files']
		except:
			pass
		# for each file that should get uploaded
		for xfile in files:
			# get the default file name
			file = xfile['filename']
			# the filename should not contain any "evil" special characters
			# basically "evil" characters are all characters that allows you to break out from the upload directory
			index = file.rfind(".")
			filename = file[:index].replace(".", "") + str(time.time()).replace(".", "") + file[index:]
			filename = filename.replace("/", "")
			# save the file in the upload folder
			with open("static/uploads/%s/" % (filename), "wb") as out:
				# Be aware, that the user may have uploaded something evil like an executable script ...
				# so it is a good idea to check the file content (xfile['body']) before saving the file
				out.write(xfile['body'])

				self.render('Webpages.html')


class ContactHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('Contact.html')

	def post(self):
		cname = self.get_argument("namec")
		cemail = self.get_argument("email")
		cmessage = self.get_argument("messege")
		try:
			contact = DataBase.Contacts()
			contact.Name = cname
			contact.Email = cemail
			contact.Message = cmessage
			contact.save()
			self.write("<script>alert('اطلاعات ثبت شد')</script>")
			self.redirect("/")
		except:
			self.write("<script>alert('اطلاعات ثبت نشد')</script>")
			self.redirect("/")

		self.redirect("/")


class MainsHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('Main.html')
