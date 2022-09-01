from flask import Blueprint, request, jsonify
from ..models import Message
from ..app import db
from flask_login import login_required, current_user

bp = Blueprint('bp_chat', __name__)


@bp.route('/chat', methods=['GET'])
@login_required
def chat_messages_get():
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
            'content': msg.content
        })
    return jsonify(results)


@bp.route('/chat', methods=['POST'])
@login_required
def chat_messages_post():
        data = request.get_json(force=True)

        if 'content' in data and len(data['content']) >= 1 and len(data['content']) <= 500:
            obj = Message(user_id=current_user.id, content=data['content'])
            db.session.add(obj)
            db.session.commit()
            return '', 204
        else:
            return 'Content is incorrect or was not given.', 400