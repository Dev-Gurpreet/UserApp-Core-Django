Functionalities cover in thia app: 
SignUp with email verification, 
Login, 
Logout, 
decorators (restrict user to access some pages), 
Reset password with email verification

1. install python
2. pip install Django
3. python manage.py migrate
4. python manage.py makemigrations
5. python manage.py create superuser

6. Setup following variables with your host email and password in setting.py file
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''

7. Go to Less secure app access option of gmail account and turn it ON

8. python manage.py runserver