from base64 import b64encode
from io import BytesIO

from qrcode import QRCode


def bytes_qrcode(data):
    qr = QRCode()
    qr.add_data(data)
    qr.make()
    image = qr.make_image()
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def base64_bytes_qrcode(data, level=None):
    byte_image = bytes_qrcode(data)
    return b64encode(byte_image)


def base64_string_qrcode(data):
    return base64_bytes_qrcode(data).decode()
