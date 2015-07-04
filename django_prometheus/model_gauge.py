from django_prometheus.utils import CallbackLabelGauge
from django.db.models import Count
from prometheus_client import Gauge


class QuerySetLabelGauge(object):
    """A gauge that exports the results of a queryset.

    Examples:

    Assuming we have a `Book` model with fields `published` and `author`:
      ```
      qs = Book.objects.filter(published=True)
      g = QuerySetLabelGauge(qs, 'books_by_author_total',
                             'Count of books by author.',
                             ['author'])
      ```
    Will export:
      ```
      books_by_author_total{author="Ernest Hemmingway"} 34
      books_by_author_total{author="Scott Adams"} 13
      ```
    """

    def __init__(self, queryset, name, description, labels, count_by='pk'):
        self._queryset = queryset.values(*labels)
        self._g = CallbackLabelGauge(name, description, labels, self.Run)
        self._count_by = count_by

    def Run(self):
        queryset = self._queryset.annotate(total=Count(self._count_by))
        samples = []
        for row in queryset:
            value = row.pop('total')
            samples.append((u'', row, value))
        return samples


class QuerySetGauge(object):
    """A gauge that exports the count of results in a queryset.

    Examples:
    ```
      qs = Books.objects.filter(published=False)
      g = QuerySetGauge(qs, 'books_unpublished_total',
                        'Count of books not yet published.')
    ```
    Will export the number of unpublished books.
    """
    def __init__(self, queryset, name, description):
        self._g = Gauge(name, description)
        self._g.set_function(lambda: queryset.count())
