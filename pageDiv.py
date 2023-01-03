from dash import html, dcc
import json

div_paras = json.load(open("div.json"))

logo_style = {
    "height": "77%",
}
tim_banner = html.Center(
    [
        html.Img(src="assets/widetim.png", style=logo_style),
        html.Div(
            [
                dcc.Markdown("""### ❤️ Make Wide Tim Some Pie 🥧"""),
                dcc.Markdown("""##### with the registrar enrollment sheets..."""),
            ],
            style={
                # "float": "left",
                "textAlign": "center",
            },
        ),
    ],
    style={
        "height": "137px",
        "verticalAlign": "top",
        "textAlign": "center",
        "display": "flex",
        "flexDirection": "row",
        "width": "30%",
        "margin": "auto",
        "float": "center",
    },
)

upload_block = dcc.Upload(
    id="upload-data",
    children=html.Div(
        [
            dcc.Markdown(
                """(Support both `classlst.xls` and `prereg.xls`. Uploaded data is stored in your current browser session **only** and does not stay on the server.)"""
            ),
            "Drag/Drop Sheets or ",
            html.A("Select Files"),
        ],
        style={
            "width": "90%",
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
        "lineHeight": "30px",
        "borderWidth": "1.5px",
        "borderStyle": "dashed",
        "borderRadius": "15px",
        "textAlign": "center",
        "margin": "auto",
        "display": "flex",
        "flexDirection": "row",
    },
)

demo_banner_block = html.Center(
    [
        "Or, get a taste of the pie without uploading your own sheet...",
        html.Button("see an example", id="demo", style={"marginLeft": "20px"}),
    ],
    id="demo_banner",
)

dept_or_year_upload = html.Div(
    [
        "Slice the last pie by",
        dcc.RadioItems(
            ["dept", "year"],
            value="dept",
            id="dept_or_year_upload",
            inline=True,
            # labelStyle={"display": "block"},
            style={"paddingTop": "10px"},
        ),
    ],
)

dept_or_year_example = html.Div(
    [
        "Slice the last pie by",
        dcc.RadioItems(
            ["dept", "year"],
            value="dept",
            id="dept_or_year_example",
            inline=True,
            # labelStyle={"display": "block"},
            style={"paddingTop": "10px"},
        ),
    ],
    style={"float": "left"},
)


pie_controls = html.Div(
    [
        html.Div(
            [
                "Select a demo course",
                dcc.Dropdown(
                    list(div_paras.keys())[:-1], value="Demo", id="courseNumber"
                ),
            ],
            style={"width": "28%", "float": "left"},
        ),
        html.Div(
            style={"width": "10%", "float": "left"},
        ),
        html.Div(
            [
                "Semester",
                dcc.Slider(
                    min=0,
                    max=4,
                    step=1,
                    value=0,
                    id="semesterSlider",
                ),
            ],
            style={"width": "33%", "float": "left"},
        ),
        html.Div(
            style={"width": "10%", "float": "left"},
        ),
        dept_or_year_example,
    ],
    style={
        "display": "flex",
        "flexDirection": "row",
        "width": "77%",
        "margin": "auto",
    },
    id="courseTermController",
)

example_chart = html.Div(
    [
        pie_controls,
        html.Div(
            id="example_pies",
            style={"width": "100%", "margin": "auto"},
        ),
    ]
)

uploaded_chart = html.Div(
    [
        dept_or_year_upload,
        html.Div(
            id="uploaded_pie",
            style={"width": "100%"},
        ),
    ],
    id="uploaded_chart",
)
