from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.contrib.admin import display
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='Başlıq')
    description = models.TextField(null=True, blank=True, verbose_name='Açıqlama')
    content = models.TextField(verbose_name='Kontent')
    cover = models.ImageField(null=True, blank=True, verbose_name='Qapaq Şəkli')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Müəllif')
    view_count = models.BigIntegerField(default=0)
    visible = models.BooleanField(default=True)
    updated = models.DateField(auto_now=True, verbose_name='Dəyişdirilmə Tarixi')
    created = models.DateField(auto_now_add=True, verbose_name='Yaradılma Tarixi')
    
    def avg_stars(self):
        # reviews =  self.review_set.all()
        reviews = self.review_list.all()
        if reviews.exists():
            return reviews.aggregate(avg_stars=Avg('star_count')).get('avg_stars')
        else:
            return 0
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:blog-detail', kwargs={'id': self.id})
    
    @display(description='Movcud Qapa Sekli')
    def cover_image_tag(self):
        return format_html(f'<img width="200" src="{self.cover.url}">')
    
    class Meta:
        verbose_name = 'Məqalə'
        verbose_name_plural = 'Məqalələr'
        
        
class Review(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='review_list')
    star_count = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    
    def __str__(self):
        return f'{self.article.title} - {self.star_count}'
    

class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article-images/')
    
    @display(description='Movcud Sekil')
    def image_tag(self):
        return format_html(f'<img width="200" src="{self.image.url}">')
    
    
    
"""
CREATE TABLE blog_author (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
)

CREATE TABLE blog_article (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    blog_author_id INT,
    updated DATE NOT NULL,
    created DATE NOT NULL,
    ADD CONSTRAINT fk_blog_author_id
        FOREIGN KEY (blog_author_id)
        REFERENCES blog_author(id)
        ON DELETE SET NULL
)
"""