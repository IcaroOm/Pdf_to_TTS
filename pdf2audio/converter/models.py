from django.db import models

class PDFFile(models.Model):
    file = models.FileField(upload_to='pdf_files/')
    created_at = models.DateTimeField(auto_now_add=True)
