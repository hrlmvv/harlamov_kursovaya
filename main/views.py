from django.shortcuts import render, redirect
from .models import News, Article
from django.core.paginator import Paginator
from django.views.generic import DetailView
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ArticleForm, NewsForm
from django.contrib import messages
from django.db.models.functions import Lower


# Create your views here.

def index(request):
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:6]
    latest_articles = Article.objects.filter(is_published=True).order_by('-created_at')[:3]
    context = {
        'latest_news': latest_news,
        'latest_articles': latest_articles
    }
    return render(request, 'main/index.html', context)

@login_required
def edit_profile(request):
    profile = request.user.profile  

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'main/edit_profile.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.profile  
    return render(request, 'main/profile.html', {'profile': profile})

def about(request):
    return render(request, 'main/about.html')

def news(request):
    news_list = News.objects.filter(is_published=True).order_by('-created_at') 
    paginator = Paginator(news_list, 5) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'main/news.html', {'page_obj': page_obj})

def articles(request):
    articles = Article.objects.filter(is_published=True).order_by('-created_at') 
    paginator = Paginator(articles, 5)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/articles.html', {'page_obj': page_obj})

def search_results(request):
    query = request.GET.get('q')
    search_type = request.GET.get('search', 'any')
    sort_order = request.GET.get('sort', 'relevance')

    search_executed = False
    
    results = []
    
    if query and query.strip():
        search_executed = True
        query = query.lower().strip()
        words = query.split()

        all_articles = list(Article.objects.filter(is_published=True))
        all_news = list(News.objects.filter(is_published=True))

        def filter_content(item):
            title_contains = lambda word: word in item.title.lower()
            content_contains = lambda word: word in item.content.lower()
            precontent_contains = lambda word: word in item.precontent.lower()

            if search_type == 'phrase':
                return query in item.title.lower() or query in item.content.lower() or query in item.precontent.lower()
            elif search_type == 'all':
                return all(title_contains(word) or content_contains(word) or precontent_contains(word) for word in words)
            else:
                return any(title_contains(word) or content_contains(word) or precontent_contains(word) for word in words)

        filtered_articles = filter(filter_content, all_articles)
        filtered_news = filter(filter_content, all_news)

        results = list(filtered_articles) + list(filtered_news)
        
        if sort_order == 'date_asc':
            results.sort(key=lambda x: x.created_at)
        elif sort_order == 'date_desc':
            results.sort(key=lambda x: x.created_at, reverse=True)

        paginator = Paginator(results, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'main/search.html', {'page_obj': page_obj, 'query': query, 'search_executed': search_executed})
    else:
        return render(request, 'main/search.html', {'page_obj': None, 'query': query, 'search_executed': search_executed})

def article(request):
    return render(request, 'main/article.html')

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, author=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ArticleForm()
    return render(request, 'main/article_form.html', {'form': form})

def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, author=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = NewsForm()
    return render(request, 'main/news_form.html', {'form': form})


class NewsDetailView(DetailView):
    model = News
    template_name = 'main/news_detail.html'
    context_object_name = 'news'

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'main/article_detail.html'
    context_object_name = 'article'

class CustomLoginView(LoginView):
    template_name = 'main/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Неверный логин или пароль.")
        return super().form_invalid(form)