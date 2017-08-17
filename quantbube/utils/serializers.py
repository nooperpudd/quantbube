# encoding:utf-8
import abc
import datetime
import decimal

import msgpack
from dateutil import parser


class MsgPackParseError(Exception):
    """
    MessagePack parse error
    """
    pass


class SerializerValidateError(Exception):
    """
    Validate the parsed data error
    """
    pass


class BaseSerializer(metaclass=abc.ABCMeta):
    """
    The base serializer class,
    only defines the signature for loads and dumps
    """
    def __init__(self, schema=None):
        """
        :param schema:
        """
        self.schema = schema

    def validate(self, data, *args, **kwargs):
        """
        validate the dumps of data is valid or not
        :return:bool
        """
        raise NotImplementedError()

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
        return parser.parse(obj["str"])

    def decode_date(self, obj):
        return parser.parse(obj["str"]).date()

    def decode_time(self, obj):
        return parser.parse(obj["str"]).time()

    def decode_decimal(self, obj):
        return decimal.Decimal(obj["str"])


class MsgPackEncoder(object):
    """
    encode the data type to the message pack format
    """

    def encode(self, obj):
        """
        :param obj:
        :return:
        """
        if type(obj) is datetime.date:
            return {"__class__": "date", "str": obj.isoformat()}
        elif type(obj) is datetime.datetime:
            return {"__class__": "datetime", "str": obj.isoformat()}
        elif type(obj) is datetime.time:
            return {"__class__": "time", "str": obj.isoformat()}
        elif isinstance(obj, decimal.Decimal):
            return {"__class__": "decimal", "str": str(obj)}
        else:
            return obj


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
            raise MsgPackParseError("MessagePack loads error: %s" % e)

    def dumps(self, data, *args, **kwargs):
        """
        :param data:
        :return:
        """
        try:
            return msgpack.packb(data, encoding="utf-8", default=MsgPackEncoder().encode, **kwargs)
        except Exception as e:
            raise MsgPackParseError("MessagePack dumps error: %s" % e)