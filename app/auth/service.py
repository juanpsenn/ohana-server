from typing import Optional

from django.contrib.auth import models as auth_models
from django.db import IntegrityError
from django_mercadopago.models import Account
from rest_framework.authtoken.models import Token

from app import models

from random import randint

from app.utils import send_email

a = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recuperación de Contraseña</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .header {
            background-color: #3498db;
            color: white;
            padding: 10px;
            text-align: center;
        }
        .content {
            padding: 20px;
            text-align: center;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
        }
        .footer {
            font-size: 12px;
            text-align: center;
            color: #666;
            padding: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Recuperación de Contraseña</h1>
        </div>
        <div class="content">
            <p>Estimado/a Usuario,</p>
            <p>Hemos recibido una solicitud para restablecer la contraseña de su cuenta. Si usted no ha realizado esta solicitud, por favor ignore este correo electrónico.</p>
            <p>Para restablecer su contraseña, haga clic en el siguiente enlace:</p>
            
            """
b = """
            <p>Si necesita ayuda adicional, no dude en contactar a nuestro equipo de soporte.</p>
            <p>Gracias por usar nuestros servicios.</p>
            <p>Atentamente,</p>
            <p>El Equipo de Ohana</p>
        </div>
        <div class="footer">
            <p>Este correo fue enviado a usted porque se solicitó un restablecimiento de contraseña para su cuenta. Si no solicitó este cambio, por favor contacte a nuestro soporte inmediatamente.</p>
        </div>
    </div>
</body>
</html>
"""

def signin(user: auth_models.User):
    # delete old token
    try:
        user.auth_token.delete()
    except auth_models.User.auth_token.RelatedObjectDoesNotExist:
        pass

    # create new one
    token, created = Token.objects.get_or_create(user=user)
    return token


def signup(
    *,
    username: str,
    password: str,
    email: str,
    first_name: str,
    last_name: str,
    phone: str,
    country: Optional[int],
    province: str,
    city: str,
) -> auth_models.User:
    user = auth_models.User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    models.UserInfo.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        country_id=country,
        province=province,
        phone=phone,
        city=city,
    )
    return user

def recover_password(username):
    user = None
    try:
        user = auth_models.User.objects.get(username=username)
    except auth_models.User.DoesNotExist:
        return False

    if user:
        recovery_code = ""
        try:
            recovery_code = models.RecoveryCode.objects.create(username=username, code=randint(100000,999999))
        except IntegrityError:
            old_code = models.RecoveryCode.objects.get(username=username)
            old_code.delete()
            recovery_code = models.RecoveryCode.objects.create(username=username, code=randint(100000,999999))
        body = a + f"localhost:8000/app/recover/password/?code={recovery_code.code}" + b
        send_email(recipient=user.email, subject="Ohana - Recuperación de constaseña", body_html=body)
    

def create_mp_account(*, name: str, user: int, app_id: str, secret_key: str) -> Account:
    return Account.objects.create(
        name=name,
        slug=f"{user}-{name.replace(' ', '-')}",
        app_id=app_id,
        secret_key=secret_key,
        sandbox=False,
    )
