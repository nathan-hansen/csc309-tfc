from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from classes.models import Class, ClassTimeTable, EnrollClass, Keywords

# Register your models here.
admin.site.register(Keywords)
admin.site.register(ClassTimeTable)
admin.site.register(EnrollClass)
admin.site.register(Class)
# @admin.register(Class)
# class ClassAdmin(admin.ModelAdmin):
#     def class_actions(self, obj):
#         return format_html(
#             '<a class="button" href="{}">Create Time</a>&nbsp;',
#             '<a class="button" href="{}">Edit Time</a>&nbsp;',
#             reverse('admin:classes_class_create_time', args=[obj.pk]),
#             reverse('admin:classes_class_edit_time', args=[obj.pk]),
#         )
#     class_actions.short_description = 'Actions'
#     class_actions.allow_tags = True

#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('class_settime/', self.set_class_time, name='class_settime'),
#             path('class_edittime/', self.edit_class_time, name='class_edittime'),
#         ]
#         return my_urls + urls

#     def set_class_time(self, request, class_id, *args, **kwargs):
#         return self.process_action(
#             request = request,
#             class_id = class_id,
#             action = 'set_time',
#             action_form = ClassCreateTimeForm,
#             action_title = 'Create Time',
#         )

#     def edit_class_time(self, request, class_id, *args, **kwargs):
#         return self.process_action(
#             request = request,
#             class_id = class_id,
#             action = 'edit_time',
#             action_form = ClassEditTimeForm,
#             action_title = 'Edit Time',
#         )

#     def process_action(self, request, class_id, action, action_form, action_title):
#         class_obj = Class.objects.get(id=class_id)
#         if request.method == 'POST':
#             form = action_form(request.POST)
#             if form.is_valid():
#                 form.save(class_obj, request.user)
#                 self.message_user(request, 'Action completed.')
#                 return HttpResponseRedirect(reverse('admin:classes_class_changelist'))
#         else:
#             form = action_form()

#         context = self.admin_site.each_context(request)
#         context['opts'] = self.model._meta
#         context['form'] = form
#         context['title'] = action_title
#         context['class_obj'] = class_obj
#         return TemplateResponse(
#             request,
#             'admin/classes/class_action.html',
#             context
#         )