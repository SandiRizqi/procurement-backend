from django.contrib import admin
from apps.persons.models import Person, PersonDocument
from django.utils.html import format_html




# Register your models here.
class PersonDocumentInline(admin.TabularInline):  # Atau gunakan StackedInline
    model = PersonDocument
    extra = 1  # Jumlah form kosong yang ditampilkan
    fields = ["title", 'file', 'file_link', 'issued_date']
    readonly_fields = ('file_link',)

    def file_link(self, obj):
        if not obj.file:
            return "-"
        return format_html(
            '<a href="{}" target="_blank">Download</a>',
            obj.signed_file_url
        )

    file_link.short_description = "File URL"

class PersonAdmin(admin.ModelAdmin):
    model = Person
    ordering = ('vendor',)
    list_display = ["full_name", "vendor", "role", "email", "phone"]
    list_filter = ["vendor", ]
    search_fields = ("full_name", "email", )
    inlines = [PersonDocumentInline] 
    




admin.site.register(Person, PersonAdmin)