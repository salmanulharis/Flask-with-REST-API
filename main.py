from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Pass123@localhost/rest_api_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Video(name = {name}, views = {views}, likes = {likes}"

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'views': fields.Integer,
	'likes': fields.Integer
}

class Video(Resource):
	@marshal_with(resource_fields)
	def get(self, video_id):
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Could not find video with that ID")
		return result

	@marshal_with(resource_fields)
	def put(self, video_id):
		args = video_put_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if result:
			abort(409, message="Video id taken...")
		video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
		# db.session.add(video)
		# db.session.commit()
		return video, 201

	@marshal_with(resource_fields)
	def patch(self, video_id): #or we can use 'put' here
		args = video_update_args.parse_args()
		result = VideoModel.query.filter_by(id=video_id).first()
		if not result:
			abort(404, message="Video doesn't exist, cannot update.")

		if args['name']:
			result.name = args['name']
		if args['views']:
			result.views = args['views']
		if args['likes']:
			result.likes = args['likes']
		db.session.commit()
		
		return result


	def delete(self, video_id):
		abort_if_video_id_does_not_exists(video_id)
		del videos[video_id]
		return '', 204

class VideoList(Resource):
	@marshal_with(resource_fields)
	def get(self):
		result = VideoModel.query.all()
		return result



api.add_resource(Video, "/video/<int:video_id>")
api.add_resource(VideoList, "/video")

# class HelloWorld(Resource):
# 	# def get(self):
# 	# 	return {'data':'Hello World'}

# 	# def get(self, name, age):
# 	# 	return {'name':name, 'age':age}

# 	def get(self, name):
# 		return names[name]

# 	def post(self):
# 		return {'data': 'posted'}

# # api.add_resource(HelloWorld, '/helloworld/<string:name>/<int:age>')
# api.add_resource(HelloWorld, '/helloworld/<string:name>')

if __name__=="__main__":
	app.run(debug=True)