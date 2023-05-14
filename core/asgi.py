"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os, sys
from pathlib import Path

from django.core.asgi import get_asgi_application
from chats.middleware import TokenAuthMiddleware  # noqa isort:skip
from core import routing  # noqa isort:skip

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa isort:skip

from django.urls import re_path, path
#import notification


# This allows easy placement of apps within the interior
# py-backend directory.

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "py-backend"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# This application object is used by any ASGI server configured to use this file.
django_application = get_asgi_application()

# Import websocket application here, so apps from django_application are loaded first



application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": TokenAuthMiddleware(URLRouter(routing.websocket_urlpatterns)),
    }
)


    
