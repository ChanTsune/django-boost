from django.views.generic import View
from django.http import FileResponse

from .utils import base64_bytes_qrcode

class QRCodeGenerateView(View):

    def get(self, request, *args, **kwargs):

        return FileResponse(base64_bytes_qrcode("QR"),filename='')

    def _clean_kwargs(self, **kwargs):
        """version=None, error_correction=0, box_size=10, border=4, image_factory=None, mask_pattern=None"""
