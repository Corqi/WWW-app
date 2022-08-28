from flask import Blueprint, render_template, request, jsonify
from ..models import User, Message
from ..app import db
# from flask_security import login_required

bp = Blueprint('bp_chat', __name__)


@bp.route('/chat', methods=['GET'])
def chat_messages_get():
    obj = Message(user_id=1, content="lalala")
    db.session.add(obj)
    db.session.commit()

    try:
        message_id = int(request.args.get('message_id'))
    except (ValueError, TypeError):
        message_id = 0

    messages = []
    if message_id > 0:
        messages = Message.query.filter(
            Message.id > message_id
        ).order_by(Message.id.asc()).limit(20).all()
    else:
        messages = Message.query.order_by(Message.id.desc()).limit(20).all()
        messages.reverse()

    results = []
    for msg in messages:
        results.append({
            'id': msg.id,
            'user_id': msg.user_id,
            'username': msg.user.name,
            'content': msg.content,
            'created_at': msg.created_at
        })
    return jsonify(results)