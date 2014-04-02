from django.contrib import admin
from django_comments.admin import CommentsAdmin
from bogofilter.actions import mark_spam, mark_ham, run_spam_filter
from bogofilter.models import BogofilterComment


BOGO_STATUS_LABELS = {
    'S': 'spam',
    'H': 'ham',
    'U': 'unsure',
}

def bogo_status(obj):
    try:
        bogotype, score = obj.bogotype()
        res = '%s<br><em>%f</em>' % (BOGO_STATUS_LABELS.get(bogotype, ''), score)
    except Exception as e:
        res = e
    return res
bogo_status.short_description = 'bogofilter status'
bogo_status.allow_tags = True

class BogoFilter(admin.SimpleListFilter):
    title = 'bogofilter status'
    parameter_name = 'bogofilter_status'
    def lookups(self, request, model_admin):
        return (
            ('S', 'Spam'),
            ('H', 'Ham'),
            ('U', 'Unsure'),
            ('M', 'Mismatches'),
        )
    def queryset(self, request, queryset):
        btype = self.value()
        if btype in ['S', 'H', 'U']:
            try:
                ids = []
                for obj in queryset.iterator():
                    if obj.bogotype()[0] == btype:
                        ids.append(obj)
            except:
                ids = []
            return queryset.filter(pk__in=ids)
        elif btype == 'M':
            try:
                ids = []
                for obj in queryset.iterator():
                    if (obj.bogotype()[0] == 'S' and obj.is_public == True) or (obj.bogotype()[0] == 'H' and obj.is_public == False):
                        ids.append(obj)
            except:
                ids = []
            return queryset.filter(pk__in=ids)

class BogofilterCommentsAdmin(CommentsAdmin):
    actions = CommentsAdmin.actions + [mark_spam, mark_ham, run_spam_filter]
    list_display = ('object_pk', bogo_status, 'is_public', 'name', 'content_type', 'ip_address', 'submit_date', 'is_removed')
    list_filter = ('submit_date', 'site', 'is_public', 'is_removed', BogoFilter)

admin.site.register(BogofilterComment, BogofilterCommentsAdmin)

