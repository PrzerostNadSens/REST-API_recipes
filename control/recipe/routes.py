from time import time

from flask import Blueprint, request, Response, jsonify
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

from errors import SchemaValidationError, AlreadyExistsError, InternalServerError, UpdatingError, DeletingError, \
    NotExistsError, FieldError
from model.recipe import Recipe

MOD_NAME = "Recipe"
IGNORED = False
api = Blueprint(MOD_NAME, __name__)



@api.route('/', methods=['GET'])
def recipe():
    query = {}

    try:
        if 'name' in request.args:
            query['name'] = request.args['name']
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
def add_recipe():
    try:
        body = request.get_json()
        recipe = Recipe(**body).save()
        id = recipe.id
        return {'id': str(id)}, 200
    except FieldDoesNotExist:
        return jsonify(FieldError()), 400
    except ValidationError:
        return jsonify(SchemaValidationError()), 400
    except NotUniqueError:
        return jsonify(AlreadyExistsError("Przepis")), 400
    except Exception as e:
        if e.code:
            return jsonify(e.description), 400
        else:
            return jsonify(InternalServerError()), 404


@api.route('/<id>', methods=['PUT'])
def update_recipe(id):
    try:
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
def delete_recipe(id):
    try:
        Recipe.objects.get(id=id).delete()
        return '', 200
    except DoesNotExist:
        return jsonify(DeletingError()), 403
    except Exception:
        return jsonify(InternalServerError()), 404


@api.route('/<id>', methods=['GET'])
def get_gas_id(id):
    try:
        recipe = Recipe.objects.get(id=id)

        def recipe():
            yield '{"TIME":' + str(time()) + ',"Recipe":['
            yield recipe.to_json() + ']}'

        return Response(recipe(), mimetype="application/json", status=200)
    except DoesNotExist:
        return jsonify(NotExistsError("Przepis")), 400
    except Exception:
        return jsonify(InternalServerError()), 404


'''
  {
    "name": "tort",
    "type": "ciasto",
    "photo": "",
    "recipe": "miejsce na przepis",
    "userId": "60c35584c44310836596e757"
  }
'''