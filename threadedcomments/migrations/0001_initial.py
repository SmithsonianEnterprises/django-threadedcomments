# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('tweentribune', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreadedComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.IntegerField(verbose_name='object ID', db_index=True)),
                ('tree_path', models.CharField(verbose_name='Tree path', max_length=500, editable=False)),
                ('comment', models.TextField(max_length=3000, verbose_name='comment')),
                ('submit_date', models.DateTimeField(default=None, verbose_name='date/time submitted')),
                ('ip_address', models.GenericIPAddressField(unpack_ipv4=True, null=True, verbose_name='IP address', blank=True)),
                ('is_public', models.BooleanField(default=False, help_text='Uncheck this box to make the comment effectively disappear from the site.', db_index=True, verbose_name='is public')),
                ('is_removed', models.BooleanField(default=False, help_text='Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.', verbose_name='is removed')),
                ('is_private_thread', models.BooleanField(default=False, db_index=True, verbose_name=b'is private thread')),
                ('classroom', models.ForeignKey(related_name='comments', blank=True, to='tweentribune.Classroom', null=True)),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_threadedcomment', verbose_name='content type', to='contenttypes.ContentType')),
                ('last_child', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Last child', blank=True, to='threadedcomments.ThreadedComment', null=True)),
                ('parent', models.ForeignKey(related_name='children', default=None, blank=True, to='threadedcomments.ThreadedComment', null=True, verbose_name='Parent')),
                ('site', models.ForeignKey(to='sites.Site')),
                ('user', models.ForeignKey(related_name='threadedcomment_comments', verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('tree_path',),
                'db_table': 'threadedcomments_comment',
                'verbose_name': 'Threaded comment',
                'verbose_name_plural': 'Threaded comments',
            },
        ),
    ]
