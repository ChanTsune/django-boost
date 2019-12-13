from django_boost.urls.converters import (
    BinIntConverter, BinStrConverter,
    DateConverter,
    HexIntConverter, HexStrConverter,
    OctIntConverter, OctStrConverter,
    register_boost_converters)
from django_boost.urls.static import include_static_files


__all__ = ['UrlSet', 'HexIntConverter', 'HexStrConverter',
           'OctIntConverter', 'OctStrConverter', 'BinIntConverter',
           'BinStrConverter', 'DateConverter', 'register_boost_converters',
           'include_static_files']


class UrlSet:
    """
    Add a namespace to the URL.

    This class does nothing else.

    e.g.

    ```
    class YourModelUrlSet(UrlSet):
        app_name = "YourModel"
        urlpatterns = [
            path('xxx/', ..., name="XXX")
            path('yyy/', ..., name="YYY")
            path('zzz/', ..., name="ZZZ")
        ]

    urlpatterns = [
        path('path/to/model/', include(YourModelUrlSet))
    ]
    ```
    """

    urlpatterns = []
    app_name = ""
    del app_name, urlpatterns
