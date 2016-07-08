from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /render/
    url(r'^$', views.index, name='index'),
    # /render/list_inheritance_templates
    url(r'^list_templates/', views.inheritance_templates, name='inheritance_templates'),
    url(r'^render_template/', views.render_template, name='render_template'),

]