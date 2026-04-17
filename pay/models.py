from django.db import models

# Create your models here.
class Pay (models.Model):
    methods=models.CharField(max_length=100)
    check=models.CharField(max_length=100)