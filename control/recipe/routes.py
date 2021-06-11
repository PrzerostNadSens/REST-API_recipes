from datetime import datetime
from time import time

from flask import Blueprint, request, Response, jsonify
from mongoengine import Q
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

from errors import SchemaValidationError, AlreadyExistsError, InternalServerError, UpdatingError, DeletingError, \
    NotExistsError, FieldError
from model.recipe import Recipe
from model.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

MOD_NAME = "Recipe"
IGNORED = False
api = Blueprint(MOD_NAME, __name__)


@api.route('/', methods=['GET'])
def recipe():
    query = {}
    t = {}
    try:
        if 'name' in request.args:
            query['name'] = request.args['name']
        if 'lastUpdate' in request.args:
            t['lastUpdate'] = datetime.fromtimestamp(float(request.args['lastUpdate']))
            rec = Recipe.objects.filter((Q(lastUpdate__gte=t['lastUpdate'])), **query)
        else:
            rec = Recipe.objects(**query)
        def recipe():
            yield '{"TIME":' + str(time()) + ',"Recipes":['
            dot = False
            for item in rec:
                if dot:
                    yield ','
                yield item.to_json()
                dot = True
            yield ']}'

        return Response(recipe(), mimetype="application/json", status=200)
    except DoesNotExist:
        return jsonify(NotExistsError("Przepis")), 400
    except Exception as e:
        return jsonify(InternalServerError()), 404


@api.route('/', methods=['POST'])
@jwt_required()
def add_recipe():
    try:
        user_id = get_jwt_identity()
        body = request.get_json()
        user = User.objects.get(id=user_id)
        recipe = Recipe(**body, added_by=user)
        recipe.save()
        user.update(push__recipes=recipe)
        user.save()
        id = recipe.id
        return {'id': str(id)}, 200
    except FieldDoesNotExist:
        return jsonify(FieldError()), 400
    except ValidationError:
        return jsonify(SchemaValidationError()), 400
    except NotUniqueError:
        return jsonify(AlreadyExistsError("Przepis")), 400
    except Exception as e:
        return jsonify(InternalServerError()), 404


@api.route('/<id>', methods=['PUT'])
@jwt_required()
def update_recipe(id):
    try:
        user_id = get_jwt_identity()
        recipe = Recipe.objects.get(id=id, added_by=user_id)
        body3 = request.get_json()
        Recipe.objects.get(id=id).update(**body3)
        Recipe.objects.get(id=id).update_date()
        return {'id': str(id)}, 200
    except InvalidQueryError:
        return jsonify(SchemaValidationError()), 400
    except ValidationError:
        return jsonify(SchemaValidationError()), 400
    except DoesNotExist:
        return jsonify(UpdatingError()), 403
    except Exception as e:
        if e.code:
            return jsonify(e.description), 400
        else:
            return jsonify(InternalServerError()), 404


@api.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(id):
    try:
        user_id = get_jwt_identity()
        recipe = Recipe.objects.get(id=id, added_by=user_id)
        recipe.delete()
        return '', 200
    except DoesNotExist:
        return jsonify(DeletingError()), 403
    except Exception:
        return jsonify(InternalServerError()), 404


@api.route('/<id>', methods=['GET'])
@jwt_required()
def get_gas_id(id):
    try:
        #user_id = get_jwt_identity()
        recipe = Recipe.objects.get(id=id)#, added_by=user_id)

        def re():
            yield '{"TIME":' + str(time()) + ',"Recipe":['
            yield recipe.to_json() + ']}'

        return Response(re(), mimetype="application/json", status=200)
    except DoesNotExist:
        return jsonify(NotExistsError("Przepis")), 400
    except Exception:
        return jsonify(InternalServerError()), 404


'''
  {
    "name": "tort",
    "type": "ciasto",
    "photo": "",
    "recipe": "miejsce na przepis"
  }
'''
