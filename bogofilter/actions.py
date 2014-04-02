def mark_spam(modeladmin, request, queryset):
    for comment in queryset.all():
        comment.mark_spam()
mark_spam.short_description = 'Mark as spam [bogofilter]'

def mark_ham(modeladmin, request, queryset):
    for comment in queryset.all():
        comment.mark_ham()
mark_ham.short_description = 'Mark as ham [bogofilter]'

def run_spam_filter(modeladmin, request, queryset):
    for comment in queryset.all():
        comment.run_spam_filter()
run_spam_filter.short_description = 'Run through the spam filter [bogofilter]'

