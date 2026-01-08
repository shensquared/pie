from dash import html, dcc
import dash_bootstrap_components as dbc


logo_style = {
    "height": "100px",
}
tim_banner = html.Center(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Markdown(
                        """#### ❤️ make wide tim some pie 🥧 with the registrar enrollment sheets 📜""",
                    ),
                ),
            ],
        ),
    ],
    id="make_banner",
)

upload_block = html.Center(
    [
        html.Br(),
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
                            """###### Drag & Drop or Click""",
                            """###### Support `classlst.xls` or `prereg.xls`""",
                            """The data is stored **only** in your browser memory; i.e., it evaporates 👻 once your tab is refreshed.""",
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
        ),
    ]
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
    style={"display": "flex", "alignItems": "center", "justifyContent": "center", "gap": "10px"},
)

uploaded_chart = html.Div(
    [
        html.Center(
            html.H3(id="upload_title"),
        ),
        html.Center(dept_or_year_upload),
        html.Div(
            id="uploaded_pie",
            style={"height": "700px", "marginTop": "10px"},
        ),
        html.Br(),
        html.Center(
            html.A(
                html.Button("Download as HTML", className="btn btn-primary"),
                id="download-chart",
                href="",
                download="enrollment_chart.html",
                style={"display": "none"},
            ),
        ),
    ],
    id="uploaded_chart",
    style={"marginTop": "-5rem"},
)


footer = html.Footer(
    [
        html.Br(),
        html.Center(
            html.Div(
                [
                    html.Span("made with ❤️ by "),
                    html.A("shensquared", href="https://shenshen.mit.edu", target="_blank"),
                    html.Span(" · "),
                    html.A(
                        html.Img(src="assets/github.svg", style={"height": "20px", "verticalAlign": "middle"}),
                        href="https://github.com/shensquared/pie",
                        target="_blank",
                    ),
                ],
                style={"display": "inline-flex", "alignItems": "center", "gap": "4px"},
            )
        ),
    ]
)
