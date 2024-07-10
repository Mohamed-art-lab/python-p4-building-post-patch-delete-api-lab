#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def get_bakeries():
    """Route to retrieve all bakeries."""
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return jsonify(bakeries)

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def get_or_update_bakery(id):
    """Route to retrieve or update a bakery by ID."""
    bakery = Bakery.query.get(id)
    if bakery is None:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)
    
    if request.method == 'GET':
        return jsonify(bakery.to_dict())
    elif request.method == 'PATCH':
        data = request.form
        if 'name' in data:
            bakery.name = data['name']
            db.session.commit()
            return jsonify(bakery.to_dict())
        else:
            return make_response(jsonify({'error': 'Name not provided in request'}), 400)

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    """Route to create a new baked good."""
    data = request.form
    if 'name' in data and 'price' in data:
        baked_good = BakedGood(name=data['name'], price=data['price'])
        db.session.add(baked_good)
        db.session.commit()
        return jsonify(baked_good.to_dict()), 201
    else:
        return make_response(jsonify({'error': 'Name and price not provided in request'}), 400)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    """Route to delete a baked good by ID."""
    baked_good = BakedGood.query.get(id)
    if baked_good is None:
        return make_response(jsonify({'error': 'Baked good not found'}), 404)
    db.session.delete(baked_good)
    db.session.commit()
    return jsonify({'message': 'Baked good deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)