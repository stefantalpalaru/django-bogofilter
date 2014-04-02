from django.conf.urls import patterns, include
from django.contrib import admin
from bogofilter.models import BogofilterComment
from bogofilter.admin import BogofilterCommentsAdmin

# Make a new AdminSite to avoid picking up the deliberately broken admin
# modules in other tests.
admin_site = admin.AdminSite()
admin_site.register(BogofilterComment, BogofilterCommentsAdmin)

# To demonstrate proper functionality even when ``delete_selected`` is removed.
admin_site2 = admin.AdminSite()
admin_site2.disable_action('delete_selected')
admin_site2.register(BogofilterComment, BogofilterCommentsAdmin)

urlpatterns = patterns('',
    (r'^admin/', include(admin_site.urls)),
    (r'^admin2/', include(admin_site2.urls)),
)
