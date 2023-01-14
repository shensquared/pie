from dash import html, dcc
import json
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
                    # width=11,
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
                            """Uploaded sheet is stored **only** in your browser memory; i.e., it evaporates 👻 once your tab is refreshed.""",
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

demo_banner_block = html.Center(
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button(
                            "(demo) for a taste",
                            color="primary",
                            className="me-1",
                            id="demo",
                        ),
                        dbc.Popover(
                            html.H6("of some half-baked pie"),
                            target="demo",
                            body=True,
                            trigger="hover",
                        ),
                    ]
                    # width=1
                    # width={"size": 1, "offset": 3, "order": "first"},
                ),
                # dbc.Col(
                #     [
                #         dcc.Markdown(
                #             "click & hover over slices for a taste of some (half-baked) pie",
                #         ),
                #     ],
                #     width=6
                #     # width={
                #     # "size": 8,
                #     # },
                # ),
            ],
            align="center",
            id="demo_banner",
        ),
        # html.Br(),
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
                    "Select course",
                    dcc.Dropdown(
                        ["demo1", "demo2", "demo3"], value="demo1", id="courseNumber"
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

footer = html.Footer(
    [
        html.Br(),
        html.Center(
            dbc.Row(
                [
                    # dbc.Col(html.P(), width=5),
                    dbc.Col(
                        [
                            dcc.Markdown(
                                """
                                Made with ❤️ by [$\\text{Shen}^2$](https://shenshen.mit.edu)
                                """,
                                mathjax=True,
                            ),
                        ],
                        # className="d-flex align-items-center",
                        # width=6,
                    ),
                    # dbc.Col(
                    #     # dcc.Markdown(
                    #     #     "[Bug report/feature request]()"
                    #     # ),
                    #     html.I(
                    #         className="bi bi-github large",
                    #         href="https://github.com/shensquared/timPie",
                    #     ),
                    #     # style={"float": "right"},
                    #     width=1,
                    # ),
                ]
            )
        ),
    ]
)
