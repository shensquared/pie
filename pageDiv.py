from dash import html, dcc
import json

div_paras = json.load(open("div.json"))

logo_style = {
    "height": "77%",
    "float": "left",
    "padding-left": "20px",
    "padding-top": "0px",
    "padding-right": "30px",
}
tim_banner = html.Div(
    [
        html.Img(src="assets/widetim.png", style=logo_style),
        html.Div(
            [
                dcc.Markdown("""### ❤️ Feed Wide Tim Some Pie 🥧"""),
                dcc.Markdown("""##### with the registrar enrollment sheets..."""),
                # html.Div(
                #     [
                #         "Drag and Drop or ",
                #         html.A("Select Files"),
                #     ],
                #     style={
                #         "width": "90%",
                #         "lineHeight": "30px",
                #         "borderWidth": "1.5px",
                #         "borderStyle": "dashed",
                #         "borderRadius": "15px",
                #         "textAlign": "center",
                #         "margin": "20px",
                #         "padding-left": "77px",
                #     },
                # ),
            ]
        ),
    ],
    style={
        "width": "90%",
        "lineHeight": "20px",
        "height": "139px",
        "float": "right",
        # "textAlign": "center",
        "margin": "auto",
        # "padding-left": "77px",
    },
)

upload_block = dcc.Upload(
    id="upload-data",
    children=html.Div(
        [
            dcc.Markdown(
                """(Support both `classlst.xls` and `prereg.xls`. Uploaded data is stored in your current browser session **only** and does not stay on the server.)"""
            ),
            "Drag and Drop or ",
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
            "padding-top": "20px",
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
        html.Div(
            [
                "Last pie slice by",
                dcc.RadioItems(
                    options=[
                        dict(label="by dept", value="dept"),
                        dict(label="by class year", value="year"),
                    ],
                    value="dept",
                    id="dept_or_year",
                    inline=True,
                    # labelStyle={"display": "block"},
                    style={"padding-top": "10px"},
                ),
            ],
            style={"float": "left"},
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "row",
        "width": "77%",
        "margin": "auto",
    },
)
