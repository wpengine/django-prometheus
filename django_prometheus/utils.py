from prometheus_client import REGISTRY, Metric
import re
from threading import Lock
import time


def Time():
    """Returns some representation of the current time.

    This wrapper is meant to take advantage of a higher time
    resolution when available. Thus, its return value should be
    treated as an opaque object. It can be compared to the current
    time with TimeSince().
    """
    # TODO(korfuri): if python>3.3, use perf_counter() or monotonic().
    return time.time()


def TimeSince(t):
    """Compares a value returned by Time() to the current time.

    Returns:
      the time since t, in fractional seconds.
    """
    return time.time() - t


def PowersOf(logbase, count, lower=0, include_zero=True):
    """Returns a list of count powers of logbase (from logbase**lower)."""
    if not include_zero:
        return [logbase ** i for i in range(lower, count+lower)]
    else:
        return [0] + [logbase ** i for i in range(lower, count+lower)]


# This should be taken directly from prometheus_client
_METRIC_NAME_RE = re.compile(r'^[a-zA-Z_:][a-zA-Z0-9_:]*$')
_METRIC_LABEL_NAME_RE = re.compile(r'^[a-zA-Z_:][a-zA-Z0-9_:]*$')


class BaseLabelGauge(object):
    """A base class for LabelGauge and CallbackLabelGauge.

    This provides the basic functionality for a metric of type "A
    label-valued gauge whose values are all updated at the same time".
    """
    def __init__(self, name, documentation, labelnames, namespace='',
                 subsystem='', registry=REGISTRY):
        # This should be deduplicated against _MetricWrapper.init
        full_name = ''
        if namespace:
            full_name += namespace + '_'
        if subsystem:
            full_name += subsystem + '_'
        full_name += name
        if not _METRIC_NAME_RE.match(full_name):
            raise ValueError('Invalid metric name: ' + full_name)

        if registry:
            registry.register(self)

        def collect():
            metric = Metric(full_name, documentation, 'gauge')
            for suffix, labels, value in self.get_samples():
                metric.add_sample(full_name + suffix, labels, value)
            return [metric]
        self.collect = collect

    def get_samples(self):
        with self._lock:
            samples = self._samples
        return samples

    def set_samples(self, samples):
        with self._lock:
            self._samples = samples


class LabelGauge(BaseLabelGauge):
    """A label-valued gauge whose values can be updated atomically."""
    def __init__(self, *args, **kwargs):
        self._samples = []
        self._lock = Lock()
        super(LabelGauge, self).__init__(*args, **kwargs)

    def get_samples(self):
        with self._lock:
            samples = self._samples
        return samples

    def set_samples(self, samples):
        with self._lock:
            self._samples = samples


class CallbackLabelGauge(BaseLabelGauge):
    """A label-valued gauge whose values are all provided at once by a
    callback.
    """
    def __init__(self, name, documentation, labelnames, callback, **kwargs):
        self._callback = callback
        super(CallbackLabelGauge, self).__init__(
            name, documentation, labelnames, **kwargs)

    def get_samples(self):
        return self._callback()
