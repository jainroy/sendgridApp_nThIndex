import sendgrid
from sendgrid.helpers.mail import Mail, Personalization, Email, Content
from decouple import config

SENDGRID_API_KEY = config("SENDGRID_API_KEY")

def send_basic_email(to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    mail = Mail(
        from_email='jainroyp.dist@gmail.com',
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )
    response = sg.send(mail)
    return response.status_code


def send_bulk_email(to_emails, subject, content):
    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    from_email='jainroyp.dist@gmail.com'
    mail = Mail()
    mail.from_email = Email(from_email)
    mail.subject = subject
    mail.add_content(Content("text/plain", content))

    for to_email in to_emails:
        personalization = Personalization()
        personalization.add_to(Email(to_email))
        mail.add_personalization(personalization)
    response = sg.send(mail)
    return response.status_code
