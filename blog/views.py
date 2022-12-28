from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Review
from .forms import ArticleForm, ArticleSearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, F, Sum, Avg, Min, Max
from django.core.paginator import Paginator
from urllib.parse import urlencode

# Create your views here.
def blog_list(request):
    
    articles = Article.objects.exclude(visible=False)
    title_search = request.GET.get('title')
    author_id = request.GET.get('author')
    if title_search:
        articles = articles.filter(title__icontains=title_search)
    elif author_id:
        articles = articles.filter(author=author_id)

    search_form = ArticleSearchForm()
    
    authors = User.objects.filter(is_staff=False).annotate(article_count=Count('article')).order_by('-article_count')[:5]
    total_article_count = articles.count()
    # total_view_count = articles.aggregate(total_view=Sum('view_count'))['total_view']
    article_statistic = articles.aggregate(
        total_view=Sum('view_count'),
        avg_view=Avg('view_count'),
        min_view=Min('view_count'),
        max_view=Max('view_count'),
    )
    
    less_view_article = articles.filter(view_count=article_statistic['min_view']).order_by('-created').first()
    max_view_article = articles.filter(view_count=article_statistic['max_view']).order_by('-created').first()
    
    paginator = Paginator(articles, 2)
    requested_page = request.GET.get('page')
    page = paginator.page(int(requested_page) if requested_page else 1)
    articles = page.object_list
    
    context={
        'articles': articles,
        'page': page,
        'paginator': paginator,
        'search_form': search_form,
        'authors': authors,
        'total_article_count': total_article_count,
        # 'total_view_count': total_view_count,
        'article_statistic': article_statistic,
        'less_view_article': less_view_article,
        'max_view_article': max_view_article,
    }
    return render(request, 'blog.html', context=context)

def blog_detail(request, id):
    article = Article.objects.get(id=id)
    article.view_count = F('view_count') + 1
    article.save()
    article.refresh_from_db()
    other_articles = article.author.article_set.exclude(id=article.id)
    return render(request, 'article.html', context={'article': article, 'other_articles': other_articles})

@login_required(login_url='user:login')
def add_article(request):
    form = ArticleForm()
    return render(request, 'add-article.html', context={'form': form})

def confirm_add_article(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog:add-article')
        else:
            return render(request, 'add-article.html', context={'form': form})
    else:
        return redirect('blog:add-article')
    
    
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(instance=article)
    return render(request, 'edit-article.html', context={'form': form, 'pk': article.pk})

def confirm_edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('blog:edit-article', pk=pk)
        else:
            return render(request, 'edit-article.html', context={'form': form, 'pk': article.pk})
    else:
        return redirect('blog:edit-article', pk=pk)
    
def confirm_delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('blog:blog-list')


def review(request, pk, star_count):
    article = get_object_or_404(Article, pk=pk)
    Review.objects.create(article=article, star_count=star_count)
    return redirect('blog:blog-detail', id=pk)