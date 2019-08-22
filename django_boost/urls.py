class UrlSet(object):
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
