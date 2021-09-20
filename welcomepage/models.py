from django.db import models
import string
import random

# Create your models here.
class Document(models.Model):
	doc_id = models.CharField(max_length=64, unique=True)
	title = models.CharField(max_length=255)
	content = models.TextField()
	colabs = models.TextField(default=0)