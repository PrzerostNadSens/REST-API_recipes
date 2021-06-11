from flask import Blueprint, request, Response, jsonify

from model.user.routes import User
from time import time
import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from errors import SchemaValidationError, AlreadyExistsError, InternalServerError, UpdatingError, DeletingError, \
    NotExistsError, FieldError, UnauthorizedError

MOD_NAME = "User"
IGNORED = False
api = Blueprint(MOD_NAME, __name__)


@api.route('/', methods=['GET'])
@jwt_required()
def get_us():
    try:
        user_id = get_jwt_identity()
        user_profile = User.objects.get(id=user_id)
        if user_profile.administrator == True:
            user_profile = User.objects()
        else:
            user_profile = ""

        def user():
            yield '{"TIME":' + str(time()) + ',"User":['
            dot = False
            for item in user_profile:
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


@api.route('/Login', methods=['POST'])
def log_user():
    body = request.get_json()
    user = User.objects.get(mail=body.get('mail'))
    authorized = user.check_password(body.get('password'))
    if not authorized:
        return UnauthorizedError()

    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)
    return {'token': access_token}, 200


@api.route('/', methods=['POST'])
def add_user():
    try:
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        user.save()
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
@jwt_required()
def update_user(id):
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
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
@jwt_required()
def delete_user(id):
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        user.delete()
        return '', 200
    except DoesNotExist:
        return jsonify(DeletingError()), 403
    except Exception:
        return jsonify(InternalServerError()), 404


@api.route('/Profile', methods=['GET'])
@jwt_required()
def get_user():
    try:
        user_id = get_jwt_identity()
        user_profile = User.objects.get(id=user_id).to_json()

        def user():
            yield '{"TIME":' + str(time()) + ',"User":['
            yield user_profile + ']}'

        return Response(user(), mimetype="application/json", status=200)
    except DoesNotExist:
        return jsonify(NotExistsError("Użytkownik")), 400
    except Exception:
        return jsonify(InternalServerError()), 404


'''  
{
    "first_name": "test_1",
    "subname": "tak",
    "mail": "przykladowy@test.com",
    "login": "test_test",
    "phone": "123123123",
    "password": "trudne_haslo.123"
}
użytkownik 1

{
    "mail": "przykladowy@test.com",
    "password": "trudne_haslo.123"
}

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMzQzOTE5MCwianRpIjoiMDlhMjE1YjItOTEyNy00ODhkLWE5MGMtNjIzNTgwYmU0MmYzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYwYzNiNmZmNDI3MjZlMGQ4YzE4NmM2ZSIsIm5iZiI6MTYyMzQzOTE5MCwiZXhwIjoxNjI0MDQzOTkwfQ.icSf6jy_D-dYYMIGOEa7tRR4hnK1n6eW033o_hZqsXI

użytkownik 2
{
    "mail": "przykladowy2@tes2t.com",
    "password": "trudne_haslo.1232"
}

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMzQzNjQ0MiwianRpIjoiZGFlYzc1OTUtNmZiNC00MDFhLTlkYTUtNGE3MjQ5ZjIwN2NhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYwYzNhYzdkNzVjY2IwN2M4OGQwNDc1NSIsIm5iZiI6MTYyMzQzNjQ0MiwiZXhwIjoxNjI0MDQxMjQyfQ.-V6al_N-pG2reWMXTgOzIvvOfMZO5vUYVzV7formtdc
'''
'''
admin

{
    "mail": "przykladoAwy@test.com",
    "password": "trudne_haslo.123"
}

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMzQzNzIyNiwianRpIjoiNThiNzg0N2EtNDg1MC00OTlmLTkwMDQtZjZlMmE4NmE5NWQxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYwYzNhZjk5ZDYwNjc3MDA3M2FjOGI4ZCIsIm5iZiI6MTYyMzQzNzIyNiwiZXhwIjoxNjI0MDQyMDI2fQ.-MotC99KoT7tTzcmCRHQGPdVvUth4q7FECDZZQu1s2w




'''
