from django.db import models
from django.contrib.auth.models import User

class Save(models.Model):
    saved=models.CharField(max_length=1000)
    sid=models.ForeignKey(User,on_delete=models.CASCADE)
    


