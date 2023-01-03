from dash import Dash, dcc, html, no_update
from dash.dependencies import Input, Output, State
import base64, datetime
from enrollment_pie import data_and_chart
import io, flask
from pageDiv import *


external_stylesheets = ["assets/upstream.css"]
server = flask.Flask(__name__)
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    server=server,
    suppress_callback_exceptions=True,
)
app.title = "Tim ❤ Enrollment Pie"

# buffer = io.StringIO()

app.layout = html.Div(
    [
        tim_banner,
        upload_block,
        html.Br(),
        html.Div(
            [demo_banner_block],
            id="real_pie",
            style={"width": "100%", "margin": "auto"},
        ),
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
    Input("demo", "n_clicks"),
    Input("upload-data", "contents"),
)
def upload_or_example(n_clicks, list_of_contents):
    if list_of_contents:
        return (uploaded_chart, {"display": "none"})
    elif n_clicks and n_clicks > 0:
        return example_chart, no_update
    return demo_banner_block, no_update


@app.callback(
    Output("uploaded_pie", "children"),
    Output("topBanner", "children"),
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
            "### " + title,
        )
    except:
        return (
            no_update,
            "Failed to process the uploaded file. We can only process un-modified `classlst` or `prereg` list from the registrar.",
        )


if __name__ == "__main__":
    app.run_server(debug=True)
