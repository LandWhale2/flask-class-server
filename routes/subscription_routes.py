from flask import Blueprint, request, jsonify
from models import News, User, School, UserNewsFeed, Subscription,db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

subscribe_bp = Blueprint('subscribe', __name__)

@subscribe_bp.route('/api/create/schools', methods=['POST'])
@jwt_required()
def create_school():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    if user.role != 'admin':
        return jsonify({"msg": "Unauthorized"}), 403

    data = request.json
    new_school = School(name=data['name'], region=data['region'], admin_id=user_id)
    db.session.add(new_school)
    db.session.commit()
    return jsonify({"id": new_school.id, "name": new_school.name, "region": new_school.region}), 201

@subscribe_bp.route('/api/subscribe_school', methods=['POST'])
@jwt_required()
def subscribe_school():
    user_id = get_jwt_identity()
    data = request.json
    school_id = data.get('school_id')

    # 이미 구독 중인지 확인
    existing_subscription = Subscription.query.filter_by(user_id=user_id, school_id=school_id).first()
    if existing_subscription:
        return jsonify({"msg": "Already subscribed"}), 409

    new_subscription = Subscription(user_id=user_id, school_id=school_id)
    db.session.add(new_subscription)
    db.session.commit()
    return jsonify({"msg": "Subscribed successfully"}), 201

@subscribe_bp.route('/api/subscribed_schools', methods=['POST'])
@jwt_required()
def subscribed_schools():
    user_id = get_jwt_identity()
    subscriptions = Subscription.query.filter_by(user_id=user_id).all()

    subscribed_schools = []
    for subscription in subscriptions:
        school = School.query.get(subscription.school_id)
        subscribed_schools.append({"id": school.id, "name": school.name, "region": school.region})

    return jsonify(subscribed_schools), 200

@subscribe_bp.route('/api/unsubscribe_school', methods=['POST'])
@jwt_required()
def unsubscribe_school():
    user_id = get_jwt_identity()
    data = request.json
    school_id = data.get('school_id')

    subscription = Subscription.query.filter_by(user_id=user_id, school_id=school_id).first()
    if not subscription:
        return jsonify({"msg": "Subscription not found"}), 404

    db.session.delete(subscription)
    db.session.commit()
    return jsonify({"msg": "Unsubscribed successfully"}), 200

@subscribe_bp.route('/api/subscribed_schools_news', methods=['POST'])
@jwt_required()
def subscribed_schools_news():
    user_id = get_jwt_identity()
    subscriptions = Subscription.query.filter_by(user_id=user_id).all()

    news_list = []
    for subscription in subscriptions:
        news_items = News.query.filter_by(school_id=subscription.school_id, is_deleted=False).order_by(News.published_date.desc()).all()
        for news in news_items:
            news_list.append({
                "news_id": news.id,
                "title": news.title,
                "content": news.content,
                "published_date": news.published_date,
                "school_id": news.school_id
            })

    return jsonify(news_list), 200