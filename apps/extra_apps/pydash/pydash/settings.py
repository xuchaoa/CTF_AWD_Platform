from django.conf import settings

# All of the refresh values are in miliseconds, 1 second = 1000 miliseconds
# Adjust accordingly as you wish, preferably in your application's settings.py.
TIME_JS_REFRESH = getattr(settings, 'TIME_JS_REFRESH', 30000)
TIME_JS_REFRESH_LONG = getattr(settings, 'TIME_JS_REFRESH_LONG', 120000)
TIME_JS_REFRESH_NET = getattr(settings, 'TIME_JS_REFRESH_NET', 2000)
_VERSION = '1.4.4'
