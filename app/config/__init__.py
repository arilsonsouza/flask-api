import os
import sys

from dotenv import load_dotenv, find_dotenv

from app.config import config

APP_ENV = os.environ.get('APP_ENV')
APP_ENV = APP_ENV[:1].upper() + APP_ENV[1:].lower()

_current = getattr(sys.modules['app.config.config'], '{0}Config'.format(APP_ENV))()

for attr in [f for f in dir(_current) if not '__' in f]:
    val = os.environ.get(attr, getattr(_current, attr))
    setattr(sys.modules[__name__], attr, val)