"""
Кастомная админка Django с расширенным функционалом
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta


class CustomAdminSite(AdminSite):
    """
    Кастомный AdminSite с улучшенным дизайном и функционалом
    """
    site_header = _('Панель администратора')
    site_title = _('Админ-панель')
    index_title = _('Добро пожаловать в панель управления')
    
    def each_context(self, request):
        """
        Добавляем кастомные переменные в контекст
        """
        context = super().each_context(request)
        context['custom_admin'] = True
        
        # Статистика для главной страницы
        if request.path == '/admin/' or request.path == '/admin':
            context['stats'] = self.get_stats()
        
        return context
    
    def get_stats(self):
        """
        Получаем статистику для главной страницы
        """
        stats = {}
        
        # Статистика пользователей
        try:
            from users.models import User as CustomUser
            stats['total_users'] = CustomUser.objects.count()
            stats['active_users'] = CustomUser.objects.filter(is_active=True).count()
            stats['staff_users'] = CustomUser.objects.filter(is_staff=True).count()
            stats['new_users_today'] = CustomUser.objects.filter(
                date_joined__gte=timezone.now() - timedelta(days=1)
            ).count()
        except:
            try:
                stats['total_users'] = User.objects.count()
                stats['active_users'] = User.objects.filter(is_active=True).count()
                stats['staff_users'] = User.objects.filter(is_staff=True).count()
                stats['new_users_today'] = User.objects.filter(
                    date_joined__gte=timezone.now() - timedelta(days=1)
                ).count()
            except:
                pass
        
        return stats
    
    def get_urls(self):
        """
        Добавляем кастомные URL
        """
        urls = super().get_urls()
        custom_urls = [
            path('stats/', self.admin_view(self.stats_view), name='admin_stats'),
        ]
        return custom_urls + urls
    
    def stats_view(self, request):
        """
        Представление для статистики
        """
        context = {
            **self.each_context(request),
            'title': 'Статистика',
        }
        return render(request, 'admin/stats.html', context)


# Создаем экземпляр кастомной админки
custom_admin_site = CustomAdminSite(name='custom_admin')

# Регистрируем стандартные модели с улучшениями
try:
    from users.models import User as CustomUser
    
    @admin.register(CustomUser, site=custom_admin_site)
    class CustomUserAdmin(admin.ModelAdmin):
        list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
        list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined')
        search_fields = ('email', 'first_name', 'last_name')
        ordering = ('-date_joined',)
        date_hierarchy = 'date_joined'
        
        fieldsets = (
            (None, {'fields': ('email', 'password')}),
            ('Персональная информация', {'fields': ('first_name', 'last_name', 'phone', 'telegram_chat_id')}),
            ('Права доступа', {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }),
            ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        )
except:
    @admin.register(User, site=custom_admin_site)
    class CustomUserAdmin(admin.ModelAdmin):
        list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
        list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined')
        search_fields = ('username', 'email', 'first_name', 'last_name')
        ordering = ('-date_joined',)
        date_hierarchy = 'date_joined'
        
        fieldsets = (
            (None, {'fields': ('username', 'password')}),
            ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
            ('Права доступа', {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }),
            ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        )


@admin.register(Group, site=custom_admin_site)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_user_count')
    search_fields = ('name',)
    
    def get_user_count(self, obj):
        return obj.user_set.count()
    get_user_count.short_description = 'Количество пользователей'
