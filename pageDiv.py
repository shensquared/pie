from dash import html, dcc
import json
import dash_bootstrap_components as dbc

div_paras = json.load(open("div.json"))

logo_style = {
    "height": "100px",
}
tim_banner = html.Center(
    [
        html.A(
            html.Img(src="assets/widetim.png", style=logo_style, id="tim"), href="/"
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Markdown(
                        """#### ❤️ make wide tim some pie 🥧 with the registrar enrollment sheets...""",
                        id="topBanner",
                    ),
                    width=11,
                ),
                dbc.Col(
                    dbc.Button(
                        "A taste of (half-baked) pie",
                        outline=True,
                        color="secondary",
                        className="me-1",
                        id="demo",
                    ),
                    # width=1,
                ),
            ],
            justify="center",
        ),
    ],
)

upload_block = dcc.Upload(
    id="upload-data",
    children=html.Div(
        [
            html.Br(),
            dcc.Markdown(
                [
                    """ ###### Support `classlst.xls` and `prereg.xls`.""",
                    """###### Drag/Drop sheets into the box, or click the box to select files""",
                    """Uploaded is stored **only** in your current browser session; i.e., it evaporates once the tab is refreshed.""",
                ],
                style={
                    "width": "90%",
                    "lineHeight": "30px",
                    "borderWidth": "1.5px",
                    "borderStyle": "dashed",
                    "borderRadius": "15px",
                    "textAlign": "center",
                    "margin": "auto",
                },
            ),
        ],
        style={
            "width": "90%",
            "lineHeight": "30px",
            "textAlign": "center",
            "margin": "auto",
            "paddingTop": "20px",
            "paddingBottom": "20px",
        },
    ),
    multiple=True,
    style={
        "width": "90%",
        "textAlign": "center",
        "margin": "auto",
        "display": "flex",
        "flexDirection": "row",
    },
)

# demo_banner_block = dbc.Row(
#     [
#         dbc.Col(
#             dcc.Markdown("""######  before uploading your own sheet..."""),
#             width=5,
#         ),
#         dbc.Col(
#             dbc.Button(
#                 "A taste of (half-baked) demo pie",
#                 id="demo",
#                 style={"marginLeft": "20px"},
#             ),
#             width=3,
#         ),
#     ],
#     justify="center",
#     id="demo_banner",
# )

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
        pie_controls,
        html.Br(),
        html.Div(
            id="example_pie",
            style={"width": "100%", "height": "700px", "display": "block"},
        ),
    ]
)

uploaded_chart = html.Div(
    [
        html.Center(dept_or_year_upload),
        html.Div(
            id="uploaded_pie",
            style={
                "width": "100%",
            },
        ),
    ],
    id="uploaded_chart",
)
