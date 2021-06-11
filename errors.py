def page_not_found(e):
    return {
        "message": "Nie znaleziono.",
        "status": 404
    }, 404

def InternalServerError():
    return {
        "message": "Coś poszło nie tak.",
        "status": 404
    }


def SchemaValidationError():
    return {
        "message": "Nieprawidłowy format danych.",
        "status": 400
    }


def FieldError():
    return {
        "message": "W żądaniu brakuje wymaganych pól.",
        "status": 400
    }


def AlreadyExistsError(name):
    return {
        "message": name + " o podanych danych już istnieje.",
        "status": 400
    }


def UpdatingError():
    return {
        "message": "Nie posiadasz uprawnień aby zaktualizować.",
        "status": 403
    }


def DeletingError():
    return {
        "message": "Nie posiadasz uprawnień aby usunąć.",
        "status": 403
    }


def NotExistsError(name):
    return {
        "message": name + " o podanym identyfikatorze nie istnieje.",
        "status": 400
    }


def UnauthorizedError():
    return {
        "message": "Nieprawidłowa nazwa użytkownika lub hasło.",
        "status": 401
    }


def EmailAlreadyExistsError():
    return {
         "message": "Użytkownik z podamym adresem email już istnieje.",
         "status": 400
     }


