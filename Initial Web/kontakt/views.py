from django.shortcuts import render, redirect
from xb1.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


# home page view
def home(request):
    return render(request, 'home.html')


# contact page view - when user wants to send a message, it will be sent to adamtranquangvu@gmail.com and user
# will be redirected to home page
def kontakt(request):
    if request.method == 'POST':
        message = request.POST['feedback']
        topic = request.POST['topic']
        name = request.POST['name']

        if 0 < len(message) <= 2000 and 0 < len(topic) <= 100 and 0 < len(name) <= 100:
            message = message + '\n\n' + 'From: ' + name
            send_mail(topic, message, EMAIL_HOST_USER, ['xb1.feedback@gmail.com'], fail_silently=False)
            return redirect('home')

    else:
        return render(request, 'kontakt.html')
