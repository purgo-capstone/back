# Purgo CRM Backend

- Django

- DjangoRestFramework

- Drf-Spectacular

### Install and Run Purgo Backend

Install Dependencies

```
$ cd pip install -r requirements.txt
```
Migrate database

```
$ python manage.py migrate
```

And Run server
```
$ python manage.py runserver --no-reload
```

### Change Server Settings

change SERVER to local, aws based on db 
```
SERVER = 'local'
if SERVER == 'local':
    # Local Sqlite db
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
    }
elif SERVER == 'aws':
    # Amazon aws ec2 server db
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv("NAME"),
            'USER': os.getenv("USER"),
            'PASSWORD': os.getenv("PASSWORD"),
            'HOST': os.getenv("HOST"),
            'PORT': os.getenv("PORT"),
        }    
    }
```

### Backend API Swagger 
Run server and go [here](http://localhost:8000/api/schema/swagger-ui/)

or use the url endpoint below
```
/api/schema/swagger-ui/
```
Redoc
```
/api/schema/redoc/
```
Swagger ui should provide a page like this:

![image](https://github.com/purgo-capstone/back/assets/64758800/42336a0b-5add-4fff-b5ac-87148e0de6bb)
