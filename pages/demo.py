from dash import dcc, html, callback, Input, Output, register_page
from enrollment_pie import data_and_chart
from pageDiv import *


register_page(__name__)

layout = html.Div(
    [
        upload_button,
        example_chart,
    ],
)


@callback(
    Output("semesterSlider", "marks"),
    Input("courseNumber", "value"),
)
def update_semesters(course):
    import os

    rootDir = "data/" + course
    for folder, subfolders, files in os.walk(rootDir):
        if folder == rootDir:
            break
    ordered = [
        "spring23",
        "fall22",
        "spring22",
        "fall21",
        "spring21",
        "fall20",
        "spring20",
        "fall19",
        "spring19",
    ]
    marks = {}
    idx = 0
    for i in ordered:
        if i in subfolders:
            marks[idx] = i
            idx += 1
    return marks


@callback(
    Output("example_pie", "children"),
    Output("example_title", "children"),
    Input("courseNumber", "value"),
    Input("semesterSlider", "value"),
    Input("semesterSlider", "marks"),
    Input("dept_or_year_example", "value"),
)
def show_example(course, value, marks, deptYear):
    # print(marks)
    try:
        term = marks[str(value)]
    except:
        term = marks["0"]
    try:
        base = "data/" + course + "/" + term
        f = base + "/classlst.xls"
        if term == "spring23":
            f = base + "/prereg.xls"
        df, fig, title = data_and_chart(f, dept_or_year=deptYear)
        return (dcc.Graph(figure=fig, style={"height": "100%"}), title)
    except:
        return None, "An error occurred"
