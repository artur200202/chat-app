from flask import request, jsonify
from app import db
from app.models import Message, User, Room
from app.blueprints.messages import messages_bp
from app.blueprints.messages.schemas import message_schema, messages_schema

@messages_bp.route('/', methods=['GET'])
def get_messages():
    """Get all messages, optionally filtered by room"""
    room_id = request.args.get('room_id', type=int)
    
    if room_id:
        messages = Message.query.filter_by(room_id=room_id).order_by(Message.created_at.asc()).all()
    else:
        messages = Message.query.order_by(Message.created_at.asc()).all()
    
    return jsonify(messages_schema.dump(messages)), 200

@messages_bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    """Get a single message by ID"""
    message = Message.query.get_or_404(message_id)
    return jsonify(message_schema.dump(message)), 200

@messages_bp.route('/', methods=['POST'])
def create_message():
    """Create a new message"""
    data = request.get_json()
    
    
    if not data or not data.get('content') or not data.get('user_id') or not data.get('room_id'):
        return jsonify({'error': 'Content, user_id, and room_id are required'}), 400
    
    
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    
    room = Room.query.get(data['room_id'])
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    
    new_message = Message(
        content=data['content'],
        user_id=data['user_id'],
        room_id=data['room_id']
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return jsonify(message_schema.dump(new_message)), 201

@messages_bp.route('/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    """Update a message"""
    message = Message.query.get_or_404(message_id)
    data = request.get_json()
    
    if 'content' in data:
        message.content = data['content']
    
    db.session.commit()
    return jsonify(message_schema.dump(message)), 200

@messages_bp.route('/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    """Delete a message"""
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted successfully'}), 200