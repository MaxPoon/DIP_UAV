import web, requests

urls = (
	'/', 'index'
)

class index:
	def GET(self):
		global string
		return string
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
string="start"

while True:
	if foundTarget():
		r = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAev2Ky8pGEMl5v04YuIOEQos4m3Hl8Ge8')
		string = 'find target at longitude: '+r.json()['location']['lng']+'latitude: '+r.json()['location']['lat']
		