from django.db import models

# Create your models here.
class Place(models.Model):
     title = models.CharField(max_length=100)

#instead of views a position title in a list
     def __str__(self):
        return self.title

class Employee(models.Model):
    username = models.CharField(max_length=100)
    mobile   = models.CharField(max_length=15,null=True)
    email = models.CharField(max_length=50,null=True)
    Place = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=10)
    
