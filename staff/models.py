from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Type(models.Model):
    Name = models.CharField(max_length=30)
    Description = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.Name
class Faculty(models.Model):
    Name = models.CharField(max_length=30)
    Description = models.CharField(max_length=200)
    def __str__(self):
        return self.Name
class User(AbstractUser):
    code = models.CharField(max_length=12, null = True, blank = True)
    Faculty = models.ForeignKey(Faculty, default=None, on_delete=models.CASCADE, blank=True, null = True)
class Term(models.Model):
    Name = models.CharField(max_length=100, null=True, blank=True)
    Description = models.CharField(max_length=200, null=True, blank=True)
    Closure_date = models.DateTimeField()
    Final_Closure_date = models.DateTimeField()
    def __int__(self):
        return self.id

class Contribution(models.Model):
    UserID = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    TermID = models.ForeignKey(Term, default=None, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Description = models.CharField(max_length=200, null=True, blank=True)
    Total_likes = models.IntegerField(blank=True)
    Incognito = models.BooleanField()
    Create_at = models.DateTimeField(auto_now_add=True)
    TypeID = models.ForeignKey(Type, default=None, on_delete=models.CASCADE, blank=True, null = True)
    def __str__(self):
        return self.Name

class Document(models.Model):
    ContributeID = models.ForeignKey(Contribution, default=None, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Description = models.CharField(max_length=200, null=True, blank=True)
    Document_detail = models.FileField()
    def __str__(self):
        return self.Name

class Like(models.Model):
    User_ID1 = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='user1')
    ContributeID = models.ForeignKey(Contribution, default=None, on_delete=models.CASCADE)
    Like = models.BooleanField()


class Comment(models.Model):
    UserID = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    ContributeID = models.ForeignKey(Contribution, default=None, on_delete=models.CASCADE)
    Comment = models.TextField()
    Incognito = models.BooleanField()
    Create_at = models.DateTimeField(auto_now_add=True)

