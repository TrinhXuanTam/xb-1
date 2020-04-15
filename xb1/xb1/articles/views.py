from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render

from .forms import AnimalForm, ArticleForm
from .models import Animal, Article
from ..core.views import LoginMixinView


class ArticleListView(LoginMixinView, ListView):
    model = Article
    template_name = "articles.html"


class ArticleCreateView(LoginMixinView, LoginRequiredMixin, CreateView):

    template_name = "articles_form.html"
    form_class = ArticleForm
    success_url = reverse_lazy("articles:article_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)


class ArticleUpdateView(LoginMixinView, LoginRequiredMixin, UpdateView):

    model = Article
    template_name = "articles_form.html"
    form_class = ArticleForm
    success_url = reverse_lazy("articles:article_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleUpdateView, self).form_valid(form)


class AnimalListView(ListView):
    """
    TODO - just for testing -will be deleted
    """

    model = Animal
    template_name = "animals.html"

    def get_context_data(self, *args, **kwargs):
        context = super(AnimalListView, self).get_context_data(*args, **kwargs)

        context["now"] = timezone.now()
        return context


class AnimalCreateView(LoginRequiredMixin, FormView):
    """
    TODO - just for testing -will be deleted
    """

    template_name = "animals_form.html"
    form_class = AnimalForm
    success_url = reverse_lazy("articles:animal_list")

    def form_valid(self, form):
        form.instance.save()
        return super(AnimalCreateView, self).form_valid(form)
