from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from apps.projects.models import Project
from apps.projects.filters import ProjectValueFilter, ProjectDurationFilter


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'project_name_display',
        'project_value_display', 
        'start_date_display',
        'end_date_display',
        'status_display',
        'duration_display'
    ]
    list_filter = ['status',  'end_date']
    search_fields = ['project_name']
    date_hierarchy = 'start_date'
    list_per_page = 20
    actions = ['mark_as_ongoing', 'mark_as_completed', 'mark_as_cancelled']
    
    fieldsets = (
        ('📋 Informasi Proyek', {
            'fields': ('project_name', 'project_value'),
            'classes': ('wide',)
        }),
        ('📅 Jadwal', {
            'fields': ('start_date', 'end_date', 'status'),
            'classes': ('wide',)
        }),
    )

    def project_name_display(self, obj):
        return format_html(
            '<div style="font-weight: 600; color: #2c3e50; font-size: 16px;">'
            '<span style="margin-right: 8px;">📁</span>{}'
            '</div>',
            obj.project_name
        )
    project_name_display.short_description = 'Nama Proyek'
    project_name_display.admin_order_field = 'project_name'

    def project_value_display(self, obj):
        value = obj.project_value
        # Format currency with separator
        formatted_value = f"Rp {value:,.2f}".replace(',', '.')
        
        # Color based on value
        if value >= 10000000000:  # >= 10 Milyar
            color = '#28a745'
        elif value >= 1000000000:  # >= 1 Milyar
            color = '#17a2b8'
         
        else:
            color = '#6c757d'
    
        
        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<span style="font-weight: 600; color: {}; font-size: 14px;">{}</span>'
            '</div>',
            color, formatted_value
        )
    project_value_display.short_description = 'Nilai Proyek'
    project_value_display.admin_order_field = 'project_value'

    def start_date_display(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; gap: 6px;">'
            '<span style="color: #2c3e50; font-weight: 500;">{}</span>'
            '</div>',
            obj.start_date.strftime('%d %b %Y')
        )
    start_date_display.short_description = 'Tanggal Mulai'
    start_date_display.admin_order_field = 'start_date'

    def end_date_display(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; gap: 6px;">'
            '<span style="color: #2c3e50; font-weight: 500;">{}</span>'
            '</div>',
            obj.end_date.strftime('%d %b %Y')
        )
    end_date_display.short_description = 'Tanggal Selesai'
    end_date_display.admin_order_field = 'end_date'

    def status_display(self, obj):
        status_config = {
            'planning': {
                'label': 'Planning',
                'color': '#ffc107',
                'bg_color': '#fff3cd',
                'icon': '📝',
                'border': '#ffc107'
            },
            'ongoing': {
                'label': 'Ongoing',
                'color': '#17a2b8',
                'bg_color': '#d1ecf1',
                'icon': '🚀',
                'border': '#17a2b8'
            },
            'completed': {
                'label': 'Completed',
                'color': '#28a745',
                'bg_color': '#d4edda',
                'icon': '✅',
                'border': '#28a745'
            },
            'cancelled': {
                'label': 'Cancelled',
                'color': '#dc3545',
                'bg_color': '#f8d7da',
                'icon': '❌',
                'border': '#dc3545'
            },
        }
        
        config = status_config.get(obj.status, status_config['planning'])
        
        return format_html(
            '<div style="display: inline-flex; align-items: center; gap: 8px; '
            'padding: 8px 16px; border-radius: 20px; '
            'background: {}; border: 2px solid {}; '
            'font-weight: 600; font-size: 13px; color: {};">'
            '<span style="font-size: 16px;">{}</span>'
            '<span>{}</span>'
            '</div>',
            config['bg_color'],
            config['border'],
            config['color'],
            config['icon'],
            config['label']
        )
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'

    def duration_display(self, obj):
        duration = (obj.end_date - obj.start_date).days
        
        if duration >= 365:
            years = duration // 365
            months = (duration % 365) // 30
            duration_text = f"{years} tahun"
            if months > 0:
                duration_text += f" {months} bulan"
            color = '#6f42c1'
            icon = '📅'
        elif duration >= 30:
            months = duration // 30
            duration_text = f"{months} bulan"
            color = '#fd7e14'
            icon = '📆'
        else:
            duration_text = f"{duration} hari"
            color = '#20c997'
            icon = '⏱️'
        
        return format_html(
            '<div style="display: flex; align-items: center; gap: 6px; '
            'padding: 6px 12px; border-radius: 12px; '
            'background: {}20; border: 1px solid {}; display: inline-flex;">'
            '<span style="font-size: 14px;">{}</span>'
            '<span style="color: {}; font-weight: 600; font-size: 13px;">{}</span>'
            '</div>',
            color, color, icon, color, duration_text
        )
    duration_display.short_description = 'Durasi'

    class Media:
        css = {
            'all': []
        }
        js = []

    # Admin Actions
    def mark_as_ongoing(self, request, queryset):
        updated = queryset.update(status='ongoing')
        self.message_user(
            request, 
            f'{updated} proyek berhasil diubah menjadi Ongoing.', 
            messages.SUCCESS
        )
    mark_as_ongoing.short_description = '🚀 Tandai sebagai Ongoing'

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(
            request, 
            f'{updated} proyek berhasil diubah menjadi Completed.', 
            messages.SUCCESS
        )
    mark_as_completed.short_description = '✅ Tandai sebagai Completed'

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(
            request, 
            f'{updated} proyek berhasil diubah menjadi Cancelled.', 
            messages.WARNING
        )
    mark_as_cancelled.short_description = '❌ Tandai sebagai Cancelled'

    def changelist_view(self, request, extra_context=None):
        # Add summary statistics
        extra_context = extra_context or {}
        
        # Calculate statistics
        total_projects = Project.objects.count()
        total_value = Project.objects.aggregate(Sum('project_value'))['project_value__sum'] or 0
        
        status_counts = {}
        for status_code, status_label in Project.STATUS:
            status_counts[status_code] = Project.objects.filter(status=status_code).count()
        
        extra_context['total_projects'] = total_projects
        extra_context['total_value'] = total_value
        extra_context['status_counts'] = status_counts
        
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Project, ProjectAdmin)

# Customize admin site header
admin.site.site_header = "Project Management System"
admin.site.site_title = "Project Management"
admin.site.index_title = "Dashboard"
