from base64 import b64encode
from io import BytesIO


def bytes_qrcode(text, **kwargs):
    from qrcode import QRCode
    qr = QRCode(**kwargs)
    qr.add_data(text)
    qr.make()
    image = qr.make_image()
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def io_qrcode(text, **kwargs):
    return BytesIO(bytes_qrcode(text, **kwargs))


def base64_bytes_qrcode(text, **kwargs):
    byte_image = bytes_qrcode(text, **kwargs)
    return b64encode(byte_image)


def base64_string_qrcode(text, **kwargs):
    return base64_bytes_qrcode(text, **kwargs).decode()
