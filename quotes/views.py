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

from django.contrib import messages
from django.contrib.auth.views import PasswordResetView        # нове
from django.contrib.messages.views import SuccessMessageMixin  # нове
from django.urls import reverse_lazy                           # нове


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
            # Отримуємо ім'я автора зі строкового поля форми
            author_name = form.cleaned_data['author']
            
            # Шукаємо реальний об'єкт автора в базі MongoDB за ім'ям
            author_obj = Author.objects(fullname=author_name).first()
            
            if not author_obj:
                messages.error(request, "Selected author does not exist!")
                return render(request, 'quotes/add_quote.html', {'form': form})

            # Конвертуємо рядок тегів у список
            raw_tags = form.cleaned_data.get('tags', '')
            tags_list = [tag.strip() for tag in raw_tags.split(',') if tag.strip()]

            # Створюємо цитату, передаючи саме об'єкт author_obj
            Quote(
                quote=form.cleaned_data['quote'],
                author=author_obj, 
                tags=tags_list
            ).save()
            
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
    try:
        quotes = Quote.objects.all()
        # Пробуємо отримати кількість, щоб перевірити чи немає битих посилань
        count = quotes.count()
        print(f"DEBUG: Знайдено цитат: {count}")
    except Exception as e:
        print(f"DEBUG: Помилка dereference в цитатах: {e}")
        # Якщо є биті цитати, витягуємо тільки ті, які не ламаються, або обнуляємо
        quotes = []

    return render(request, 'quotes/index.html', {'quotes': quotes})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'quotes/password_reset.html'
    email_template_name = 'quotes/password_reset_email.html'
    html_email_template_name = 'quotes/password_reset_email.html'
    subject_template_name = 'quotes/password_reset_subject.txt'
    success_url = reverse_lazy('quotes:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."