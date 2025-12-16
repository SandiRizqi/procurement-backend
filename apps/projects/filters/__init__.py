from django.contrib import admin
from django.db.models import Q


class ProjectValueFilter(admin.SimpleListFilter):
    title = 'Nilai Proyek'
    parameter_name = 'value_range'

    def lookups(self, request, model_admin):
        return (
            ('small', '💳 < 1 Milyar'),
            ('medium', '💵 1-10 Milyar'),
            ('large', '💰 > 10 Milyar'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'small':
            return queryset.filter(project_value__lt=1000000000)
        elif self.value() == 'medium':
            return queryset.filter(
                project_value__gte=1000000000,
                project_value__lt=10000000000
            )
        elif self.value() == 'large':
            return queryset.filter(project_value__gte=10000000000)
        return queryset


class ProjectDurationFilter(admin.SimpleListFilter):
    title = 'Durasi Proyek'
    parameter_name = 'duration'

    def lookups(self, request, model_admin):
        return (
            ('short', '⏱️ < 1 Bulan'),
            ('medium', '📆 1-12 Bulan'),
            ('long', '📅 > 1 Tahun'),
        )

    def queryset(self, request, queryset):
        from datetime import timedelta
        
        if self.value() == 'short':
            projects = []
            for project in queryset:
                if (project.end_date - project.start_date).days < 30:
                    projects.append(project.id)
            return queryset.filter(id__in=projects)
        
        elif self.value() == 'medium':
            projects = []
            for project in queryset:
                duration = (project.end_date - project.start_date).days
                if 30 <= duration < 365:
                    projects.append(project.id)
            return queryset.filter(id__in=projects)
        
        elif self.value() == 'long':
            projects = []
            for project in queryset:
                if (project.end_date - project.start_date).days >= 365:
                    projects.append(project.id)
            return queryset.filter(id__in=projects)
        
        return queryset
