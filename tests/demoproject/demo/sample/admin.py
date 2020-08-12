from django.contrib import admin

from unicef_snapshot.admin import ActivityInline, SnapshotModelAdmin

from demo.sample.models import Author


class AuthorAdmin(SnapshotModelAdmin):
    list_display = ('name', )
    inlines = (ActivityInline, )


admin.site.register(Author, AuthorAdmin)
