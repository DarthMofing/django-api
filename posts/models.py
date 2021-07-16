""" Posts Models """

from django.db import models

# Models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


class Post (models.Model):
    """ Data that comes from a post """

    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    likes = models.IntegerField()

    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title

class Author(models.Model):
	""" Model to link an author to its post """
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __str__(self):
		return self.author.username