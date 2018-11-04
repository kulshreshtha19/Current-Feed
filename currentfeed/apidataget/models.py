from django.db import models
from django.contrib.auth.models import User

class Save(models.Model):
    article_title=models.CharField(max_length=1000,unique=True)
    article_image=models.CharField(max_length=5000)
    article_description=models.CharField(max_length=5000)
    article_url=models.CharField(max_length=5000)
    article_time=models.CharField(max_length=5000)
    sid=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.article_title
    


