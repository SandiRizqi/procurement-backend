from django.contrib import admin
from apps.vendors.models import Vendor, VendorDocument
from apps.persons.models import Person
from django.utils.html import format_html


class VendorPersonsInline(admin.TabularInline):  # Atau gunakan StackedInline
    model = Person
    extra = 0  # Jumlah form kosong yang ditampilkan
    fields = ["full_name", "role","email", "phone"]


# Register your models here.
class VendorDocumentInline(admin.TabularInline):  # Atau gunakan StackedInline
    model = VendorDocument
    extra = 0  # Jumlah form kosong yang ditampilkan
    fields = ["vendor",  "document_type", "title", 'file', 'file_link',]
    readonly_fields = ('file_link',)

    

    def file_link(self, obj):
        if not obj.file:
            return "-"
        return format_html(
            '<a id="download-link" href="{}" target="_blank">Download</a>',
            obj.signed_file_url
        )

    file_link.short_description = "File URL"

class VendorAdmin(admin.ModelAdmin):
    model = Vendor
    #change_list_template = 'admin/vendors/vendor/change_list.html'
    list_display = ["name", "vendor_type", "email"]
    list_filter = ["vendor_type"]
    search_fields = ("name", "npwp", "persons__full_name")
    inlines = [VendorDocumentInline, VendorPersonsInline] 

    fieldsets = (
        ('Vendor Info', {
            'fields': ('name', 'vendor_type', 'npwp'),
            'classes': ('wide',)
        }),
        ('Contact', {
            'fields': ('address', 'email', 'phone'),
            'classes': ('wide',)
        }),
    )


admin.site.register(Vendor, VendorAdmin)