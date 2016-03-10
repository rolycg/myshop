from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    url(r'^search/?$', views.search, name='search'),
    url(r'^login/?$', views.login, name='login'),
    url(r'^signup/?$', views.signup, name='signup'),
    url(r'^all/?$', views.all_products, name='all_products'),
    url(r'^set_language/?$', views.set_language, name='set_language'),
    url(r'^$', views.product_list, name='product_list')
]
