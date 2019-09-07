from flask import Flask
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from sklearn.externals import joblib
app = Flask(__name__) 
api = Api(app)

class iris(Resource):
	def get(self):
		return {"Imama api":"it reply your answers automatically"}
	def post (self):
		parser = reqparse.RequestParser()
		parser.add_argument('message')
		args = parser.parse_args()
		message = args['message']

		message = str(message)
		msg_r = [message]
		cv = joblib.load('cv.pkl')
		model = joblib.load('imama.pkl')
		msg = cv.transform(msg_r).toarray()
		print(msg)
		result = model.predict(msg)
		result = result[0]
		result = int(result)
		print(result)
		db = create_engine("sqlite:///imama_new.db")
		conn = db.connect()
		query = "select answer from brain_talk where label == {}".format(result)
		result_proxy = conn.execute(query)
		result = result_proxy.fetchall()
		ans = {"answer":"""{}""".format(result)}	
		print(result)
		return ans

api.add_resource(iris, "/")

if __name__ == '__main__':
	app.run(debug=True)


#@Iris Coders