from django.db import models
from django.contrib.auth.models import User


# Create your models here.
#movie --- Guest --- Reversition

class Movie(models.Model):
    movie = models.CharField(max_length=10)
    hall = models.CharField(max_length=10)
    date = models.DateField( auto_now_add=True)

    def __str__(self):
        return self.movie


class Guest(models.Model):
    name = models.CharField(max_length=15 )
    mobile = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name



class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    discreption = models.TextField()

    def __str__(self):
        return self.title



class Reversition(models.Model):
    guest = models.ForeignKey(Guest, related_name='reversition', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='reversition', on_delete=models.CASCADE)
    
    def __str__(self):
        return  self.movie.movie


