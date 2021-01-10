from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time
from django.utils import timezone
from django.contrib.auth.models import User


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Post(models.Model):
    
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post-update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post-delete', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_pub']


class Tag(models.Model):
    
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})
    
    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']

# class Comment(models.Model):
#     content = models.TextField(max_length=150)
#     date_posted = models.DateTimeField(default=timezone.now)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     post_connected = models.ForeignKey(Post, on_delete=models.CASCADE)


# class Preference(models.Model):
#     user= models.ForeignKey(User, on_delete=models.CASCADE)
#     post= models.ForeignKey(Post, on_delete=models.CASCADE)
#     value= models.IntegerField()
#     date= models.DateTimeField(auto_now= True)

#     def __str__(self):
#         return str(self.user) + ':' + str(self.post) +':' + str(self.value)

#     class Meta:
#        unique_together = ("user", "post", "value")