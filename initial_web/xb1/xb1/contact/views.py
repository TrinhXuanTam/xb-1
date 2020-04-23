from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from .forms import ContactForm
from ..settings import EMAIL_HOST_USER, FEEDBACK_EMAIL

# Create your views here.

class ContactFormView(FormView):

    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("index")


    def form_valid(self, form):

        message = form.cleaned_data["message"]
        topic = form.cleaned_data["topic"]
        send_mail(topic, message, EMAIL_HOST_USER, [FEEDBACK_EMAIL], fail_silently=False)

        return super(ContactFormView, self).form_valid(form)
