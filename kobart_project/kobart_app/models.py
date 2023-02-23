from django.db import models

# Create your models here.

class database(models.Model):
    before_text = models.CharField(max_length=300)
    after_text = models.CharField(max_length=300)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.before_text
    