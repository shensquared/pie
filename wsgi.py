from dashboard import app
from werkzeug.middleware.proxy_fix import ProxyFix


server = app.server
server.wsgi_app = ProxyFix(server.wsgi_app, x_for=1, x_host=1)
if __name__ == "__main__":
    app.run(APPLICATION_ROOT="/pie")
