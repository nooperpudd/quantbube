# encoding:utf-8
import abc
import datetime
import decimal
import typing

import msgpack
import rapidjson


class ParseError(Exception):
    """
    MessagePack parse error
    """
    pass


class BaseSerializer(metaclass=abc.ABCMeta):
    """
    The base serializer class,
    only defines the signature for loads and dumps
    """

    @abc.abstractmethod
    def loads(self, data, *args, **kwargs):
        """
        Deserialize the data
        :param data: the structure data need to be
        :return:
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def dumps(self, data, *args, **kwargs):
        """
        Serialize ``data`` to kinds of type
        :param data:
        :return:
        """
        raise NotImplementedError()


class MsgPackDecoder(object):
    """
    decode serializer data
    """

    def decode(self, obj):
        """
        :param obj:
        :return:
        """
        if "__class__" in obj:
            decode_func = getattr(self, "decode_%s" % obj["__class__"])
            return decode_func(obj)
        return obj

    def decode_datetime(self, obj):
        return datetime.datetime.strptime(obj["str"], "%Y-%m-%dT%H:%M:%S.%f")

    def decode_date(self, obj):
        return datetime.datetime.strptime(obj["str"], "%Y-%m-%d")

    def decode_time(self, obj):
        return datetime.datetime.strptime(obj["str"], "%H:%M:%S.%f")

    def decode_decimal(self, obj):
        return decimal.Decimal(obj["str"])


class MsgPackEncoder(object):
    """
    encode the data type to the message pack format
    """

    @typing.overload
    def encode(self, obj):
        """
        :param obj:
        :return:
        """
        return obj

    @typing.overload
    def encode(self, obj: datetime.date):
        """
        :param obj:
        :return:
        """
        return {"__class__": "date", "str": obj.strftime("%Y-%m-%d")}

    @typing.overload
    def encode(self, obj: datetime.datetime):
        """
        :param obj:
        :return:
        """
        return {"__class__": "datetime", "str": obj.strftime("%Y-%m-%dT%H:%M:%S.%f")}

    @typing.overload
    def encode(self, obj: datetime.time):
        """
        :param obj:
        :return:
        """
        return {"__class__": "time", "str": obj.strftime("%H:%M:%S.%f")}

    @typing.overload
    def encode(self, obj: decimal.Decimal):
        """
        :param obj:
        :return:
        """
        return {"__class__": "decimal", "str": str(obj)}


class MsgPackSerializer(BaseSerializer):
    """
    MessagePack serializer

    CPython’s GC starts when growing allocated object.
     This means unpacking may cause useless GC.
     You can use gc.disable() when unpacking large message.
    """

    def loads(self, data, *args, **kwargs):
        """
        :param data:
        :return:
        """
        try:
            return msgpack.unpackb(data, encoding="utf-8",
                                   object_hook=MsgPackDecoder().decode, **kwargs)
        except Exception as e:
            raise ParseError("MessagePack loads error: %s" % e)

    def dumps(self, data, *args, **kwargs):
        """
        :param data:
        :return:
        """
        try:
            return msgpack.packb(data, default=MsgPackEncoder().encode, **kwargs)
        except Exception as e:
            raise ParseError("MessagePack dumps error: %s" % e)


class JsonSerializer(BaseSerializer):
    """
    Json object serializer

    http://python-rapidjson.readthedocs.io/en/latest/api.html
    """
    datetime_mode = rapidjson.DM_ISO8601

    def loads(self, data, object_hook=None, **kwargs):
        """
        :param data:
        :param object_hook:
        :return:
        """
        try:
            return rapidjson.loads(data, use_decimal=True,
                                   object_hook=object_hook,
                                   datetime_mode=self.datetime_mode, **kwargs)
        except Exception as e:
            raise ParseError("Json loads error: %s" % e)

    def dumps(self, data, default=None, **kwargs):
        """
        :param data:
        :param default:
        :return:
        """
        try:
            return rapidjson.dumps(data,
                                   default=default,
                                   use_decimal=True,
                                   datetime_mode=self.datetime_mode, **kwargs)
        except Exception as e:
            raise ParseError("Json Dumps error: %s" % e)

# todo support steam pack and uppack
# https://pypi.python.org/pypi/msgpack-python
