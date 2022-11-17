import datetime

from django.db import models as m

from accounts.models import Account


class Class(m.Model):
    studio = m.ForeignKey('studios.Studio', on_delete=m.CASCADE, related_name='tfc_class')
    name = m.CharField(max_length=250)
    description = m.TextField()
    coach = m.CharField(max_length=250)
    class_start = m.DateField()
    class_end = m.DateField()
    class_time = m.TimeField()
    duration = m.DurationField()
    days_inbetween = m.IntegerField()
    spots = m.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.set_time()
        return self

    def set_time(self):
        self.duration = self.duration

        time_i = datetime.datetime.combine(self.class_start, self.class_time)
        while time_i <= datetime.datetime.combine(self.class_end, self.class_time):
            ClassTimeTable.objects.create(
                classid=self,
                time=time_i,
                spotleft=self.spots,
            )
            time_i += datetime.timedelta(days=self.days_inbetween)
            print("time_i: {}".format(time_i))

        return

    def edit_time(self):
        ClassTimeTable.objects.filter(class_id=self).delete()
        self.set_time()
    
    def delete_one_time(self, time: datetime.datetime):
        if not ClassTimeTable.objects.filter(class_id=self, time=time).exists():
            return False

        ClassTimeTable.objects.filter(class_id=self, time=time).delete()
        return True

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