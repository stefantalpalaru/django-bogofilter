from __future__ import absolute_import

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.test import TestCase
from django.test.utils import override_settings

from bogofilter.forms import BogofilterCommentForm
from bogofilter.models import BogofilterComment

from ..models import Article, Author


# workaround for bug #11154 - https://code.djangoproject.com/ticket/11154
from django.contrib.auth.management import create_permissions, _get_all_permissions
from django.contrib.auth import models as auth_app
from django.db.models import get_models
from django.db.models.signals import post_syncdb
from django.db import DEFAULT_DB_ALIAS, router

def new_create_permissions(app, created_models, verbosity, db=DEFAULT_DB_ALIAS, **kwargs):
    if not router.allow_syncdb(db, auth_app.Permission):
        return

    from django.contrib.contenttypes.models import ContentType

    app_models = get_models(app)

    # This will hold the permissions we're looking for as
    # (content_type, (codename, name))
    searched_perms = list()
    # The codenames and ctypes that should exist.
    ctypes = set()
    ctypes_for_models = ContentType.objects.get_for_models(*app_models, for_concrete_models=False)
    for klass, ctype in ctypes_for_models.items():
        ctypes.add(ctype)
        for perm in _get_all_permissions(klass._meta, ctype):
            searched_perms.append((ctype, perm))

    # Find all the Permissions that have a context_type for a model we're
    # looking for. We don't need to check for codenames since we already have
    # a list of the ones we're going to create.
    all_perms = set(auth_app.Permission.objects.using(db).filter(
        content_type__in=ctypes,
    ).values_list(
        "content_type", "codename"
    ))

    perms = [
        auth_app.Permission(codename=codename, name=name, content_type=ctype)
        for ctype, (codename, name) in searched_perms
        if (ctype.pk, codename) not in all_perms
    ]
    auth_app.Permission.objects.using(db).bulk_create(perms)
    if verbosity >= 2:
        for perm in perms:
            print("Adding permission '%s'" % perm)

post_syncdb.disconnect(create_permissions, \
                       dispatch_uid='django.contrib.auth.management.create_permissions')
post_syncdb.connect(new_create_permissions, \
                    dispatch_uid='django.contrib.auth.management.create_permissions')


# Shortcut
CT = ContentType.objects.get_for_model

# Helper base class for comment tests that need data.
@override_settings(PASSWORD_HASHERS=('django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',))
class CommentTestCase(TestCase):
    fixtures = ["comment_tests"]
    urls = 'testapp.urls_default'

    def createSomeComments(self):
        # Two anonymous comments on two different objects
        c1 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            user_name = "Joe Somebody",
            user_email = "jsomebody@example.com",
            user_url = "http://example.com/~joe/",
            comment = "First!",
            site = Site.objects.get_current(),
        )
        c2 = BogofilterComment.objects.create(
            content_type = CT(Author),
            object_pk = "1",
            user_name = "Joe Somebody",
            user_email = "jsomebody@example.com",
            user_url = "http://example.com/~joe/",
            comment = "First here, too!",
            site = Site.objects.get_current(),
        )

        # Two authenticated comments: one on the same Article, and
        # one on a different Author
        user = User.objects.create(
            username = "frank_nobody",
            first_name = "Frank",
            last_name = "Nobody",
            email = "fnobody@example.com",
            password = "",
            is_staff = False,
            is_active = True,
            is_superuser = False,
        )
        c3 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            user = user,
            user_url = "http://example.com/~frank/",
            comment = "Damn, I wanted to be first.",
            site = Site.objects.get_current(),
        )
        c4 = BogofilterComment.objects.create(
            content_type = CT(Author),
            object_pk = "2",
            user = user,
            user_url = "http://example.com/~frank/",
            comment = "You get here first, too?",
            site = Site.objects.get_current(),
        )

        return c1, c2, c3, c4

    def getData(self):
        return {
            'name'      : 'Jim Bob',
            'email'     : 'jim.bob@example.com',
            'url'       : '',
            'comment'   : 'This is my comment',
        }

    def getValidData(self, obj):
        f = BogofilterCommentForm(obj)
        d = self.getData()
        d.update(f.initial)
        return d

from .app_api_tests import *
from .feed_tests import *
from .model_tests import *
from .comment_form_tests import *
from .templatetag_tests import *
from .comment_view_tests import *
from .moderation_view_tests import *
from .comment_utils_moderators_tests import *
from .bogofilter_tests import *

