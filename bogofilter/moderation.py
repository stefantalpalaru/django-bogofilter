from django_comments.moderation import CommentModerator


class BogofilterCommentModerator(CommentModerator):
    def moderate(self, comment, content_object, request):
        should_be_moderated = False
        if comment.bogotype()[0] == 'S':
            should_be_moderated = True
        return should_be_moderated

