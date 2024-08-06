from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.

class PublishedStateOptions(models.TextChoices):
        PUBLISH = 'PU','Publish'
        DRAFT   = 'DR','DRAFT'