from flask import Blueprint, request, jsonify
from models import News, User, Subscription, db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/social_login', methods=['POST'])
def social_login():
    data = request.json
    social_type = data.get('social_type')
    social_id = data.get('social_id')
    name = data.get('name')
    email = data.get('email')

    user = User.query.filter_by(social_type=social_type, social_id=social_id).first()

    if not user:
        user = User(
            name=name,
            email=email,
            social_type=social_type,
            social_id=social_id
        )
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@auth_bp.route('/api/users/update', methods=['POST'])
@jwt_required()
def update_user_info():
    current_user_id = get_jwt_identity()
    data = request.json

    user = User.query.get_or_404(current_user_id)

    user.role = data.get('role', user.role)
    user.name = data.get('name', user.name)

    db.session.commit()
    return jsonify({"id": user.id, "role": user.role, "name": user.name, "email": user.email}), 200