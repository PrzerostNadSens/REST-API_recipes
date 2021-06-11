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
    "name": "test_1",
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

użytkownik 2
{
    "mail": "przyklaowy@test.com",
    "password": "trudne_haslo.123"
}

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyMzQzMTc1NywianRpIjoiZTkyYWIzYTYtMTY5Ny00MWU3LWFhOWItYzc1YzEwMmQ3NjEwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYwYzM5YTIzOWE2NTVmZjdiNmVmMDUyNiIsIm5iZiI6MTYyMzQzMTc1NywiZXhwIjoxNjI0MDM2NTU3fQ.M5DICHRPm9Rr8VD_ZsvSKh8ibYd0Onv8NrNf-Sua-Y0

'''
