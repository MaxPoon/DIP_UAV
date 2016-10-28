import web

urls = (
	'/', 'index'
)

class index:
	def GET(self):
		global string
		return string
string="hello world"
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
string="hi"