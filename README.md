## description

Bayesian filtering applied to comment spam.

When CAPTCHA can't cut it anymore, Akismet and Disqus are not an option and the
weasels are closing in it's time to look at how the problem is tackled for the
biggest spam target of all time: email. Statistical analysis of word frequency
in individual messages proved to be simple, fast and reliable given enough
training data.

The trick to using a tool designed for emails on comment spam is to generate
email messages on the fly using comment data. Custom email headers allow us to
feed bogofilter any field we deem relevant. Training is done from the Django
admin, moderation with a custom moderation class and the app is highly
configurable.

## usage

- if you don't have a [custom comments app][4], make one
- in your custom comments app subclass your model from bogofilter.models.BogofilterComment
  (it's a proxy model that will not add any new fields)
- subclass your form from bogofilter.forms.BogofilterCommentForm
- [register][5] bogofilter.moderation.BogofilterCommentModerator or a subclass of it
  for the model that your comments are attached to. You can do this in that app's
  models.py file with something like this (assuming the target model is Entry):
```python
if Entry not in moderator._registry:
    moderator.register(Entry, BogofilterCommentModerator)
```
- in admin.py you probably want to change the fields order in your custom admin model.
  Use bogofilter.admin.bogo_status as a field for list_display.
  Register your admin model subclassed from bogofilter.admin.BogofilterCommentsAdmin like this:
```python
admin.site.unregister(BogofilterComment)
admin.site.register(MyComment, MyCommentAdmin)
```
- from the admin, train bogofilter with a batch of wanted (ham) and unwanted
  (spam) comments. 100 of each is a good start. After this filter by "Unsure"
  and mark those accordingly.  Next filter by 'Mismatches'. The assumption is
  that your ham comments are public, while the spam ones are not. Fix any
  conflict between bogofilter's status and your public status by marking the
  comments as spam or ham.
- you can pass command line arguments to bogofilter through the BOGOFILTER_ARGS
  variable in settings.py:
```python
BOGOFILTER_ARGS = ['-o', '0.7'] # lower the spam_cutoff from the default 0.95
```
- if you use bogofilter for more than one thing in the same account, you'll
  want to specify a directory other than the default ~/.bogofilter:
```python
BOGOFILTER_ARGS = ['-d', '~/.bogofilter_comments', '-o', '0.7']
```

## tips

- some spam bots stay only a few seconds on page so they can be weeded out based on that.
  You can get the 'time_on_page' field from the form (it's a floating point timestamp),
  store it in the model and return False from the 'allow' method of the moderator class
  if it's less than a certain value (4 seconds should be enough to avoid false negatives).
- for some reason, moderation signals might get lost and spam comments with a .bogotype() of 'S'
  (spam) or a time on page lower than your limit get through. You can deal with those with a
  periodic task that deletes them. I have mine running every 5 minutes and any notification
  related to new comments ignores those newer than that.
- regularly delete the spam comments after an interval long enough to allow you to rescue incorrectly
  classified ham.

## requirements

- [Django][1]
- [django-contrib-comments][2]
- [bogofilter][3]

## testing

```sh
python setup.py test
```
The test suite is shamelessly taken from django-contrib-comments and converted
to use the 'bogofilter' app wherever possible.

Tested with python-2.7.6, python-3.3.4, django-1.6.2, django-contrib-comments-1.5
and bogofilter-1.2.4 .

## credits

- author: Ștefan Talpalaru <stefantalpalaru@yahoo.com>

- homepage: https://github.com/stefantalpalaru/django-bogofilter

- PyPI: https://pypi.python.org/pypi/django-bogofilter

[1]: https://www.djangoproject.com/
[2]: https://github.com/django/django-contrib-comments
[3]: http://bogofilter.sourceforge.net/
[4]: http://django-contrib-comments.readthedocs.org/en/latest/custom.html
[5]: http://django-contrib-comments.readthedocs.org/en/latest/moderation.html

