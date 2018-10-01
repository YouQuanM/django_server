# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

from django.shortcuts import render

# Create your views here.
from poker.models import Poker_cards


def add_player(request):
    username = request.GET.get('username')
    for i in 3:
        cardcolor = random.randint(0,3)
        cardnum = random.randint(2,14)
        haspoker = Poker_cards.objects.filter(poker_card_color=cardcolor,poker_card_num=cardnum)
        print(haspoker)



