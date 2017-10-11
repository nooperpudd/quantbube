# encoding:utf-8
from .base import BaseSerializer


class DummySerializer(BaseSerializer):
    """
    dummy serializer
    """
    def dumps(self, data, *args, **kwargs):
        pass

    def loads(self, data, *args, **kwargs):
        pass
