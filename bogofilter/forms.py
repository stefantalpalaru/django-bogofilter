from django_comments.forms import CommentForm
from bogofilter.models import BogofilterComment
import time

class BogofilterCommentForm(CommentForm):
    def get_comment_model(self):
        return BogofilterComment

