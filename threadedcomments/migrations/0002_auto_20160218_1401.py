# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tweentribune', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('sites', '0001_initial'),
        ('threadedcomments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='threadedcomment',
            name='classroom',
            field=models.ForeignKey(related_name='comments', blank=True, to='tweentribune.Classroom', null=True),
        ),
        migrations.AddField(
            model_name='threadedcomment',
            name='content_type',
            field=models.ForeignKey(related_name='content_type_set_for_threadedcomment', verbose_name='content type', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='threadedcomment',
            name='last_child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Last child', blank=True, to='threadedcomments.ThreadedComment', null=True),
        ),
        migrations.AddField(
            model_name='threadedcomment',
            name='parent',
            field=models.ForeignKey(related_name='children', default=None, blank=True, to='threadedcomments.ThreadedComment', null=True, verbose_name='Parent'),
        ),
        migrations.AddField(
            model_name='threadedcomment',
            name='site',
            field=models.ForeignKey(to='sites.Site'),
        ),
        migrations.AddField(
            model_name='threadedcomment',
            name='user',
            field=models.ForeignKey(related_name='threadedcomment_comments', verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
