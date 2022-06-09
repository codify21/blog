from django.core import validators
from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def full_name(self):
        return f"{self.caption}"


    def __str__(self):
        return self.full_name()

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


    def __str__(self):
        return self.full_name()

class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200)
    # image = models.CharField(max_length=200))
    image = models.ImageField(upload_to="posts",null=True)#name of folder inside uploads
    date = models.DateField(auto_now=True)
    slug = models.SlugField(max_length=200)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=SET_NULL ,null=True, related_name= "posts")
    tags = models.ManyToManyField(Tag)

    def __str__(self):
            return self.title


class Comment(models.Model):
    user_name = models.CharField(max_length=20)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")

       

