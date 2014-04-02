from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.test.utils import override_settings

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from ..models import Article
from bogofilter.models import BogofilterComment
from bogofilter.moderation import BogofilterCommentModerator
from django_comments.moderation import moderator
from bogofilter.forms import BogofilterCommentForm
import shutil
import os

from . import CommentTestCase


CT = ContentType.objects.get_for_model


class BogofilterTests(CommentTestCase):

    def CommentFormData(self, data):
        f = BogofilterCommentForm(self.article)
        d = data.copy()
        d.update(f.initial)
        return d

    def setUp(self):
        super(BogofilterTests, self).setUp()
        self.article = Article.objects.get(pk=1)

        # register our moderator
        if Article not in moderator._registry:
            moderator.register(Article, BogofilterCommentModerator)

        # training spam
        self.c1 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            site = Site.objects.get_current(),
            comment = "Tirage du tarot de marseille gratuit en ligne horoscope homme balance 2011",
            user_name = "voyance gratuite",
            user_email = "nicholas_archdall@example.com",
            user_url = "http://www.alainfauquet.fr/",
            ip_address = "85.254.74.3",
        )
        self.c1.mark_spam()
        self.c2 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            site = Site.objects.get_current(),
            comment = "Tirage du tarot de marseille gratuit en ligne horoscope homme balance 2011",
            user_name = "voyance gratuite en ligne",
            user_email = "silas_poulson@example.com",
            user_url = "http://www.annonces-flash.com/",
            ip_address = "85.254.75.75",
        )
        self.c2.mark_spam()
        self.c3 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            site = Site.objects.get_current(),
            comment = "Voyance sante gratuite tirag tarot gratuit",
            user_name = "voyance gratuite",
            user_email = "adalbertohudd@example.com",
            user_url = "http://www.annonces-flash.com/",
            ip_address = "85.254.81.91",
        )
        self.c3.mark_spam()
        self.c4 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            site = Site.objects.get_current(),
            comment = "Voyance pendule gratuite horoscope christine haas 2011",
            user_name = "voyance",
            user_email = "elainecatalano@example.com",
            user_url = "http://www.alainfauquet.fr/",
            ip_address = "85.254.81.202",
        )
        self.c4.mark_spam()
        
        # training ham
        self.c7 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            site = Site.objects.get_current(),
            comment = "Great post. Saved me a ton of time. Thanks.",
            user_name = "Reg Doe",
            user_email = "reg@example.com",
            user_url = "http://www.regdoe.ca/",
            ip_address = "95.47.208.0",
        )
        self.c7.mark_ham()
        self.c8 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            site = Site.objects.get_current(),
            comment = "This is just awesome! Thanks for the defs.",
            user_name = "Shivi",
            user_email = "shivinitin@example.com",
            user_url = "",
            ip_address = "121.160.222.97",
        )
        self.c8.mark_ham()
        self.c9 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            site = Site.objects.get_current(),
            comment = "Worked for me thanks",
            user_name = "raga",
            user_email = "s-hanson@example.com",
            user_url = "",
            ip_address = "140.240.54.144",
        )
        self.c9.mark_ham()
        self.c10 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            site = Site.objects.get_current(),
            comment = "Nice post. Very concise and useful. I like your approach of attaching custom attributes to the QPushButton. I tend to do this sort of thing using lambda. I'm not sure if one way is better than the other, just an observation: button.clicked.connect(lambda: self.listen(name, url)) http://codrspace.com/durden/using-lambda-with-pyqt-signals/ I've also seen people solve this problem with functools.partial: http://eli.thegreenplace.net/2011/04/25/passing-extra-arguments-to-pyqt-slot/",
            user_name = "Luki Lii",
            user_email = "durdenmisc@example.com",
            user_url = "http://lukilii.me/",
            ip_address = "137.31.79.10",
        )
        self.c10.mark_ham()
        self.c11 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            site = Site.objects.get_current(),
            comment = "Yes, using the lambda is a valid alternative but self.sender() no longer works inside self.listen() - or inside the lambda for that matter.",
            user_name = "Stefan Talpalaru",
            user_email = "stefan.talpalaru@example.com",
            user_url = "",
            ip_address = "78.23.54.6",
        )
        self.c11.mark_ham()
        self.c12 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            site = Site.objects.get_current(),
            comment = "Neat article. For future reference: http://blog.scoopz.com/2011/05/05/listen-to-any-bbc-radio-live-stream-using-vlc-including-radio-1-and-1xtra/",
            user_name = "carlisle",
            user_email = "n-a@example.com",
            user_url = "",
            ip_address = "177.208.61.148",
        )
        self.c12.mark_ham()
        self.c13 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            site = Site.objects.get_current(),
            comment = "Thank you!",
            user_name = "Gordon",
            user_email = "thisisgordonsemail@example.com",
            user_url = "http://cafeofbrokenarms.com/",
            ip_address = "130.106.173.235",
        )
        self.c13.mark_ham()
        self.c14 = BogofilterComment.objects.create(
            content_type = CT(Article),
            object_pk = "1",
            site = Site.objects.get_current(),
            comment = "Thank you for this great bit of code. It has worked for the two websites I have used this in. Your article is very informative and written with a very fun tone. Thanks!",
            user_name = "Rachel",
            user_email = "englerae@example.com",
            user_url = "",
            ip_address = "172.13.9.220",
        )
        self.c14.mark_ham()

        # test spam
        self.client.post("/post/",
                         self.CommentFormData({
                             "comment"   : "Horoscope yahoo du jour l ascendant astrologique",
                             "name"      : "voyance",
                             "email"     : "genesisroesch@example.com",
                             "url"       : "http://www.annonces-flash.com/",
                         }),
                         REMOTE_ADDR="85.254.82.164")
        self.c5 = BogofilterComment.objects.order_by('-submit_date')[0]
        self.client.post("/post/",
                         self.CommentFormData({
                             "comment"   : "Accouchement lune calcul horoscope femme scorpion",
                             "name"      : "voyance gratuite en ligne",
                             "email"     : "cliftonlerner@example.com",
                             "url"       : "http://www.annonces-flash.com/",
                         }),
                         REMOTE_ADDR="85.254.153.161")
        self.c6 = BogofilterComment.objects.order_by('-submit_date')[0]


        # test ham
        self.client.post("/post/",
                         self.CommentFormData({
                             "comment"   : "Hi, thanks for the blog. Can this project still work with facebook oauth 2.0 and kay framework 3? because I see the project is pretty old (3years). I try to use Kay ext for facebook/twitter but it does not work. Therefore, I hope your project can help me.",
                             "name"      : "Nam",
                             "email"     : "dbss.contact@example.com",
                             "url"       : "",
                         }),
                         REMOTE_ADDR="48.131.92.5")
        self.c28 = BogofilterComment.objects.order_by('-submit_date')[0]
        self.client.post("/post/",
                         self.CommentFormData({
                             "comment"   : "This post was very useful. Having my logs in UTC will be excellent.",
                             "name"      : "Tim Wilder",
                             "email"     : "wildertm@example.com",
                             "url"       : "",
                         }),
                         REMOTE_ADDR="207.145.42.4")
        self.c29 = BogofilterComment.objects.order_by('-submit_date')[0]
        self.client.post("/post/",
                         self.CommentFormData({
                             "comment"   : "One other thing: since the lambda's body is not evalued until the signal is triggered, a naive implementation would make all the buttons play the last radio station (because 'name' and 'url' point to it at the end of the loop). The only way it works is something like this: button.clicked.connect(lambda _button=button, _name=name, _url=url: self.listen(_button, _name, _url)) Yes, it's ugly...",
                             "name"      : "Stefan Talpalaru",
                             "email"     : "stefan.talpalaru@example.com",
                             "url"       : "http://stefantalpalaru.wordpress.com",
                         }),
                         REMOTE_ADDR="86.8.17.57")
        self.c30 = BogofilterComment.objects.order_by('-submit_date')[0]
        
    def tearDown(self):
        super(BogofilterTests, self).tearDown()
        bogofilter_dir = settings.BOGOFILTER_ARGS[1]
        if os.path.isdir(bogofilter_dir):
            shutil.rmtree(bogofilter_dir)
        # unregister our moderator
        if Article in moderator._registry:
            moderator.unregister(Article)

    def testBogo(self):
        # test the spam
        self.assertEqual(self.c5.bogotype()[0], 'S')
        self.assertEqual(self.c5.is_public, False)
        self.assertEqual(self.c6.bogotype()[0], 'S')
        self.assertEqual(self.c6.is_public, False)
        # test the ham
        self.assertNotEqual(self.c28.bogotype()[0], 'S')
        self.assertEqual(self.c28.is_public, True)
        self.assertNotEqual(self.c29.bogotype()[0], 'S')
        self.assertEqual(self.c29.is_public, True)
        self.assertNotEqual(self.c30.bogotype()[0], 'S')
        self.assertEqual(self.c30.is_public, True)

