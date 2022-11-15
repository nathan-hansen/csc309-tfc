from django.contrib import admin

from classes.models import Class, ClassTimeTable, Keywords

# Register your models here.
admin.site.register(Class)
admin.site.register(Keywords)
admin.site.register(ClassTimeTable)
