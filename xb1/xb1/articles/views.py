from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render
from django.http import HttpResponse

from .forms import ArticleForm
from .models import Article, Comment
from ..core.models import Profile
from ..core.views import LoginMixinView

from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

class ArticleListView(LoginMixinView, ListView):
    model = Article
    template_name = "articles.html"


class ArticleCreateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    template_name = "articles_form.html"
    form_class = ArticleForm
    success_url = reverse_lazy("articles:article_list")
    permission_required = "articles.add_article"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)


class ArticleUpdateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Article
    template_name = "articles_form.html"
    form_class = ArticleForm
    success_url = reverse_lazy("articles:article_list")
    permission_required = "articles.change_article"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleUpdateView, self).form_valid(form)

class ArticleDetailView(LoginMixinView, DetailView):
    model = Article
    template_name = "articles_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        article = Article.objects.get(slug=kwargs['slug'])
        comments = None
        if article.allow_comments:
            comments = Comment.objects.filter(article=article.id, reaction_to_id=None).order_by('date').reverse()
            # Get comments with user data
            for comment in comments:
                comment.user = Profile.objects.get(user_id=comment.author_id)
                # Get replies to given comment
                comment.replies = Comment.objects.filter(reaction_to_id=comment.id).order_by('date')
                for reply in comment.replies:
                    reply.user = Profile.objects.get(user_id=reply.author_id)
        context['article'] = article
        context['comments'] = comments
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return render(request, 'articles_detail.html', self.get_context_data(*args, **kwargs))

class PostCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            article_id = int(request.POST.get('article'))
            comment_text = request.POST.get('text')
            new_comment = Comment(text=comment_text, author_id=request.user.id, article_id=article_id)
            new_comment.save()
            new_comment.user = Profile.objects.get(user_id=request.user.id)
            context = {"comment":new_comment, "article": Article.objects.get(id=article_id)}
            return render(request, 'new_comment.html', context)
        else:
            response = JsonResponse({"error": "Unauthorized"})
            response.status_code = 401
            return response

class PostCommentReplyView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            reply_text = request.POST.get('text')
            article_id = int(request.POST.get('article'))
            reaction_id = int(request.POST.get('comment_id'))
            new_reply = Comment(text=reply_text, author_id=request.user.id, article_id=article_id, reaction_to_id=reaction_id)
            new_reply.save()
            new_reply.user = Profile.objects.get(user_id=request.user.id)
            return render(request, 'new_reply.html', {"reply":new_reply})
        else:
            response = JsonResponse({"error": "Unauthorized"})
            response.status_code = 401
            return response