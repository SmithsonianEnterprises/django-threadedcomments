from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .compat import BASE_APP
from .models import ThreadedComment


# This code is not in the .compat module to avoid admin imports in all other code.
# The admin import usually starts a model registration too, hence keep these imports here.

if BASE_APP == 'django.contrib.comments':
    # Django 1.7 and below
    from django.contrib.comments.admin import CommentsAdmin
elif BASE_APP == 'django_comments':
    # Django 1.8 and up
    from django_comments.admin import CommentsAdmin
else:
    raise NotImplementedError()


class IsPublicCommentFilter(admin.SimpleListFilter):
    title = "Is Public"
    parameter_name = "is_public"

    def lookups(self, request, model_admin):
        return [(1, "Yes"), (0, "No")]

    def queryset(self, request, queryset):
        """
        If filter exists, filter queryset and return else
        just return the queryset filtered by current site.
        """
        if not self.value() is None:
            value = bool(int(self.value()))
            queryset = queryset \
                .filter(is_public=value) \
                .filter(classroom__public_comments=value) \
                .distinct()

        return queryset


class ThreadedCommentsAdmin(CommentsAdmin):
    fieldsets = (
        (None,
         {'fields': ('content_type', 'object_pk', 'site')}
         ),
        (_('Content'),
         {'fields': ('user', 'classroom', 'comment')}
         ),
        (_('Hierarchy'),
         {'fields': ('parent',)}
         ),
        (_('Metadata'),
         {'fields': ('submit_date', 'ip_address', 'is_public', 'classroom_public', 'is_removed')}
         ),
    )
    list_filter = ('submit_date', 'site', IsPublicCommentFilter, 'is_removed')

    list_display = ('content_type', 'object_pk', 'parent',
                    'ip_address', 'submit_date', 'classroom_public', 'is_public', 'is_removed')
    search_fields = ('comment', 'user__username', 'ip_address', 'object_pk')
    raw_id_fields = ("parent", 'user', 'classroom')
    readonly_fields = ['classroom_public']

    def classroom_public(self, obj):
        if obj.classroom:
            return obj.classroom.public_comments
        return False

    classroom_public.boolean = True


admin.site.register(ThreadedComment, ThreadedCommentsAdmin)
