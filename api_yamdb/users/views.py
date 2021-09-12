from django.core.mail import send_mail
from django.conf import settings

settings.configure()

send_mail(
    subject='confirmation code',
    message='bla-bla',
    from_email='admin@yamdb.ru',
    recipient_list='email',
    fail_silently=False
)

