# Framework Imports
from django.conf import settings

# External Imports
from email.mime.text import MIMEText
import smtplib
import ssl


def send_email(
    EMAIL_SUBJECT,
    EMAIL_CONTENT,
    EMAIL_TO,
    EMAIL_HOST_USER=settings.EMAIL_HOST_USER,
    DEFAULT_FROM_EMAIL=settings.DEFAULT_FROM_EMAIL,
    EMAIL_HOST=settings.EMAIL_HOST,
    EMAIL_PORT=settings.EMAIL_PORT,
    EMAIL_HOST_PASSWORD=settings.EMAIL_HOST_PASSWORD,
):
    """
    Send an email to a given end user.
    """
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        if "gmail" in EMAIL_HOST:
            context = ssl.create_default_context()
            server.starttls(context=context)
        else:
            server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        if not isinstance(EMAIL_TO, list):
            EMAIL_TO = [EMAIL_TO]
        for EMAIL_TO_i in EMAIL_TO:
            msg = MIMEText(EMAIL_CONTENT, "html")
            msg["Subject"] = EMAIL_SUBJECT
            msg["From"] = DEFAULT_FROM_EMAIL
            msg["To"] = EMAIL_TO_i
            try:
                server.sendmail(EMAIL_HOST_USER, [EMAIL_TO_i], msg.as_string())
                print("Sent email to: ", EMAIL_TO_i)
            except:
                print("Fail email to: ", EMAIL_TO_i)
        server.quit()


def format_validation_email_content(globals, user, domain, code):
    return {
        "EMAIL_SUBJECT": f"Verify Email ({globals.site_name})",
        "EMAIL_CONTENT": f"Hi {user.first_name} {user.last_name},<br/><br/>Welcome to {globals.site_name}!<br/><br/>To get started please verify your email by clicking <a href='{domain}/auth/validate_email?code={code}'>here</a>.<br/><br/> Thank you!<br/><br/>The {globals.site_name} Team",
        "EMAIL_TO": user.email,
    }
