from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.conf import settings

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
        )  # Changed to use custom user model
    job_title = models.CharField(max_length=200, blank=True)
    thumbnail = models.ImageField(
        upload_to='thumbnails/', 
        blank=True, 
        null=True
        )  # New field for thumbnail
    
    video = models.FileField(
        upload_to='videos/', 
        blank=True, 
        null=True
        )  # New field for video
    content = models.TextField()
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='draft'
        )
    publish_date = models.DateTimeField(auto_now_add=True)
    on_delete=models.CASCADE
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Like',
        related_name='liked_posts',
        blank=True,
    )
    likes_count = models.IntegerField(default=0)    
    

    def save(
            self, 
            force_insert=False, 
            force_update=False, 
            using=None, 
            update_fields=None
            ):
        self.slug = slugify(self.title)
        if update_fields is not None and "title" in update_fields:
            update_fields = {"slug"}.union(update_fields)
        super().save(
            force_insert=force_insert, 
            force_update=force_update, 
            using=using, 
            update_fields=update_fields
            )

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        related_name='comments', 
        on_delete=models.CASCADE
        )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
        )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"
    
class Like(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"Like by {self.user} on {self.post.title}"

    

