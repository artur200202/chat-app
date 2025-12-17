from flask import request, jsonify
from app import db
from app.models import Room
from app.blueprints.rooms import rooms_bp
from app.blueprints.rooms.schemas import room_schema, rooms_schema

@rooms_bp.route('/', methods=['GET'])
def get_rooms():
    """Get all rooms"""
    rooms = Room.query.all()
    return jsonify(rooms_schema.dump(rooms)), 200

@rooms_bp.route('/<int:room_id>', methods=['GET'])
def get_room(room_id):
    """Get a single room by ID"""
    room = Room.query.get_or_404(room_id)
    return jsonify(room_schema.dump(room)), 200

@rooms_bp.route('/', methods=['POST'])
def create_room():
    """Create a new room"""
    data = request.get_json()
    
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Room name is required'}), 400
    
    
    if Room.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Room name already exists'}), 400
    
    
    new_room = Room(
        name=data['name'],
        description=data.get('description', '')
    )
    
    db.session.add(new_room)
    db.session.commit()
    
    return jsonify(room_schema.dump(new_room)), 201

@rooms_bp.route('/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    """Update a room"""
    room = Room.query.get_or_404(room_id)
    data = request.get_json()
    
    if 'name' in data:
        
        existing = Room.query.filter_by(name=data['name']).first()
        if existing and existing.id != room_id:
            return jsonify({'error': 'Room name already exists'}), 400
        room.name = data['name']
    
    if 'description' in data:
        room.description = data['description']
    
    db.session.commit()
    return jsonify(room_schema.dump(room)), 200

@rooms_bp.route('/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    """Delete a room"""
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Room deleted successfully'}), 200