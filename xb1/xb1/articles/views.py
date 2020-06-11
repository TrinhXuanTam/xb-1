from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
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
from .models import Article, Comment, Category, Tag
from ..core.models import Profile
from ..core.views import LoginMixinView

from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from functools import reduce

class ArticleListView(LoginMixinView, ListView):
    model = Article
    template_name = "articles.html"
    ordering = ['-modified']

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all()
        for article in context['object_list']:
            article.article_tags = Tag.objects.filter(article=article).order_by('name')
        return context


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
        context  = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        article  = Article.objects.get(slug=kwargs['slug'])
        comments = []

        if article.allow_comments:
            q_comments = Comment.objects.filter(article=article, reaction_to=None)

            for comment in q_comments:
                comments.append({
                    "author": comment.author,
                    "text": comment.text,
                    "date": comment.date,
                    "id": comment.pk,
                    "comments": self.get_comment_childs(comment),
                    "is_censured": comment.is_censured
                })

        article_tags       = Tag.objects.filter(article=article)
        article_categories = Category.objects.filter(article=article)

        context['article']    = article
        context['comments']   = comments
        context['categories'] = article_categories
        context['tags']       = article_tags

        return context

    def get_comment_childs(self, parent):

        res = []

        for comment in parent.comment_set.all():
            res.append({
                "author": comment.author,
                "text": comment.text,
                "date": comment.date,
                "id": comment.pk,
                "comments": self.get_comment_childs(comment),
                "is_censured": comment.is_censured
            })

        return res

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return render(request, 'articles_detail.html', self.get_context_data(*args, **kwargs))


class PostCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            article_id = int(request.POST.get('article_id'))
            reaction_to_id = int(request.POST.get('comment_id'))
            comment_text = request.POST.get('text')
            comment = Comment(
                text=comment_text,
                author_id=request.user.id,
                article_id=article_id
            )
            if reaction_to_id >= 0:
                comment.reaction_to_id=reaction_to_id

            comment.save()
            comment.user = Profile.objects.get(user_id=request.user.id)
            context = {
                "comments":[comment],
                "article": Article.objects.get(id=article_id)
            }
            return render(request, 'article_comment.html', context)
        else:
            response = JsonResponse({"error": "Unauthorized"})
            response.status_code = 401
            return response


class GetArticlesByCategoryView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.filter(category=request.GET.get('category'))
        for article in articles:
            article.article_tags = Tag.objects.filter(article=article).order_by('name')
        return render(request, 'get_articles.html', {"articles":articles})


class GetAllArticlesView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().order_by('-modified')
        for article in articles:
            article.article_tags = Tag.objects.filter(article=article).order_by('name')
        return render(request, 'get_articles.html', {"articles":articles})


class ArticleSearchView(View):
    def get(self, request, *args, **kwargs):
        keywords       = request.GET.get('keywords').split()
        tags_query     = reduce(lambda x, y: x | y, [Q(name__icontains=keyword) for keyword in keywords])
        articles_query = reduce(lambda x, y: x | y, [Q(title__icontains=keyword) for keyword in keywords])
        tags           = Tag.objects.filter(tags_query)
        articles       = Article.objects.filter(Q(tags__in=tags) | Q(articles_query)).distinct().order_by('-modified')
        for article in articles:
            article.article_tags = Tag.objects.filter(article=article).order_by('name')
        return render(request, 'get_articles.html', {"articles":articles})


class ArticleDeleteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(id=int(request.POST.get('article_id')))
        if self.request.user == article.author:
            article.delete()
            response = JsonResponse({"ok": "deleted"})
            response.status_code = 204
            return response
        else:
            response = JsonResponse({"error": "Unauthorized"})
            response.status_code = 401
            return response


class HideArticleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        article = Article.objects.get(id=int(request.POST.get('article_id')))
        if self.request.user == article.author:
            article.article_state = 0
            article.save()
            response = JsonResponse({"ok": "hidden"})
            response.status_code = 200
            return response
        else:
            response = JsonResponse({"error": "Unauthorized"})
            response.status_code = 401
            return response


class PublishArticleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        article = Article.objects.get(id=int(request.POST.get('article_id')))
        if self.request.user == article.author:
            article.article_state = 1
            article.save()
            response = JsonResponse({"ok": "published"})
            response.status_code = 200
            return response
        else:
            response = JsonResponse({"error": "Unauthorized"})
            response.status_code = 401
            return response


class BanCommentView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = "articles.change_comment"

    def get(self, request, *args, **kwargs):

        comment = Comment.objects.get(pk=kwargs["pk"])

        comment.is_censured = True
        comment.save()

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class UnbanCommentView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = "articles.change_comment"

    def get(self, request, *args, **kwargs):

        comment = Comment.objects.get(pk=kwargs["pk"])

        comment.is_censured = False
        comment.save()

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
