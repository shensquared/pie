from dash import html, dcc
import json

div_paras = json.load(open("div.json"))

logo_style = {
    "height": "100px",
}
tim_banner = html.Center(
    [
        html.A(
            html.Img(src="assets/widetim.png", style=logo_style, id="tim"), href="/"
        ),
        html.Div(
            [
                dcc.Markdown(
                    """#### ❤️ make wide tim some pie 🥧 with the registrar enrollment sheets...""",
                    id="topBanner",
                ),
                # dcc.Markdown("""##### with the registrar enrollment sheets..."""),
            ],
            # style={
            #     # "float": "left",
            #     # "textAlign": "center",
            # },
        ),
    ],
    style={
        # "height": "137px",
        # "verticalAlign": "top",
        # "textAlign": "center",
        # "display": "flex",
        # "flexDirection": "row",
        # "width": "30%",
        # "margin": "auto",
        # "float": "center",
    },
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
                    # """# Click WideTim to refresh""",
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
            # "Drag/Drop the sheets or ",
            # html.A("Select Files"),
        ],
        style={
            "width": "80%",
            "lineHeight": "30px",
            # "borderWidth": "1.5px",
            # "borderStyle": "dashed",
            # "borderRadius": "15px",
            "textAlign": "center",
            "margin": "auto",
            "paddingTop": "20px",
            "paddingBottom": "20px",
        },
    ),
    multiple=True,
    style={
        "width": "77%",
        "textAlign": "center",
        "margin": "auto",
        "display": "flex",
        "flexDirection": "row",
    },
)

demo_banner_block = html.Center(
    [
        dcc.Markdown(
            """###### Or, get a taste of the **interactive** pie without uploading your own sheet..."""
        ),
        html.Button(
            "some half-baked examples", id="demo", style={"marginLeft": "20px"}
        ),
    ],
    id="demo_banner",
)

dept_or_year_upload = html.Div(
    [
        "Slice the pie crust by",
        dcc.RadioItems(
            ["dept", "year"],
            value="dept",
            id="dept_or_year_upload",
            inline=True,
            # labelStyle={"display": "block"},
            # style={"paddingTop": "10px"},
        ),
    ],
)

dept_or_year_example = html.Div(
    [
        "Slice the pie crust by",
        dcc.RadioItems(
            ["dept", "year"],
            value="dept",
            id="dept_or_year_example",
            inline=True,
            # labelStyle={"display": "block"},
            style={"paddingTop": "10px"},
        ),
    ],
)


pie_controls = html.Center(
    [
        html.Div(
            [
                "Select a demo course",
                dcc.Dropdown(
                    list(div_paras.keys())[:-1], value="6.390", id="courseNumber"
                ),
            ],
            # style={"margin": "auto", "width": "30%"},
        ),
        html.Div(
            style={"width": "5%", "float": "left"},
        ),
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
            style={
                "width": "50%",
            },
        ),
        html.Div(
            style={"width": "5%", "float": "left"},
        ),
        dept_or_year_example,
    ],
    style={
        "display": "flex",
        "flexDirection": "row",
        "width": "77%",
        "margin": "auto",
        "paddingBottom": "10px",
    },
    # className="justify-content-center",
    id="courseTermController",
)

example_chart = html.Div(
    [
        pie_controls,
        html.Div(
            id="example_pie",
            style={"width": "100%"},
        ),
    ]
)

uploaded_chart = html.Div(
    [
        html.Center(dept_or_year_upload),
        html.Div(
            id="uploaded_pie",
            style={"width": "100%"},
        ),
    ],
    id="uploaded_chart",
    # style={"display": "flex", "flex-direction": "row"},
)
