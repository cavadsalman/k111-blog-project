from django.contrib import admin
from .models import Article, ArticleImage, Review
# Register your models here.
admin.site.register(Review)

class ArticleImageInline(admin.TabularInline):
    fields = ['image', 'image_tag', ]
    readonly_fields = ['image_tag']
    model = ArticleImage
    extra = 1
    
@admin.action(description='Görünən Et')
def make_visible(modeladmin, request, queryset):
    queryset.update(visible=True)
    
@admin.action(description='Gizli Et')
def make_unvisible(modeladmin, request, queryset):
    queryset.update(visible=False)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # fields = ['title', 'description', 'content', 'cover', 'author', 'created']
    # exclude = ['updated']
    fieldsets = [
        ('Melumat ve Kontent', {
            'fields': ['title', 'description', 'content'],
            'classes': ['collapse']
        }),
        (None, {
            'fields': ['cover_image_tag', 'cover', 'author', 'view_count', 'visible', ('created', 'updated')]
        })
    ]
    readonly_fields = ['created', 'updated', 'cover_image_tag', 'view_count']
    inlines = [ArticleImageInline]

    list_display = ['title', 'author', 'visible', 'view_count', 'avg_stars',  'created']
    # list_editable = ['description']
    list_display_links = ['title', 'created']
    list_filter = ['author', 'created']
    search_fields = ['title', 'description', 'content']
    actions = [make_visible, make_unvisible]