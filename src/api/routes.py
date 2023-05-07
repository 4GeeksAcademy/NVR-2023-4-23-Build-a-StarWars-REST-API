"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Character, Location, Episode, UserFavourite
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)

# Default route function


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# Get-all functions


@api.route('/users', methods=['GET'])
def get_all_users():

    response_body = {
        "message": "List of all active users:"
    }

    users = User.query.filter_by(is_active=True).all()
    users_serialized = [user.serialize() for user in users]
    return jsonify({"Active users": users_serialized}), 200


@api.route("/characters", methods=['GET'])
def get_all_characters():

    response_body = {
        "message": "List of all characters:"
    }

    characters = Character.query.all()
    characters_serialized = [character.serialize() for character in characters]
    return jsonify({"Characters": characters_serialized}), 200


@api.route("/locations", methods=['GET'])
def get_all_locations():

    response_body = {
        "message": "List of all locations:"
    }

    locations = Location.query.all()
    locations_serialized = [location.serialize() for location in locations]
    return jsonify({"Locations": locations_serialized}), 200


@api.route("/episodes", methods=['GET'])
def get_all_episodes():

    response_body = {
        "message": "List of all episodes:"
    }

    episodes = Episode.query.all()
    episodes_serialized = [episode.serialize() for episode in episodes]
    return jsonify({"Episodes": episodes_serialized}), 200


# Get-by-Id functions

@api.route("/users/<int:target_user_id>", methods=['GET'])
def get_user_by_id(target_user_id):

    response_body = {
        "Message": "User:"
    }

    target_user = User.query.filter_by(id=target_user_id).first()

    if not target_user:
        return jsonify({"Message": "User not found"}), 404

    target_user_serialized = target_user.serialize()
    return jsonify({"User": target_user_serialized}), 200


@api.route("/characters/<int:target_character_id>", methods=['GET'])
def get_character_by_id(target_character_id):

    response_body = {
        "Message": "Character:"
    }

    target_character = Character.query.filter_by(
        id=target_character_id).first()

    if not target_character:
        return jsonify({"Message": "Character not found"}), 404

    target_character_serialized = target_character.serialize()
    return jsonify({"Character": target_character_serialized}), 200


@api.route("/locations/<int:target_location_id>", methods=['GET'])
def get_location_by_id(target_location_id):

    response_body = {
        "Message": "Location:"
    }

    target_location = Location.query.filter_by(id=target_location_id).first()

    if not target_location:
        return jsonify({"Message": "Location not found"}), 404

    target_location_serialized = target_location.serialize()
    return jsonify({"Location": target_location_serialized}), 200


@api.route("/episodes/<int:target_episode_id>", methods=['GET'])
def get_episode_by_id(target_episode_id):

    response_body = {
        "Message": "Episode"
    }

    target_episode = Location.query.filter_by(id=target_episode_id).first()

    if not target_episode:
        return jsonify({"Message": "Episode not found"}), 404

    target_episode_serialized = target_episode.serialize()
    return jsonify({"Location": target_episode_serialized}), 200


@api.route("/users/<int:target_user_id>/favourites", methods=['GET'])
def user_favourites(target_user_id):
    user = User.query.get(target_user_id)
    if not user:
        return jsonify({"Message": "User not found"}), 404

    favourites = UserFavourite.query.filter_by(user_id=target_user_id).all()
    favourites_serialized = [favourite.serialize() for favourite in favourites]
    return jsonify({"favorites": favourites_serialized}), 200

# Post functions

@api.route('/users', methods=["POST"])
def create_user():
  
    body= request.json
    new_user = User(username=body["username"] , email=body["email"] , password=body["password"], is_active=True)
    db.session.add(new_user)
    db.session.commit()

    users = User.query.all()
    users_serialzied =  [user.serialize() for user  in users]
    return jsonify({"All users": users_serialzied}), 200

@api.route('/characters', methods=["POST"])
def create_character():
  
    body= request.json
    new_character = Character(name=body["name"] , species=body["species"])
    db.session.add(new_character)
    db.session.commit()

    characters = Character.query.all()
    characters_serialzied =  [character.serialize() for character  in characters]
    return jsonify({"All characters": characters_serialzied}), 200

@api.route('/locations', methods=["POST"])
def create_location():
  
    body= request.json
    new_location = Location(name=body["name"] , type=body["type"])
    db.session.add(new_location)
    db.session.commit()

    locations = Location.query.all()
    locations_serialzied =  [location.serialize() for location  in locations]
    return jsonify({"All locations": locations_serialzied}), 200

@api.route('/episodes', methods=["POST"])
def create_episode():
  
    body= request.json
    new_episode = Episode(name=body["name"] , air_date=body["air_date"])
    db.session.add(new_episode)
    db.session.commit()

    episodes = Episode.query.all()
    episodes_serialzied =  [episode.serialize() for episode  in episodes]
    return jsonify({"All episodes": episodes_serialzied}), 200

@api.route("/favourites/characters", methods=["POST"])
def create_favourite_character():
    
    body= request.json
    target_user = User.query.filter_by(id=body["user_id"]).first()
    target_character = Character.query.filter_by(id=body["character_id"]).first()
    if not target_user:
        return jsonify({"Message": "User not found"}), 404
    if not target_character:
        return jsonify({"Message": "Character not found"}), 404
   
    new_favourite = UserFavourite(user_id=target_user.id, character_id=target_character.id)
    db.session.add(new_favourite)
    db.session.commit()
    return jsonify({"Message": "Favourite Character sucessfully added"}), 200

@api.route("/favourites/locations", methods=["POST"])
def create_favourite_location():
    
    body= request.json
    target_user = User.query.filter_by(id=body["user_id"]).first()
    target_location = Location.query.filter_by(id=body["location_id"]).first()
    if not target_user:
        return jsonify({"Message": "User not found"}), 404
    if not target_location:
        return jsonify({"Message": "Location not found"}), 404
   
    new_favourite = UserFavourite(user_id=target_user.id, location_id=target_location.id)
    db.session.add(new_favourite)
    db.session.commit()
    return jsonify({"Message": "Favourite Loation sucessfully added"}), 200

@api.route("/favourites/episodes", methods=["POST"])
def create_favourite_episode():
    
    body= request.json
    target_user = User.query.filter_by(id=body["user_id"]).first()
    target_episode = Episode.query.filter_by(id=body["episode_id"]).first()
    if not target_user:
        return jsonify({"Message": "User not found"}), 404
    if not target_episode:
        return jsonify({"Message": "Episode not found"}), 404
   
    new_favourite = UserFavourite(user_id=target_user.id, episode_id=target_episode.id)
    db.session.add(new_favourite)
    db.session.commit()
    return jsonify({"Message": "Favourite episode sucessfully added"}), 200

   

