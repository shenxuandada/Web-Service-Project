# from django.contrib import admin
# from .models import Post

# admin.site.register(Post)
# # Register your models here.


from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 在列表页面中显示的字段
    list_display = ('title', 'author', 'published_date')  # 移除 'category_counts'

    # 可供搜索的字段
    search_fields = ('title', 'text')

    # 可过滤的字段
    list_filter = ('author', 'created_date', 'published_date')

    # 配置字段的显示顺序
    fieldsets = (
        ('基本信息', {
            'fields': ('author', 'title', 'text', 'image')
        }),
        ('时间信息', {
            'fields': ('created_date', 'published_date')
        }),
    )
