from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import base64, datetime
from enrollment_pie import read_into_df, enrollment_chart
import io

external_stylesheets = ["upstream.css"]
external_stylesheets = []
app = Dash(__name__, external_stylesheets=external_stylesheets)
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
        html.H1(
            "hhh",
            id="title",
        ),
        dcc.Tabs(
            id="tabs",
            value="dept",
            children=[
                dcc.Tab(label="By Department", value="dept"),
                dcc.Tab(label="By Year", value="year"),
            ],
        ),
        html.Div(id="tabs-content", style={"width": "100%"}),
        # html.A(
        #     html.Button("Download as HTML"),
        #     id="download",
        #     href="data:text/html;base64,",
        #     download="enrollment.html",
        # ),
    ]
)


@app.callback(
    Output("tabs-content", "children"),
    Input("upload-data", "contents"),
    Input("tabs", "value"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_output(list_of_contents, tab, list_of_names, list_of_dates):
    if list_of_contents is not None:
        # children = [
        #     parse_contents(c, n, d)
        #     for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        # ]
        children, CourseTitle = parse_contents(
            list_of_contents[0], tab, list_of_names[0], list_of_dates[0]
        )
        return children


def parse_contents(contents, tab, filename, date):
    if not filename.startswith("classlst") and not filename.startswith("prereg"):
        return html.Div(
            ["Can only process un-modified classlst or prereg list from the registrar."]
        )
    decoded = base64.b64decode(contents)

    if filename.startswith("classlst"):
        f = decoded.decode(encoding="windows-1252")[24:].split("\n")
    elif filename.startswith("prereg"):
        f = decoded.decode(encoding="windows-1252")[25:].split("\n")
    df, CourseTitle, subTitle = read_into_df(f)
    # print(df)
    # print(tab)
    fig = enrollment_chart(df, dept_or_year=tab)
    fig.write_html(buffer)
    html_bytes = buffer.getvalue().encode()
    encoded = base64.b64encode(html_bytes).decode()
    return dcc.Graph(figure=fig, style={"height": "100%"})


if __name__ == "__main__":
    app.run_server(debug=True)
