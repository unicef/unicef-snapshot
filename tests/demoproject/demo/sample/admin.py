from demo.sample.models import Author
from django.contrib import admin

from unicef_snapshot.admin import ActivityInline, SnapshotModelAdmin


class AuthorAdmin(SnapshotModelAdmin):
    list_display = ('name', )
    inlines = (ActivityInline, )


admin.site.register(Author, AuthorAdmin)
