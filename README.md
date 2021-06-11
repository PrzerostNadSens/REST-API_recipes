# REST-API_recipes

## Instalacja

Urządzenie z zainstalowanym środowiskiem Python 3 lub nowszym (aplikacja pisana w oparciu o Python 3.8) wraz z
zainstalowanym systemem pakietów z listy `requirements.txt`.

Komenda do instalacji pakietów:

```shell
pip install -r requirements.txt
```

## Uruchomienie

```shell
export FLASK_ENV=development
export FLASK_DEBUG=1
python app.py
```

> Wyjaśnienie:\
> `FLASK_ENV=development` - środowisko produkcyjne, puste oznacza produkcje \
> `FLASK_DEBUG=` `1`(ON) / `0`(OFF) W wypadku błędu wyślij jego opis w odpowiedzi\
> `python app.py --host=0.0.0.0` uruchomi serwer w trybie publicznym i będzie akceptować połączenie z poza urządzenia
> lokalnego, można to też ustawić w kodzie.

## Dodatkowe uwagi

W wypadku dodania nowych pakietów proszę zaktualizować plik `requirements.txt` ręcznie lub używając komendy:

```shell
python -m pip freeze > requirements.txt
```

Zaowocuje to uzupełnieniem pliku requirements.txt o listę wszystkich zainstalowanych pakietów w danym środowisku.

## katalog control

Zawiera paczki kodu które są automatycznie importowane wraz z startem serwera oraz zawierają kod odpowiedzialny za
obsługę endpointów. Każda paczka powinna składać się z pliku:`__init__.py` zawierającego informacje jakie obiekty można
zaimportować z paczki oraz co najmniej jeden plik z konfiguracją i kodem obsługującym endpointy. W celu poprawnego
importu paczka mui zawierać parametry takie jak:

- `api`(structura flask.Blueprint),
- `MOD_NAME`(nazwa endpointu, może różnić się od nazwy paczki),
- `IGNORED`(informacja czy paczka ma być ignorowana).

## Baza danych a katalog model

W katalogu model powinny znajdować się pliki odpowiedzialne za łączenie z bazą danych oraz opisujące strukturę tych
danych. Nie narzucam koncepcji, ale wolał bym gdyby było rozłożone to na kilka plików w celu ułatwienia późniejszej
współbieżnej pracy na nich. Przykładowa forma jaką wykorzystywałem w poprzednim projekcie znajduje się w
pliku `example.py` oraz sposób inicjacji jest umieszczony (lecz za komentowany) w pliku `app.py`.

## Elementy statyczne

Elementy statyczne takie jak np. grafika można umieszczać w folderze `static`, o ile nie istnieje należy go utworzyć.
