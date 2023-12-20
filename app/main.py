from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name}

# Create the tables
@app.before_first_request
def create_tables():
    db.create_all()

# Create
@app.route('/item', methods=['POST'])
def add_item():
    data = request.get_json()
    item = Item(name=data['name'])
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

# Read
@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict())

# Update
@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = Item.query.get_or_404(item_id)
    item.name = data['name']
    db.session.commit()
    return jsonify(item.to_dict())

# Delete
@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
