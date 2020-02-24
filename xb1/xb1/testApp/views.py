from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from .forms import AnimalForm
from .models import Animal


class AnimalListView(ListView):

    model = Animal
    template_name = "animals.html"

    def get_context_data(self, *args, **kwargs):

        context = super(AnimalListView, self).get_context_data(*args, **kwargs)

        context["now"] = timezone.now()
        return context


class AnimalCreateView(FormView):

    template_name = "animals_form.html"
    form_class = AnimalForm
    success_url = reverse_lazy("testApp:animal_list")


    def form_valid(self, form):

        form.instance.save()
        return super(AnimalCreateView, self).form_valid(form)
