from flask import Blueprint, request, jsonify
from models import News, User, School, UserNewsFeed, Subscription,db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

news_bp = Blueprint('news', __name__)


@news_bp.route('/api/publish_news', methods=['POST'])
@jwt_required()
def publish_news():
    data = request.json
    user_id = get_jwt_identity()
    school_id = data.get('school_id')

    school = School.query.get_or_404(school_id)
    if school.admin_id != user_id:
        return jsonify({"msg": "Unauthorized. Not the admin of the school"}), 403

    new_news = News(title=data['title'], content=data['content'], school_id=school.id)
    db.session.add(new_news)

    subscriptions = Subscription.query.filter_by(school_id=school.id).all()
    for subscription in subscriptions:
        user_feed = UserNewsFeed(user_id=subscription.user_id, news_id=new_news.id)
        db.session.add(user_feed)


    db.session.commit()
    return jsonify({"id": new_news.id, "title": new_news.title, "content": new_news.content}), 201


@news_bp.route('/api/delete_news', methods=['POST'])
@jwt_required()
def delete_news():
    data = request.json
    user_id = get_jwt_identity()
    news_id = data.get('news_id')

    news = News.query.get_or_404(news_id)
    school = School.query.get_or_404(news.school_id)

    if school.admin_id != user_id:
        return jsonify({"msg": "Unauthorized. Not the admin of the school"}), 403

    news.is_deleted = True
    db.session.commit()
    return jsonify({"msg": "News marked as deleted"}), 200

@news_bp.route('/api/my_news_feed', methods=['POST'])
@jwt_required()
def my_news_feed():
    user_id = get_jwt_identity()
    user_feed = UserNewsFeed.query.filter_by(user_id=user_id).order_by(UserNewsFeed.created_at.desc()).all()

    news_list = [{
        "news_id": feed_item.news.id,
        "title": feed_item.news.title,
        "content": feed_item.news.content,
        "published_date": feed_item.news.published_date,
        "school_id": feed_item.news.school_id
    } for feed_item in user_feed if not feed_item.news.is_deleted]

    return jsonify(news_list), 200