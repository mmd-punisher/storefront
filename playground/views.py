from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage


# def say_hello(request):
#     try:
#         # send_mail('subject', 'message', 'mohammadmoosapoor03@gmail.com', ['mohammadmoosapoor4@gmail.com'])
#         # mail_admins('subject', 'message', html_message='message')
#         message = EmailMessage('subject', 'message', 'mohammadmoosapoor03@gmail.com', ['receive@mmd.com'])
#         message.attach_file('playground/static/images/img.jpg')
#         message.send()
#     except BadHeaderError:
#         pass
#     return render(request, 'hello.html', {'name': 'Mohammad'})
def say_hello(request):
    try:
        message = BaseEmailMessage(
            template_name='emails/hello.html',
            context={'name': 'Mohammad'}

        )
        message.send(to=['mohammadmoosapoor4@gmail.com'])
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Mohammad'})
