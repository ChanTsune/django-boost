from django.urls import register_converter

from django_boost.urls.converters.date import DateConverter


class HexConverter:
    regex = '[0-9a-fA-F]+'

    def to_url(self, value):
        if isinstance(value, int):
            return hex(value)[2:]
        return str(value)


class OctConverter:
    regex = '[0-7]+'

    def to_url(self, value):
        if isinstance(value, int):
            return oct(value)[2:]
        return str(value)


class BinConverter:
    regex = '[01]+'

    def to_url(self, value):
        if isinstance(value, int):
            return bin(value)[2:]
        return str(value)


class HexIntConverter(HexConverter):
    def to_python(self, value):
        return int(value, 16)


class OctIntConverter(OctConverter):
    def to_python(self, value):
        return int(value, 8)


class BinIntConverter(BinConverter):
    def to_python(self, value):
        return int(value, 2)


class HexStrConverter(HexConverter):
    def to_python(self, value):
        return value


class OctStrConverter(OctConverter):
    def to_python(self, value):
        return value


class BinStrConverter(BinConverter):
    def to_python(self, value):
        return value


class FloatingPointConverter:
    regex = '[0-9]+([.][0-9]+)?'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)


BOOST_CONVERTERS = {
    'bin': BinIntConverter,
    'oct': OctIntConverter,
    'hex': HexIntConverter,
    'bin_str': BinStrConverter,
    'oct_str': OctStrConverter,
    'hex_str': HexStrConverter,
    'float': FloatingPointConverter,
    'date': DateConverter,
}


def register_boost_converters():
    for name, klass in BOOST_CONVERTERS.items():
        register_converter(klass, name)
