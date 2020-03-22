from django.db import models
from datetime import datetime

# Create your models here.
class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    tutorial_summary = models.TextField()
    tutorial_content = models.TextField()
    tutorial_category= models.CharField(max_length=200)
    tutorial_published = models.DateTimeField(
        "date published", default=datetime.now())

    def __str__(self):
        return self.tutorial_title
