from django.contrib import admin
from apps.procurements.models import Procurement, ProcurementParticipant
from django.utils.html import format_html

# Register your models here.
class ProcurementParticipantInline(admin.TabularInline):  # Atau gunakan StackedInline
    model = ProcurementParticipant
    extra = 1  # Jumlah form kosong yang ditampilkan
    fields = ["procurement", "vendor", "bid_value","file", "file_link","submission_date", "status"]
    readonly_fields = ("file_link",)

    def file_link(self, obj):
        if not obj.file:
            return "-"
        return format_html(
            '<a href="{}" target="_blank">Download</a>',
            obj.signed_file_url
        )
    file_link.short_description = "File URL"
 



class ProcurementAdmin(admin.ModelAdmin):
    model = Procurement
    ordering = ('-start_date',)
    list_display = ["project", "colored_status", "procurement_type", "start_date", "end_date"]
    list_filter = ["status", "procurement_type"]
    search_fields = ("project__project_name",)
    inlines = [ProcurementParticipantInline]
    
    def colored_status(self, obj):
        status_colors = {
            'open': 'status-open',
            'evaluation': 'status-evaluation',
            'winner_selected': 'status-winner_selected',
            'failed': 'status-failed',
        }
        css_class = status_colors.get(obj.status, '')
        return format_html(
            '<span class="{}">{}</span>',
            css_class,
            obj.get_status_display()
        )
    colored_status.short_description = 'Status'
    colored_status.admin_order_field = 'status'

    

class ProcurementParticipantAdmin(admin.ModelAdmin):
    model = ProcurementParticipant
    ordering = ('-submission_date',)
    list_display = ["procurement", "vendor", "bid_value", "file_link", "submission_date", "status"]
    list_filter = ["procurement", "vendor", "status"]
    search_fields = ("procurement",)

    def file_link(self, obj):
        if not obj.file:
            return "-"
        return format_html(
            '<a href="{}" target="_blank">Download</a>',
            obj.signed_file_url
        )

    file_link.short_description = "File URL"

admin.site.register(Procurement, ProcurementAdmin)
admin.site.register(ProcurementParticipant, ProcurementParticipantAdmin)
