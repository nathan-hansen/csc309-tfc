from django import forms

from classes.models import Class, ClassTimeTable, EnrollClass


class ClassActionForm(forms.Form):

    def form_action(self, class_obj: Class, user):
        raise NotImplementedError()

    def save(self, class_obj: Class, user):
        class_obj, user = self.form_action(class_obj, user)
        return class_obj, user

class ClassCreateTimeForm(ClassActionForm):
    class_time = forms.DateTimeField()
    class_end = forms.DateTimeField()
    duration = forms.DurationField()
    spot_left = forms.IntegerField()

    def form_action(self, class_obj: Class, user):
        return Class.set_time(
            class_time=self.cleaned_data['class_time'],
            class_end=self.cleaned_data['class_end'],
            duration=self.cleaned_data['duration'],
            spot_left=self.cleaned_data['spot_left'],
        )

class ClassEditTimeForm(ClassActionForm):
    ...

class ClassDeleteTimeForm(ClassActionForm):
    ...