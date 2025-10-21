from django.shortcuts import render, redirect
from .forms import ContactForm, BookForm, DocumentForm
from .models import Book
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def contact_view(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data['name'])
        print(form.cleaned_data['email'])
        print(form.cleaned_data['message'])
        messages.success(request, '연락처 정보 전송 완료!')
        return redirect('main:contact')
    return render(request, 'contact.html', {'form': form})

def create_book_view(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, '도서 정보 등록 완료!')
        return redirect('main:book')
    return render(request, 'book_form.html', {'form': form})

def upload_view(request):
    form = DocumentForm(request.POST or None, request.FILES or None)
    # print(request.POST)
    # print(request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, '파일 업로드 완료!')
        return redirect('main:upload')
    return render(request, 'upload.html', {'form': form})

class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('main:book_list')

# BookUpdateView 작성

# BookDeleteView 작성
