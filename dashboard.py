from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import base64, datetime
from enrollment_pie import data_and_chart
import io, flask

external_stylesheets = ["upstream.css"]
# external_stylesheets = []
server = flask.Flask(__name__)
app = Dash(__name__, external_stylesheets=external_stylesheets, server=server)
buffer = io.StringIO()

app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "lineHeight": "100px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "10px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        dcc.Dropdown(["6.390", "6.101"], id="by"),
        dcc.RadioItems(["dept", "year"], "dept", id="dept_or_year", inline=True),
        # dcc.Tabs(
        #     id="tabs",
        #     value="dept",
        #     children=[
        #         dcc.Tab(label="By Department", value="dept"),
        #         dcc.Tab(label="By Year", value="year"),
        #     ],
        # ),
        html.Div(id="tabs-content", style={"width": "100%"}),
        dcc.Slider(min=0, max=20, step=5, value=10, id="my-slider")
        # html.A(
        #     html.Button("Download as HTML"),
        #     id="download",
        #     href="data:text/html;base64,",
        #     download="enrollment.html",
        # ),
    ]
)
app.title = "Tim Enrollment Pie"


@app.callback(
    Output("tabs-content", "children"),
    Input("upload-data", "contents"),
    Input("dept_or_year", "value"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_output(list_of_contents, tab, list_of_names, list_of_dates):
    if list_of_contents and len(list_of_contents) == 1:
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
        df, fig = data_and_chart(f, dept_or_year=tab)
        # print(df)
        # print(tab)
        fig.write_html(buffer)
        html_bytes = buffer.getvalue().encode()
        encoded = base64.b64encode(html_bytes).decode()
        return dcc.Graph(figure=fig, style={"height": "100%"})
    except:
        return html.H1(
            "Failed to process the uploaded file. We can only process un-modified classlst or prereg list from the registrar."
        )


if __name__ == "__main__":
    app.run_server(debug=True)
