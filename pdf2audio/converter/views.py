import os
import tempfile
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from PyPDF2 import PdfFileReader
import pyttsx3

from .models import PDFFile

def home(request):
    if request.method == 'POST':
        pdf_file = request.FILES['pdf_file']
        pdf = PDFFile.objects.create(file=pdf_file)
        return redirect('pdf_detail', pk=pdf.pk)
    return render(request, 'home.html')

def pdf_detail(request, pk):
    pdf = PDFFile.objects.get(pk=pk)
    text = extract_text(pdf.file.path)
    audio_path = convert_to_audio(text)
    return render(request, 'pdf_detail.html', {'pdf': pdf, 'audio_path': audio_path})

def download_audio(request, pk):
    pdf = get_object_or_404(PDFFile, pk=pk)
    audio_path = request.GET.get('audio_path', None)
    if audio_path is None:
        raise Http404("Audio file does not exist")
    audio_file = os.path.join(settings.AUDIO_OUTPUT_DIR, audio_path)
    if not os.path.exists(audio_file):
        raise Http404("Audio file does not exist")
    with open(audio_file, 'rb') as f:
        response = HttpResponse(f.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = f'attachment; filename="{pdf.file.name}.mp3"'
        return response

def extract_text(filepath):
    with open(filepath, 'rb') as f:
        pdf = PdfFileReader(f)
        text = ''
        for page_num in range(pdf.getNumPages()):
            text += pdf.getPage(page_num).extractText() + '\n'
        return text

def convert_to_audio(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    audio_path = os.path.join(settings.AUDIO_OUTPUT_DIR, 'output.mp3')
    engine.save_to_file(text, audio_path)
    engine.runAndWait()
    return audio_path
