from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView
from django.urls import reverse_lazy


from .models import *
from .forms import ArticleForm, CommentForm, UserLogin, UserRegister


# def index(request):
#     articles = Article.objects.all()
#     context = {
#         'title': 'Birinchi sayt',
#         'articles': articles
#     }
#
#     return render(request, 'blog/index.html', context)

class ArticleList(ListView):  # article_list.html
    model = Article  # Article.objects.all() -> object
    context_object_name = 'articles'
    template_name = 'blog/index.html'
    extra_context = {
        'title': 'Влог'
    }



# def articles_by_category(request, category_id):
#
#     category = Category.objects.get(id=category_id)
#     # articles = Article.objects.filter(category__id=category_id)
#     articles = Article.objects.filter(category=category)
#     context = {
#         'title': category.title,
#         'articles': articles
#     }
#     return render(request, 'blog/index.html', context)

class ArticlesByCategory(ArticleList):
    def get_queryset(self):
        return Article.objects.filter(category__id=self.kwargs['category_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = f"{Category.objects.get(id=self.kwargs['category_id']).title}: Yangiliklar"
        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        context['title'] = article.title
        context['comments'] = Comment.objects.filter(article=article)
        context['comment_form'] = CommentForm()
        return context




def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    context = {
        'article': article,
        'title': article.title[:20]
    }
    return render(request, 'blog/article_detail.html', context)


class AddArticle(CreateView):
    model = Article
    template_name = 'blog/add_article.html'
    form_class = ArticleForm



def profile(request):
    context = {
        'title': "Провиль"
    }
    return render(request, 'blog/profile.html', context)

def user_login(request):
    if request.method == "POST":
        form = UserLogin(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserLogin()

    context = {
        'form': form,
        'title': 'Вход'
    }
    return render(request, 'blog/login_form.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = UserRegister(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('index')
    else:
        form = UserRegister()

    context = {
        'title': "Присоединиться",
        'form': form
    }
    return render(request, 'blog/register.html', context)


def save_comment(request, article_id):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            article = Article.objects.get(pk=article_id)
            comment.article = article
            comment.save()
        else:
            pass
        return redirect('artocle_detail', article_id)


class EditArticle(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/add_article.html'

class DeleteArticle(DeleteView):
    model = Article
    success_url = reverse_lazy('index')
    context_object_name = 'article'
