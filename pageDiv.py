from dash import html, dcc
import json
import dash_bootstrap_components as dbc

div_paras = json.load(open("div.json"))

logo_style = {
    "height": "100px",
}
tim_banner = html.Center(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Markdown(
                        """#### ❤️ make wide tim some pie 🥧 with the registrar enrollment sheets...""",
                    ),
                    width=11,
                ),
            ],
        ),
    ],
    id="make_banner",
)

upload_block = html.Center(
    dcc.Upload(
        id="upload-data",
        children=html.Div(
            [
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                dcc.Markdown(
                    [
                        """ ###### Support `classlst.xls` and `prereg.xls`.""",
                        """###### Drag/Drop sheets into this box, or click this box to select files""",
                        """Uploaded is stored **only** in your current browser session; i.e., it evaporates 👻 once the tab is refreshed.""",
                    ],
                ),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
            ],
            style={
                "width": "90%",
                "lineHeight": "30px",
                "borderStyle": "dashed",
                "borderWidth": "2px",
                "textAlign": "center",
                "margin": "auto",
                "borderRadius": "15px",
                "paddingTop": "20px",
                "paddingBottom": "20px",
            },
        ),
        multiple=True,
    )
)

demo_banner_block = dbc.Row(
    [
        dbc.Col(
            dbc.Button(
                "A taste of some (half-baked) pie",
                color="primary",
                className="me-1",
                id="demo",
            ),
            width={"size": 3, "offset": 3, "order": "first"},
        ),
        dbc.Col(
            dcc.Markdown(
                """feel free to click/hover around. [Bug report/feature request](https://github.com/shensquared/timPie)"""
            ),
            width={
                "size": 3,
            },
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
    ],
    align="center",
    id="demo_banner",
)

dept_or_year_upload = html.Div(
    [
        "Slice the pie crust by",
        dbc.RadioItems(
            options=["dept", "year"],
            value="dept",
            id="dept_or_year_upload",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
        ),
    ],
)

dept_or_year_example = html.Div(
    [
        "Slice the pie crust by",
        dbc.RadioItems(
            options=["dept", "year"],
            value="dept",
            id="dept_or_year_example",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
        ),
    ],
)


pie_controls = dbc.Row(
    [
        dbc.Col(
            html.Div(
                [
                    "Select a demo course",
                    dcc.Dropdown(
                        list(div_paras.keys())[:-1], value="6.390", id="courseNumber"
                    ),
                ],
            ),
            width=2,
        ),
        dbc.Col(
            width=1,
        ),
        dbc.Col(
            html.Div(
                [
                    "Semester",
                    dcc.Slider(
                        step=1,
                        value=1,
                        id="semesterSlider",
                        marks=None,
                    ),
                ],
            ),
            width=5,
        ),
        dbc.Col(
            width=1,
        ),
        dbc.Col(dept_or_year_example),
    ],
    className="align-items-md-stretch",
    id="courseTermController",
)

example_chart = html.Div(
    [
        html.Br(),
        html.Center(
            html.H3("", id="example_title"),
        ),
        pie_controls,
        html.Br(),
        html.Div(
            id="example_pie",
            style={"height": "700px"},
        ),
    ]
)

uploaded_chart = html.Div(
    [
        html.Center(
            html.H3("", id="upload_title"),
        ),
        dbc.Col(html.Center(dept_or_year_upload)),
        html.Br(),
        dbc.Col(
            html.Div(
                id="uploaded_pie",
                style={"height": "700px"},
            ),
        ),
    ],
    id="uploaded_chart",
)
