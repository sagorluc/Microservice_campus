from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4
from base64 import b64encode, b64decode
from uuid import uuid4

from random import randint
def random_num_generator():
    n = 10
    range_start = 10**(n-1)
    range_end = (10**n)-1
    random_value = randint(range_start, range_end)
    return random_value


class DisputeSubmissionModel(models.Model): 
    submission_id = models.CharField(max_length=200, default=str(uuid4()))
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(
            auto_now_add=True,
            help_text="timestamp of creation"
        )
    created_by = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            related_name='user',
            null=True,
            blank=True
        )

    def __str__(self):
        return "{}{}".format(self.submission_id, self.created_by)

    # def save(self, *args, **kwargs):
    #     self.submission_id = str(random_num_generator())

    #     return super().save(*args, **kwargs)