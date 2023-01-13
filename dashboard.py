from dash import Dash, dcc, html, no_update
from dash.dependencies import Input, Output, State
import base64, datetime
from enrollment_pie import data_and_chart
import flask
from pageDiv import *

import dash_bootstrap_components as dbc

# https://dashcheatsheet.pythonanywhere.com/
# external_stylesheets = ["assets/upstream.css"]
external_stylesheets = [dbc.themes.MATERIA, dbc.icons.BOOTSTRAP]
# external_stylesheets = []


class ReverseProxied(object):
    # https://web.archive.org/web/20131129080707/http://flask.pocoo.org/snippets/35/

    """Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get("HTTP_X_SCRIPT_NAME", "")
        if script_name:
            environ["SCRIPT_NAME"] = script_name
            path_info = environ["PATH_INFO"]
            if path_info.startswith(script_name):
                environ["PATH_INFO"] = path_info[len(script_name) :]

        scheme = environ.get("HTTP_X_SCHEME", "")
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        return self.app(environ, start_response)


server = flask.Flask(__name__)

server.wsgi_app = ReverseProxied(server.wsgi_app)
# https://community.plotly.com/t/reverse-proxy-not-working-but-works-with-flask/11087/5
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    server=server,
    suppress_callback_exceptions=True,
    routes_pathname_prefix="/",
    requests_pathname_prefix="/pie/",
)
app.title = "Tim ❤ Enrollment Pie"

# buffer = io.StringIO()

app.layout = dbc.Container(
    [
        html.Br(),
        html.Center(
            html.A(
                html.Img(src="/assets/widetim.png", style=logo_style, id="tim"),
                href="/",
            ),
        ),
        tim_banner,
        demo_banner_block,
        upload_block,
        html.Div(
            [],
            id="real_pie",
            style={"width": "100%", "margin": "auto"},
        ),
        html.Br(),
        footer
        # html.A(
        #     html.Button("Download as HTML"),
        #     id="download",
        #     href="data:text/html;base64,",
        #     download="enrollment.html",
        # ),
    ],
)


@app.callback(
    Output("real_pie", "children"),
    Output("upload-data", "style"),
    Output("make_banner", "style"),
    Output("demo_banner", "style"),
    Input("demo", "n_clicks"),
    Input("upload-data", "contents"),
)
def upload_or_example(n_clicks, list_of_contents):
    if list_of_contents:
        return (
            uploaded_chart,
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
        )
    elif n_clicks and n_clicks > 0:
        return (
            example_chart,
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
        )
    return [], no_update, no_update, no_update


@app.callback(
    Output("uploaded_pie", "children"),
    Output("upload_title", "children"),
    Input("dept_or_year_upload", "value"),
    State("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_output(tab, list_of_contents, list_of_names, list_of_dates):
    if list_of_contents:
        if len(list_of_contents) == 1:
            children = [
                parse_contents(c, tab, n, d)
                for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
            ]
            return children[0]
        else:
            return html.H1("Multiple Course/Years Logic Not Implemented Yet")


def parse_contents(contents, tab, filename, date):
    try:
        decoded = base64.b64decode(contents)
        if "classlst" in filename:
            f = decoded.decode(encoding="windows-1252")[24:].split("\n")
        elif "prereg" in filename:
            f = decoded.decode(encoding="windows-1252")[25:].split("\n")
        df, fig, title = data_and_chart(f, dept_or_year=tab)
        # print(df)
        # print(tab)
        # fig.write_html(buffer)
        # html_bytes = buffer.getvalue().encode()
        # encoded = base64.b64encode(html_bytes).decode()
        return (
            dcc.Graph(figure=fig, style={"height": "100%"}),
            title,
        )
    except:
        return (
            no_update,
            "Failed to process the uploaded file. We can only process un-modified `classlst` or `prereg` list from the registrar.",
        )


# @app.callback(
#     Output("tim", "src"),
#     State("upload-data", "last_modified"),
#     Input("upload_pie", "children"),
# )
# def update_tim(a, b):
#     return "assets/long_tim.png"


@app.callback(
    Output("semesterSlider", "marks"),
    Input("courseNumber", "value"),
)
def update_semesters(course):
    import os

    rootDir = "data/" + course
    for folder, subfolders, files in os.walk(rootDir):
        if folder == rootDir:
            break
    ordered = [
        "spring23",
        "fall22",
        "spring22",
        "fall21",
        "spring21",
        "fall20",
        "spring20",
        "fall19",
        "spring19",
    ]
    marks = {}
    idx = 0
    for i in ordered:
        if i in subfolders:
            marks[idx] = i
            idx += 1
    return marks


@app.callback(
    Output("example_pie", "children"),
    Output("example_title", "children"),
    Input("courseNumber", "value"),
    Input("semesterSlider", "value"),
    Input("semesterSlider", "marks"),
    Input("dept_or_year_example", "value"),
)
def show_example(course, value, marks, deptYear):
    # print(marks)
    try:
        term = marks[str(value)]
    except:
        term = marks["0"]
    try:
        base = "data/" + course + "/" + term
        f = base + "/classlst.xls"
        if term == "spring23":
            f = base + "/prereg.xls"
        df, fig, title = data_and_chart(f, dept_or_year=deptYear)
        return (dcc.Graph(figure=fig, style={"height": "100%"}), title)
    except:
        return None, "An error occurred"


# @server.route("/pie/")
# def hello():
#     return flask.redirect("/")


if __name__ == "__main__":
    app.run_server(debug=True)
