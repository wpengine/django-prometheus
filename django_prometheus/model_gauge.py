from django_prometheus.utils import CallbackLabelGauge
from django.db.models import Count


class QuerySetGauge(object):
    """A gauge that exports the results of a queryset.

    Examples:

    Assuming we have a `Book` model with fields `published` and `author`:
      ```
      qs = Book.objects.filter(published=True)
      g = QuerySetGauge(qs, 'books_by_author_total',
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
        if labels:
            self._queryset = queryset.values(*labels)
        else:
            self._queryset = queryset
        self._g = CallbackLabelGauge(name, description, labels, self.Run)
        self._count_by = count_by

    def Run(self):
        queryset = self._queryset.annotate(total=Count(self._count_by))
        samples = []
        for row in queryset:
            value = row.pop('total')
            samples.append((u'', row, value))
        return samples
