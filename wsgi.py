from dashboard import app
from werkzeug.middleware.proxy_fix import ProxyFix


from reverse_proxy import FlaskReverseProxied


server = app.server
# server.wsgi_app = ProxyFix(server.wsgi_app, x_for=1, x_host=1)
server = FlaskReverseProxied(server)
if __name__ == "__main__":
    app.run(APPLICATION_ROOT="/pie")
