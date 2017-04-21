# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Tokens(models.Model):
    user = models.OneToOneField(User, related_name="tokens",null=False)
    token = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if self.token is None or self.token == "":
            import uuid
            self.token=uuid.uuid4().hex
        super(Tokens, self).save(*args, **kwargs)
