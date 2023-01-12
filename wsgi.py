from dashboard import app
from werkzeug.middleware.proxy_fix import ProxyFix

# https://github.com/noirbizarre/flask-restplus/issues/132

# from reverse_proxy import FlaskReverseProxied


server = app.server
server.wsgi_app = ProxyFix(server.wsgi_app, x_proto=1, x_host=1)
# server = FlaskReverseProxied(server)
if __name__ == "__main__":
    app.run()
