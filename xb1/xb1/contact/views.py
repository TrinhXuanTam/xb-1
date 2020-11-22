from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from .forms import ContactForm
from ..core.views import LoginMixinView
from ..settings import EMAIL_HOST_USER, FEEDBACK_EMAIL

# Create your views here.


class ContactFormView(FormView):
    """
    Contact form for authenticated users,
    sends message to email specified in settings.py
    """
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        try:
            with transaction.atomic():

                message = form.cleaned_data["message"] + "\n\nFrom: " + self.request.user.username
                subject = form.cleaned_data["subject"]
                send_mail(subject, message, EMAIL_HOST_USER, [FEEDBACK_EMAIL], fail_silently=False)
                messages.success(self.request, _("Email has been successfully sent."))
                return super(ContactFormView, self).form_valid(form)
        except Exception as e:
            messages.warning(self.request, _("Error trying to send email. If problem persists, please contact staff members."))
            return super(ContactFormView, self).form_invalid(form)

