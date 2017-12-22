from haystack import indexes
from .models import Post

# original instructions returned error on:
# cmd: python manage.py build_solr_schema
# error: TypeError: context must be a dict rather than Context.
# https://groups.google.com/forum/#!topic/django-haystack/YigE4tg89Wc
# updated python3.6/site-packages/haystack/management/commands/build_solr_schema.py
# for my current venv

class PostIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)
  publish = indexes.DateTimeField(model_attr='publish')

  def get_model(self):
    return Post

  def index_queryset(self, using=None):
    return self.get_model().published.all()

