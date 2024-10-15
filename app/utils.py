from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText

# Define the subject and body of the email.
subject = "Donacion Ohana!"
a = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agradecimiento por su Donación</title>
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
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            text-align: center;
        }
        .content {
            padding: 20px;
            text-align: center;
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
            <h1>¡Gracias por su Generosa Donación!</h1>
        </div>
        <div class="content">
            <p>Estimado/a Donante,</p>
            <p>Queremos expresar nuestro más sincero agradecimiento por su contribución de <strong>
            
            """

b = """
</strong> durante el evento <strong>
"""

c = """
</strong>.</p>
            <p>Su apoyo es invaluable para nosotros y nos ayudará a continuar con nuestra misión.</p>
            <p>Gracias por hacer una diferencia.</p>
            <p>Con agradecimiento,</p>
            <p>El Equipo de Ohana!</p>
        </div>
        <div class="footer">
            <p>Este correo fue enviado a usted porque hizo una donación en nuestro evento. Si tiene alguna pregunta, por favor contacte a nuestro soporte.</p>
        </div>
    </div>

</body>
</html>
"""

body = a + b + c


def build_body(amount, event):
    return a + " " + str(amount) + " " + b + " " + event + c


# Define the sender's email address.
sender = "ohana.notifications.utn@gmail.com"
# Password for the sender's email account.
password = "onig bstu avxk qpvh"


def send_email(
    recipient, subject=subject, body_html=body, sender=sender, password=password
):
    # Crear el objeto de mensaje multipart
    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    # Crear la parte HTML
    html_part = MIMEText(body_html, "html")

    # Adjuntar la parte HTML al mensaje
    msg.attach(html_part)

    # Iniciar la conexión con el servidor SMTP
    smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtpserver.ehlo()
    smtpserver.login(sender, password)

    # Enviar el correo
    smtpserver.sendmail(sender, recipient, msg.as_string())

    # Cerrar la conexión
    smtpserver.close()
