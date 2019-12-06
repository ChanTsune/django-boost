from django.http import FileResponse
from django.views.generic import View

from .utils import io_qrcode


class QRCodeGenerateView(View):

    def get(self, request, *args, **kwargs):
        kw = dict(request.GET.items())
        kw = self._clean_kwargs(**kw)
        return FileResponse(streaming_content=io_qrcode(**kw),
                            filename='code.png')

    def _clean_kwargs(self, **kwargs):
        """version=None, error_correction=0, box_size=10, border=4, mask_pattern=None"""
        safe_kwargs = ["text", "version", "error_correction",
                       "box_size", "border", "mask_pattern"]
        cleaned_kwargs = {}
        for key, value in kwargs.items():
            if key in safe_kwargs:
                cleaned_kwargs[key] = value
        if "text" not in cleaned_kwargs.keys():
            cleaned_kwargs["text"] = "Welcol to Django_Boost QR code generator"
        return cleaned_kwargs
