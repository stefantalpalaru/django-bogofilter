from django.db import models
from django_comments.models import Comment
import bogofilter.utils as bogo
from django.conf import settings
import traceback


class BogofilterComment(Comment):
    bogofilter_args = getattr(settings, 'BOGOFILTER_ARGS', [])
    bogofilter_extra_headers = {}
    _bogofilter_email_msg = None
    _bogotype = None

    def make_email_msg(self):
        if self._bogofilter_email_msg is None:
            extra_headers = self.bogofilter_extra_headers.copy()
            extra_headers.update({
                'X-IP': self.ip_address,
                'X-URL': self.user_url,
            })
            self._bogofilter_email_msg =  bogo.make_email_msg(
                from_email = self.user_email,
                subject = self.user_name,
                body = self.comment,
                extra_headers = extra_headers)
        return self._bogofilter_email_msg

    def mark_spam(self):
        """
        raises:
            subprocess.CalledProcessError
            bogofilter.utils.BogofilterException
        """
        bogo.mark_spam(self.make_email_msg(), bogofilter_args = self.bogofilter_args[:])
        self.is_public = False
        self.save()

    def mark_ham(self):
        """
        raises:
            subprocess.CalledProcessError
            bogofilter.utils.BogofilterException
        """
        bogo.mark_ham(self.make_email_msg(), bogofilter_args = self.bogofilter_args[:])
        self.is_public = True
        self.save()

    def bogotype(self):
        """
        raises:
            subprocess.CalledProcessError
            bogofilter.utils.BogofilterException
        """
        if self._bogotype is None:
            self._bogotype = bogo.classify_msg(self.make_email_msg(), bogofilter_args = self.bogofilter_args[:])
        return self._bogotype

    def run_spam_filter(self):
        btype = self.bogotype()[0]
        if btype == 'S':
            self.is_public = False
            self.save()
        elif btype == 'H':
            self.is_public = True
            self.save()

    class Meta:
        ordering = ('submit_date',)
        permissions = [("can_moderate", "Can moderate comments")]
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        proxy = True

