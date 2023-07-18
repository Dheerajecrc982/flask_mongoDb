from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from bson import json_util
import json

app = Flask(__name__)
client = MongoClient("mongodb://mongodb-container:27017")  # Replace with your MongoDB connection string

database_name = "mydb"  # Replace with the desired database name

# Access the database
db = client[database_name]

# Check if the database already exists
if database_name in client.list_database_names():
    print(f"The database '{database_name}' already exists.")
else:
    # Create the database
    db = client[database_name]
    print(f"The database '{database_name}' was created.")

collection_name = "user_details"  # Replace with the desired collection name

# Check if the collection already exists
if collection_name in db.list_collection_names():
    print(f"The collection '{collection_name}' already exists in '{database_name}'.")
else:
    # Create the collection
    collection = db[collection_name]
    print(f"The collection '{collection_name}' was created in '{database_name}'.")

collection = db[collection_name]

@app.route('/api/users', methods=['POST'])
def create_user():
    user_data = request.json
    # Perform validation and error handling as needed
    result = collection.insert_one(user_data)
    return jsonify({'message': 'User created', 'id': str(result.inserted_id)})


@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = list(collection.find())
        serialized_users = json.loads(json_util.dumps(users))
        return jsonify(serialized_users)
    except Exception as e:
        return jsonify({'message': 'Error occurred', 'error': str(e)})



@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = collection.find_one({'_id': ObjectId(user_id)})
    if user:
        serialized_user = json.loads(json_util.dumps(user))
        return jsonify(serialized_user)
    else:
        return jsonify({'message': 'User not found'})


@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    result = collection.update_one({'_id': ObjectId(user_id)}, {'$set': user_data})
    if result.modified_count > 0:
        return jsonify({'message': 'User updated'})
    else:
        return jsonify({'message': 'User not found'})


@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = collection.delete_one({'_id': ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted'})
    else:
        return jsonify({'message': 'User not found'})

if __name__ == '__main__':
    app.run(debug=True)
