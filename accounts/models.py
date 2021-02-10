from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    """
    Represent a user's profile
    """
    class Meta:
        verbose_name = 'نمایه کاربری'
        verbose_name_plural = 'نمایه کاربری'

    user = models.OneToOneField\
        (User, on_delete=models.CASCADE, verbose_name='حساب کاربری')
    # important fields that are stored in User model:
    #   first_name, last_name, email, date_joined

    mobile = models.CharField('تلفن همراه', max_length=11, null=True, blank=False)

    PERSON = 1
    COMPANY = 2
    user_type_choices = ((PERSON, 'حقیقی'), (COMPANY, 'حقوقی'))
    user_type = models.IntegerField\
        ('نوع کاربری', choices=user_type_choices, null=True, blank=True)
    birth_date = models.DateField('تاریخ تولد', null=True, blank=True)
    address = models.TextField('آدرس', null=True, blank=True)
    organ_name = models.CharField('سازمان یا نام رسمی', max_length=50, null=False, blank=False)
    profile_image = models.ImageField('تصویر', upload_to='users/profile_images/', null=True, blank=True)

    def __str__(self):

        if self.user.first_name:
            show_name = self.user.get_full_name()
        else:
            show_name = self.organ_name
        return show_name


class Submit(models.Model):
    """
    Represent Submit model
    """
    class Meta:
        verbose_name = 'ثبت نام'
        verbose_name_plural = 'ثبت نام'

    submitted_user = models.ForeignKey\
        ('Profile', on_delete=models.PROTECT, blank=False, verbose_name='ثبت نام کننده')
    submitted_event = models.ForeignKey\
        ('eventing.Event', on_delete=models.PROTECT, blank=False, verbose_name='رویداد')
    cancel = models.BooleanField('وضعیت ثبت نام', null=False, default=False)
    submit_time = models.DateTimeField('زمان ثبت نام', blank=False, auto_now_add=True)

    def __str__(self):
        """
        override Submit models *string representation* method
        """
        submitter = self.submitted_user.user.get_full_name()
        event = self.submitted_event.title
        return 'ثبت نام کننده:{} -- رویداد:{}'.format(submitter, event)

    def cancel_submit(self):
        """
        user cancel submitted event
        """
        self.cancel = True

