from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_html(activation, request):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    activation_link = "{0}/auth/activations/activate/{1}/".format(
        current_site, activation.uuid)
    if activation.full_name:
        message = render_to_string('page1.html',
                                   {'name': activation.full_name,
                                    'link': activation_link})
    else:
        message = render_to_string('page1.html',
                                   {'name': activation.email,
                                    'link': activation_link})
    msg = EmailMessage(mail_subject, message, to=[activation.email])
    msg.content_subtype = "html"
    msg.send()
