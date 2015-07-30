import django
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .models import ThreadedComment
from .compat import CommentForm


class ThreadedCommentForm(CommentForm):
    title = forms.CharField(label=_('Title'), required=False, max_length=getattr(settings, 'COMMENTS_TITLE_MAX_LENGTH', 255))
    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)

    def __init__(self, target_object, parent=None, data=None, initial=None):
        if django.VERSION >= (1,7):
            # Using collections.OrderedDict from Python 2.7+
            # This class does not have an insert method, have to replace it.
            from collections import OrderedDict
            keys = list(self.base_fields.keys())
            keys.remove('title')
            keys.insert(keys.index('comment'), 'title')

            self.base_fields = OrderedDict((k, self.base_fields[k]) for k in keys)
        else:
            self.base_fields.insert(
                self.base_fields.keyOrder.index('comment'), 'title',
                self.base_fields.pop('title')
            )

        # Remove fields
        self.base_fields['email'].required = False
        self.base_fields['email'].widget = forms.HiddenInput()
        self.base_fields['title'].widget = forms.HiddenInput()
        self.base_fields['name'].widget = forms.HiddenInput()
        self.base_fields['url'].widget = forms.HiddenInput()


        self.parent = parent
        if initial is None:
            initial = {}
        initial.update({'parent': self.parent})
        super(ThreadedCommentForm, self).__init__(target_object, data=data, initial=initial)

    def check_for_duplicate_comment(self, new):
        """
        Check that a submitted comment isn't a duplicate. This might be caused
        by someone posting a comment twice. If it is a dup, silently return the *previous* comment.
        """
        possible_duplicates = self.get_comment_model()._default_manager.using(
            self.target_object._state.db
        ).filter(
            content_type=new.content_type,
            object_pk=new.object_pk,
        )
        for old in possible_duplicates:
            if old.submit_date.date() == new.submit_date.date() and old.comment == new.comment:
                return old

        return new

    def get_comment_model(self):
        return ThreadedComment

    def get_comment_create_data(self):
        d = super(ThreadedCommentForm, self).get_comment_create_data()
        d['parent_id'] = self.cleaned_data['parent']
        d.pop('user_name')
        d.pop('user_email')
        d.pop('user_url')
        return d
