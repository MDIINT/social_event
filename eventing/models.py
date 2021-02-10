from django.db import models


class Event(models.Model):
    """
    Represents an event
    """
    class Meta:
        verbose_name = "رویداد"
        verbose_name_plural = "رویداد"

    title = models.CharField('عنوان', max_length=150, unique=True, blank=False)

    subject_choices = (
        ('computer science', 'علوم رایانه'),
        ('data science', 'علم داده'),
        ('big data', 'کلان داده'),
        ('artificial intelligence', 'هوش مصنوعی'),
        ('security', 'امنیت'),
        ('software engineering', 'مهندسی نرافزار'),
        ('develop', 'توسعه‌ی نرم افزار'),
        ('cryptography', 'رمزنگاری'),
        ('crypto currency', 'رمز ارز'),
        ('IOT', 'اینترنت اشیا'),
        ('startup', 'استارتاپ'),
    )
    subject = models.CharField('موضوع', choices=subject_choices, max_length=30, blank=False)
    tags = models.CharField('برچسب ها', max_length=70, null=True, blank=True)
    organizer = models.ForeignKey\
        ('accounts.Profile', on_delete=models.PROTECT, verbose_name='برگزار کننده')
    start_date = models.DateTimeField('زمان شروع', blank=False)
    end_date = models.DateTimeField('زمان پایان', blank=False)
    details = models.TextField('درمورد رویداد', max_length=2000, blank=False)
    poster = models.ImageField('پوستر', upload_to='event_posters/', blank=False)
    trailer = models.FileField('پیش نمایش', upload_to='event_trailers', null=True, blank=True)
    '#Represent situation of each event'
    EVENT_NOT_STARTED = 1
    EVENT_DONE = 2
    EVENT_STARTED = 3
    EVENT_CANCELED = 4
    NOT_VERIFY = 5
    situation_choices = (
        (EVENT_NOT_STARTED, 'رویداد آغاز نشده'),
        (EVENT_STARTED, 'رویداد آغاز شده'),
        (EVENT_DONE, 'رویداد پایان یافت'),
        (EVENT_CANCELED, 'رویداد لغو شده'),
        (NOT_VERIFY, 'در انتظار تایید')
    )
    situation = models.IntegerField\
        ('وضعیت رویداد', blank=True, choices=situation_choices, default=NOT_VERIFY)
    verify = models.BooleanField('تایید', null=False, blank=True, default=False)
    cancel = models.BooleanField('لغو', null=False, blank=True, default=False)
    end = models.BooleanField('پایان', null=False, blank=True, default=False)
    made_time = models.DateTimeField('زمان ایجاد', auto_now_add=True)

    def __str__(self):
        """
        override Event models *string representation* method
        """
        title = self.title
        if self.organizer.organ_name is not None:
            organizer = self.organizer.organ_name
        else:
            organizer = self.organizer.user.get_full_name()

        return 'عنوان:{}--زمان:{}--برگزار کننده:{}'.format(title, self.start_date, organizer)

    def cancel_event(self):
        """
        user/organizer canceled event
        """
        self.cancel = True
        self.situation = Event.EVENT_CANCELED
