from django.core.mail import send_mail


def send_activation_email(user):
    subject = 'Thank you for registering to our site'
    body = 'Thank you for registering to our site.\n'\
           'For activation follow this link: '\
           f'http://127.0.0.1:8000/account/activate/{user.activation_code}/'
    from_email = 'test@django.kg'
    recipients = [user.email]
    send_mail(subject=subject, message=body, from_email=from_email, recipient_list=recipients, fail_silently=False)
