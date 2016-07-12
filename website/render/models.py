from django.db import models


class Imported(models.Model):
    imported_text = models.CharField(max_length=10000)
    pub_date = models.DateTimeField('date published')


class Rendered(models.Model):
    imported_text = models.ForeignKey(Imported, on_delete=models.CASCADE)
    rendered_text = models.CharField(max_length=10000)
    templates_used = models.CharField(max_length=500)


class Templates(models.Model):
    template_name = models.CharField(max_length=100)
    template_body = models.CharField(max_length=10000)
