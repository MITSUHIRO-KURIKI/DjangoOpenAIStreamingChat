@rem makemigrations の実行
python manage.py makemigrations axes
python manage.py makemigrations access_security
python manage.py makemigrations social_django
python manage.py makemigrations accounts
python manage.py makemigrations user_properties
python manage.py makemigrations inquiry
python manage.py makemigrations chat
python manage.py makemigrations

@rem migrate の実行
python manage.py migrate axes
python manage.py migrate access_security
python manage.py migrate social_django
python manage.py migrate accounts
python manage.py migrate user_properties
python manage.py migrate inquiry
python manage.py migrate chat
python manage.py migrate

@rem createsuperuser の実行
python manage.py createsuperuser