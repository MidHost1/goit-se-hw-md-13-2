from django.shortcuts import render
from .models import Quote
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from quotes.documents import Quote, Author
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
from django.http import Http404
from mongoengine.errors import NotUniqueError


from mongoengine.errors import NotUniqueError
from django.contrib import messages # Імпортуй це!

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            try:
                Author(
                    fullname=form.cleaned_data['fullname'],
                    born_date=form.cleaned_data['born_date'],
                    born_location=form.cleaned_data['born_location'],
                    description=form.cleaned_data['description']
                ).save()
                return redirect('quotes:index')
            except NotUniqueError:
                messages.error(request, "Author with this name already exists!")
                return render(request, 'quotes/add_author.html', {'form': form})
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:index')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

def author_detail(request, name):
    try:
        author = Author.objects.get(fullname=name)
    except Author.DoesNotExist:
        raise Http404("Author not found")
    return render(request, 'quotes/author_detail.html', {'author': author})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quotes:index')
    else:
        form = RegisterForm()
    return render(request, 'quotes/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('quotes:index')
    else:
        form = AuthenticationForm()
    return render(request, 'quotes/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('quotes:index')

def quote_list(request):
    quotes = Quote.objects.all()
    try:
        count = quotes.count()
        print(f"DEBUG: Знайдено цитат: {count}")
    except Exception as e:
        print(f"DEBUG: Помилка підключення до БД: {e}")
        count = 0

    return render(request, 'quotes/index.html', {'quotes': quotes})