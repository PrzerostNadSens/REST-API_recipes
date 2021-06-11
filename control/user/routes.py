from flask import Blueprint, request, Response, jsonify

from model.user.routes import User
from time import time

from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from errors import SchemaValidationError, AlreadyExistsError, InternalServerError, UpdatingError, DeletingError, \
    NotExistsError, FieldError

MOD_NAME = "User"
IGNORED = False
api = Blueprint(MOD_NAME, __name__)


@api.route('/', methods=['GET'])
def get_us():
    try:
        def user():
            yield '{"TIME":' + str(time()) + ',"User":['
            dot = False
            for item in User.objects():
                if dot:
                    yield ','
                yield item.to_json()
                dot = True
            yield ']}'
        return Response(user(), mimetype="application/json", status=200)
    except DoesNotExist:
        return jsonify(NotExistsError("Użytkownik")), 400
    except Exception as e:
        return jsonify(InternalServerError()), 404

@api.route('/', methods=['POST'])
def add_user():
    try:
        body = request.get_json()
        user = User(**body).save()
        id = user.id
        return {'id': str(id)}, 200
    except FieldDoesNotExist:
        return jsonify(FieldError()), 400
    except ValidationError:
        return jsonify(SchemaValidationError()), 400
    except NotUniqueError:
        return jsonify(AlreadyExistsError("Użytkownik")), 400
    except Exception as e:
        return jsonify(InternalServerError()), 404



@api.route('/<id>', methods=['PUT'])
def update_user(id):
    try:
        body1 = request.get_json()
        User.objects.get(id=id).update(**body1)
        return {'id': str(id)}, 200
    except InvalidQueryError:
        return jsonify(SchemaValidationError()), 400
    except ValidationError:
        return jsonify(SchemaValidationError()), 400
    except DoesNotExist:
        return jsonify(UpdatingError()), 403
    except NotUniqueError:
        return jsonify(AlreadyExistsError("Użytkownik")), 400
    except Exception as e:
        if e.code:
            return jsonify(e.description), 400
        else:
            return jsonify(InternalServerError()), 404


@api.route('/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.objects.get(id=id).delete()
        return '', 200
    except DoesNotExist:
        return jsonify(DeletingError()), 403
    except Exception:
        return jsonify(InternalServerError()), 404


@api.route('/<id>', methods=['GET'])
def get_user(id):
    try:
        User.objects.get(id=id)

        def user():
            yield '{"TIME":' + str(time()) + ',"User":['
            yield User.objects.get(id=id).to_json() + ']}'

        return Response(user(), mimetype="application/json", status=200)
    except DoesNotExist:
        return jsonify(NotExistsError("Użytkownik")), 400
    except Exception:
        return jsonify(InternalServerError()), 404

'''  
{
    "name": "test_1",
    "subname": "tak",
    "mail": "przykladowy@test.com",
    "login": "test_test",
    "phone": "123123123",
    "password": "trudne_haslo.123"
}
'''