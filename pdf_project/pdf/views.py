from tkinter import Canvas
from django.http import FileResponse
from django.shortcuts import redirect, render
from io import BytesIO
from reportlab.pdfgen import canvas

from .form import BookForm
from .models import Book

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    else:
        form = BookForm()
    return render(request, 'home.html', {'form':form})


def generate_pdf(request):
    response = FileResponse(generate_pdf_file(), as_attachment=True, filename='book_details.pdf')
    return response


def generate_pdf_file():
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    books= Book.objects.all()
    c.drawString(100,750, "Book Details")

    y=700
    for book in books:
        c.drawString(100, y, f"Title: {book.title}")
        c.drawString(100, y - 20, f"Author: {book.author}")
        c.drawString(100, y - 40, f"Year: {book.publication_year}")
        y -= 60

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer