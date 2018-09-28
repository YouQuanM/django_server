# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Book(models.Model):
    book_name = models.CharField(max_length=64)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.book_name

class Article(models.Model):
    article_title = models.CharField(max_length=64)
    article_body = models.TextField(max_length=256)
    add_time = models.DateTimeField(auto_now_add=True)
    article_praise = models.IntegerField()
    article_user = models.CharField(max_length=64,default="")

    def __unicode__(self):
        return self.article_title,self.article_body,self.article_praise,self.article_user