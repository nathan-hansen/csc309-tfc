from django.db import models as m

from accounts.models import Account


class Class(m.Model):
    studio = m.ForeignKey('studios.Studio', on_delete=m.CASCADE, related_name='tfc_class')
    name = m.CharField(max_length=250)
    description = m.TextField()
    coach = m.CharField(max_length=250)
    duration = m.DurationField()

class Keywords(m.Model):
    classid = m.ForeignKey('Class', on_delete=m.CASCADE, related_name='keywords')
    keyword = m.CharField(max_length=250)

class ClassTimeTable(m.Model):
    classid = m.ForeignKey('Class', on_delete=m.CASCADE, related_name='timetable')
    time = m.DateTimeField()
    spotleft = m.IntegerField()

    def check_full(self):
        return self.spotleft != 0


class EnrollClass(m.Model):
    account = m.ForeignKey('accounts.Account', on_delete=m.CASCADE, related_name='enrollclass')
    classtime = m.ForeignKey('classes.ClassTimeTable', on_delete=m.CASCADE, related_name='enrollclass')

    def enroll(self, account: Account, classtime: ClassTimeTable):
        self.account = account
        self.classtime = classtime
        self.save()

    def check_enroll(self, account: Account, classtime: ClassTimeTable):
        return self.objects.filter(account=account, classtime=classtime).exists()

    def get_user_enroll(self, account: Account):
        return self.objects.filter(account=account)