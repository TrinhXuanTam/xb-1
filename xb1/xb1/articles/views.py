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
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models.functions import Lower

from .forms import ArticleForm
from .models import Article, Comment, Category, Tag
from ..core.models import Profile
from ..core.views import LoginMixinView

from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from functools import reduce


class ArticleListView(LoginMixinView, ListView):
    """
    Renders a list of all articles.
    Articles marked as hidden are only rendered for authorized users with sufficient privileges.
    Users with sufficient privileges are able to create, edit and delete articles.
    """

    model = Article
    template_name = "articles.html"
    ordering = ['-modified']

    def get_context_data(self, *args, **kwargs):
        """Adds categories to context and assigns tags to articles."""

        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().order_by(Lower("name"))
        for article in context['object_list']:
            article.article_tags = Tag.objects.filter(article=article).order_by('name')
        return context


class ArticleCreateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Creates a new article if user has sufficient privileges for managing articles.
    """

    template_name = "articles_form.html"
    form_class = ArticleForm
    success_url = reverse_lazy("articles:article_list")
    permission_required = "articles.add_article"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)


class ArticleUpdateView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Updates an article if user has sufficient privileges for managing articles.
    """

    model = Article
    template_name = "articles_form.html"
    form_class = ArticleForm
    success_url = reverse_lazy("articles:article_list")
    permission_required = "articles.change_article"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleUpdateView, self).form_valid(form)


class TagCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Dynamically creates new tags via AJAX.
    Sufficient privileges for managing articles are required in order to create new tags.
    """

    permission_required = "articles.change_article"

    def post(self, request, *args, **kwargs):
        """A new tag will be created if and only if the tag doesn't already exists and is not an empty string."""

        tag_text = request.POST.get("tag_text")
        if tag_text and not Tag.objects.filter(name=tag_text).exists():
            new_tag  = Tag.objects.create(name=tag_text)
            response = JsonResponse({"tag_id" : new_tag.id})
            response.status_code = 201
            return response


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Creates a new article category.
    Sufficient privileges for managing articles are required in order to create new categories.
    """

    permission_required = "articles.change_article"

    def post(self, request, *args, **kwargs):
        """A new category will be created if and only if the category doesn't already exists and is not an empty string."""

        category_name = request.POST.get("category_name")
        if category_name and not Category.objects.filter(name=category).exists():
            Category.objects.create(name=request.POST.get("category_name"))

        return HttpResponseRedirect(reverse_lazy("articles:article_list"))


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Deletes an existing category.
    Sufficient privileges for managing articles are required in order to delete categories.
    """

    permission_required = "articles.change_article"

    def post(self, request, *args, **kwargs):
        if Category.objects.filter(id=request.POST.get("category_id")).exists():
            Category.objects.get(id=request.POST.get("category_id")).delete()

        return HttpResponseRedirect(reverse_lazy("articles:article_list"))


class ArticleDetailView(LoginMixinView, DetailView):
    """
    Renders detail view of an article,
    also renders comments under the article
    """
    model = Article
    template_name = "articles_detail.html"

    def get_context_data(self, *args, **kwargs):
        context  = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        article  = Article.objects.get(slug=kwargs['slug'])

        if article.article_state == article.HIDDEN and article.author != self.request.user:
            return False

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

        tmp = self.get_context_data(*args, **kwargs)
        if not tmp:
            return redirect('articles:article_list')
        else:
            return render(request, 'articles_detail.html', tmp)


class PostCommentView(LoginRequiredMixin, View):
    """
    Creates new comment posts and replies via AJAX.
    A rendered comment/reply as HTML will be return to the client.
    User authorization is required.
    """

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
    """
    Handles AJAX requests and returns a filtered list of articles according to a given category as HTML.
    """

    def get(self, request, *args, **kwargs):
        articles = Article.objects.filter(category=request.GET.get('category'))
        for article in articles:
            article.article_tags = Tag.objects.filter(article=article).order_by('name')
        return render(request, 'get_articles.html', {"articles":articles})


class GetAllArticlesView(View):
    """
    Returns a list of all articles as HTML.
    """

    def get(self, request, *args, **kwargs):
        articles = Article.objects.all().order_by('-modified')
        for article in articles:
            article.article_tags = Tag.objects.filter(article=article).order_by('name')
        return render(request, 'get_articles.html', {"articles":articles})


class ArticleSearchView(View):
    """
    Returns a filtered list of articles according to a given set of keywords.
    """

    def get(self, request, *args, **kwargs):
        """An article matches a keyword if the title or its tags contains a given the given keyword"""

        keywords       = request.GET.get('keywords').split()
        tags_query     = reduce(lambda x, y: x | y, [Q(name__icontains=keyword) for keyword in keywords])
        articles_query = reduce(lambda x, y: x | y, [Q(title__icontains=keyword) for keyword in keywords])
        tags           = Tag.objects.filter(tags_query)
        articles       = Article.objects.filter(Q(tags__in=tags) | Q(articles_query)).distinct().order_by('-modified')
        for article in articles:
            article.article_tags = Tag.objects.filter(article=article).order_by('name')
        return render(request, 'get_articles.html', {"articles":articles})


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Deletes an existing article.
    Sufficient privileges for managing articles are required in order to delete articles.
    """

    permission_required = "articles.change_article"

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(id=int(request.POST.get('article_id')))
        if article:
            article.delete()
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=401)


class HideArticleView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Marks an article as hidden which prevents the article being rendered for ordinary users.
    Sufficient privileges for managing articles are required in order to hide articles.
    """

    permission_required = "articles.change_article"

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(id=int(request.POST.get('article_id')))
        if article:
            article.article_state = 0
            article.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)


class PublishArticleView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Marks an article as published which makes the article public.
    Sufficient privileges for managing articles are required in order to publish articles.
    """

    permission_required = "articles.change_article"

    def post(self, request, *args, **kwargs):
        article = Article.objects.get(id=int(request.POST.get('article_id')))
        if article:
            article.article_state = 1
            article.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)


class BanCommentView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Changes comment status to banned and redirects user back to previous page.
    """

    permission_required = "articles.change_comment"

    def get(self, request, *args, **kwargs):

        comment = Comment.objects.get(pk=kwargs["pk"])

        comment.is_censured = True
        comment.save()

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class UnbanCommentView(LoginMixinView, LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Changes comment status to unbanned and redirects user back to prevous page.
    """

    permission_required = "articles.change_comment"

    def get(self, request, *args, **kwargs):

        comment = Comment.objects.get(pk=kwargs["pk"])

        comment.is_censured = False
        comment.save()

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
