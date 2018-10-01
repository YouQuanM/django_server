# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Poker_cards(models.Model):
    poker_username = models.CharField(max_length=64)
    poker_card_color = models.IntegerField()
    poker_card_num = models.IntegerField()

    def __unicode__(self):
        return self.poker_card_color,self.poker_card_num,self.poker_username