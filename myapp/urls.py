from django.conf.urls import url, include
import views

urlpatterns = [
    url(r'add_book$', views.add_book, ),
    url(r'show_books$', views.show_books, ),
    url(r'delete_book$', views.delete_book, ),
    url(r'show_articles$', views.show_articles, ),
    url(r'add_article$', views.add_article, ),
    url(r'delete_article$', views.delete_article, ),
    url(r'log_up$', views.log_up, ),
    url(r'log_in$', views.log_in, ),
    url(r'log_out$', views.log_out, ),
    url(r'add_comment$', views.add_comment, ),
    url(r'show_comment$', views.show_comment, ),
    url(r'add_praise$', views.add_praise, ),
    url(r'change_password$', views.change_password, ),
]

