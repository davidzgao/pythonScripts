from django.db import models
from django import forms
from django.core.urlresolvers import reverse

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length = 150)
    body = models.TextField()
    timestamp = models.DateTimeField()
    category = models.CharField(max_length = 150, blank = True)

    def get_absolute_url(self):
        path = reverse('detail', kwargs={id:self.id})
        return "http://119.254.102.37:8000%s" % path
    class Meta:
        ordering = ('-timestamp',)


class BlogPostForm(forms.ModelForm):
#    title = forms.CharField(max_length = 150)
#    body = forms.CharField( 
#                widget= forms.Textarea(attrs={'rows':3, 'cols': 60})
#           )
#    timestamp = forms.DateTimeField()
     class Meta:
         model = BlogPost
         exclude = ('timestamp',)


