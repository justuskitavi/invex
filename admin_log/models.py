from django.db import models 
from django.contrib.admin.models import LogEntryManager, ADDITION, CHANGE, DELETION
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from invex.models import User


class CustomLogEntry(models.Model):
    action_time = models.DateTimeField(default=now, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name = '+',
        db_column='user_id',
        to_field='userID',
    )

    content_type = models.ForeignKey(
        ContentType,
        models.SET_NULL,
        blank=True,
        null=True,
    )

    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField(choices=[
        (ADDITION, 'Addition'),
        (CHANGE, 'Change'),
        (DELETION, 'Deletion')
    ])
    change_message = models.TextField(blank=True)


    objects = LogEntryManager()

    class Meta:
        db_table = 'custom_admin_log'
        verbose_name = 'log entry'
        verbose_name_plural = 'log entries'

    def __str__(self):
        return f"{self.user} - {self.object_repr}"

