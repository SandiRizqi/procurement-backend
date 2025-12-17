from django.contrib import admin
from apps.procurements.models import Procurement, ProcurementParticipant
from django.utils.html import format_html

# Register your models here.
class ProcurementParticipantInline(admin.TabularInline):  # Atau gunakan StackedInline
    model = ProcurementParticipant
    extra = 0  # Jumlah form kosong yang ditampilkan
    fields = ["procurement", "vendor", "bid_value_display", "file_link","submission_date", "status"]
    readonly_fields = ("file_link", "bid_value_display",)

    def has_add_permission(self, request, obj=None):
        return False  # semua user tidak bisa tambah data

    def file_link(self, obj):
        if not obj.file:
            return "-"
        return format_html(
            '<a id="download-link" href="{}" target="_blank">Download</a>',
            obj.signed_file_url
        )
    file_link.short_description = "DOC URL"


    def bid_value_display(self, obj):
        if obj.bid_value is None:
            return "-"

        value = float(obj.bid_value)
        formatted_value = f"Rp {value:,.2f}".replace(',', '.')
        color = '#6c757d'

        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<span style="font-weight: 600; color: {}; font-size: 14px;">{}</span>'
            '</div>',
            color, formatted_value
        )

    bid_value_display.short_description = 'BID'
    bid_value_display.admin_order_field = 'bid_value'
 



class ProcurementAdmin(admin.ModelAdmin):
    model = Procurement
    ordering = ('-start_date',)
    list_display = ["project", "colored_status", "procurement_type", "start_date", "end_date"]
    list_filter = ["status", "procurement_type"]
    search_fields = ("project__project_name",)
    inlines = [ProcurementParticipantInline]

    fieldsets = (
        ('procurement Info', {
            'fields': ('project', 'procurement_type'),
            'classes': ('wide',)
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'status'),
            'classes': ('wide',)
        }),
    )
    
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
    list_display = ["procurement", "vendor", "bid_value_display", "file_link", "submission_date", "status"]
    list_filter = ["procurement", "vendor", "status"]
    search_fields = ("procurement",)

    fieldsets = (
        ('Procurement Info', {
            'fields': ('procurement', 'submission_date', "status"),
            'classes': ('wide',)
        }),
        ('Vendor Info', {
            'fields': ('vendor', 'bid_value', 'file'),
            'classes': ('wide',)
        }),
    )

    def file_link(self, obj):
        if not obj.file:
            return "-"
        return format_html(
            '<a id="download-link" href="{}" target="_blank">Download</a>',
            obj.signed_file_url
        )

    file_link.short_description = "DOC URL"

    def bid_value_display(self, obj):
        if obj.bid_value is None:
            return "-"

        value = float(obj.bid_value)
        formatted_value = f"Rp {value:,.2f}".replace(',', '.')
        color = '#6c757d'

        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<span style="font-weight: 600; color: {}; font-size: 14px;">{}</span>'
            '</div>',
            color, formatted_value
        )

    bid_value_display.short_description = 'BID'
    bid_value_display.admin_order_field = 'bid_value'
 

admin.site.register(Procurement, ProcurementAdmin)
admin.site.register(ProcurementParticipant, ProcurementParticipantAdmin)
