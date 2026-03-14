from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= "mysql+pymysql://root:Mysql123@localhost/service_db"
db = SQLAlchemy(app)

class Service(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(20))
    subtitle=db.Column(db.String(30))
    description=db.Column(db.String(100))
    price=db.Column(db.Integer)
    imageurl=db.Column(db.String(30))
    status=db.Column(db.String(20))
    categoryid=db.Column(db.Integer)
    created_at=db.Column(db.DateTime,default=datetime.now)
    updated_at=db.Column(db.DateTime,default=datetime.now,onupdate = datetime.now)
    deleted_at=db.Column(db.DateTime,nullable=True)


    def to_dict(self):
        return { "id":self.id,
                 "title":self.title,
                 "subtitle":self.subtitle,
                 "description":self.description,
                 "price":self.price,
                 "imageurl":self.imageurl,
                 "status":self.status
                 "categoryid":self.categoryid
                 }
    
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "home page"

@app.route('/service',methods=["GET"])
def service_all():
    services = Service.query.all()
    return jsonify([s.to_dict() for s in services])

@app.route("/createservice",methods=["POST"])
def Createservice():
    payload = request.get_json()
    service_list = Service(
                            title = payload["title"],
                            subtitle = payload["subtitle"],
                            description = payload["description"],
                            price = payload["price"],
                            imageurl = payload["imageurl"],
                            status = payload["status"],
                            categoryid = payload["categoryid"]
                          )           
    
    db.session.add(service_list)
    db.session.commit()
    return jsonify({"message":"service added successfully"})


@app.route('/service_cid/<int:categoryid>',methods=["GET"])
def service_category(categoryid):
    services = Service.query.filter_by(categoryid=categoryid).all()
    return jsonify([s.to_dict()for s in services])

@app.route('/services_id/<int:id>' ,methods=["GET"])
def service_id(id):
    services = Service.query.filter_by(id=id).first()
    return jsonify(services.to_dict())

@app.route("/update_service/<int:id>",methods = ["put"])
def update_service(id):
    services = Service.query.filter_by(id=id).first()
    if not services:
        return jsonify({"message": "not found"})
    data = request.get_json()
    services.title = data["title"]
    services.subtitle = data["subtitle"]
    services.description = data["description"]
    services.price = data["price"]
    services.imageurl = data["imageurl"]
    services.status = data["status"]
    services.categoryid = data["categoryid"]
    db.session.commit()
    return jsonify({"message":"service updated"})

@app.route("delete_services/<int:id>",methods=["put"])
def delete_service(id):
    service = Service.query.filter_by(id=id).first()
    if not service:
        return jsonify({"message":"not found"})
    service.delete_status = True
    service.delete_at = datetime.now()
    db.session.commit()
    return jsonify({"message": True})


if __name__ == "__main__":
    app.run(debug=True)

