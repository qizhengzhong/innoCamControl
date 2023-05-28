from channels.routing import ProtocolTypeRouter, URLRouter
import channels.staticfiles
from channels.auth import AuthMiddlewareStack
import data.routing


application = ProtocolTypeRouter({
        'websocket': AuthMiddlewareStack(
            URLRouter(
                data.routing.websocket_urlpatterns
            )
        ),
    })
