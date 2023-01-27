import json
import pandas as pd
import plotly.express as px

maps_json = "data/maps.json"
maps = json.load(open(maps_json))


def read_into_df(file):

    detail_major_list = []
    dept_list = []
    reg_or_can_list = []
    year_list = []

    def group_majors(detail_major):
        try:
            return maps["major_to_dept"][detail_major]
        except:
            print(f"group major {detail_major}")
            s = detail_major.split(" ")
            for j in s:
                if j != "":
                    maps["major_to_dept"][detail_major] = j
                    with open(maps_json, "w") as f:
                        json.dump(maps, f, indent=4, sort_keys=True)
                    return j

    def chop_off_white_spaces(s):
        try:
            return maps["major_without_spaces"][s]
        except:
            print(f"chop off {s}")
            # there must be better way
            left = 0
            right = -1
            for i in range(len(s)):
                if s[i] != " ":
                    left = i
                    break
            # hard code for now
            for j in range(-1, -10, -1):
                if s[j] != " ":
                    right = len(s) + j + 1
                    break
            new_s = s[left:right]
            maps["major_without_spaces"][s] = new_s
            with open(maps_json, "w") as f:
                json.dump(maps, f, indent=4, sort_keys=True)
            return new_s

    def process_f(f):
        CourseTitle = "Sheet has been modified; header title is missing."
        subTitle = ""
        encountered_term = 0
        for (idx, line) in enumerate(f):
            if line.startswith('"Sp') or line.startswith('"Fall'):
                if encountered_term == 1:
                    break
                encountered_term += 1
            if idx == 0:
                line = line.replace('"', "")
                if line.startswith("S") or line.startswith("F"):
                    CourseTitle = line
            elif idx == 1:
                subTitle = line
            elif not line.startswith('"9'):
                continue

            fields = line.split("\t")
            if len(fields) <= 4:
                continue
            detail_major = fields[2]
            if detail_major == "Course" or detail_major.startswith("___"):
                continue
            detail_major = chop_off_white_spaces(detail_major)
            detail_major_list.append(detail_major)
            year_list.append(f"Year {fields[3][1]}")
            dept_list.append(group_majors(detail_major))
            if len(fields[4]) > 2:
                reg_or_can_list.append(maps["reg_can"][fields[4]])
            else:
                reg_or_can_list.append("Pre-registered")
        df = pd.DataFrame(
            dict(
                major=detail_major_list,
                dept=dept_list,
                year=year_list,
            )
        )

        if reg_or_can_list:
            df["reg_status"] = reg_or_can_list
        df["Department"] = df["dept"].map(
            lambda x: maps["CourseNumber_to_Label"].get(str(x), x)
        )
        # df.convert_dtypes
        return df, CourseTitle, subTitle

    if type(file) is list:
        df, CourseTitle, subTitle = process_f(file)
    else:
        with open(file) as f:
            df, CourseTitle, subTitle = process_f(f)

    # df.to_csv(term + "_" + filename.split(".")[0] + ".csv")
    # df.to_csv(CourseTitle + ".csv")
    # print(CourseTitle)
    # print(CourseTitle.split(" "))
    # print(subTitle)
    return df, CourseTitle, subTitle


def enrollment_chart(df, CourseTitle="", dept_or_year="dept"):
    if dept_or_year == "dept":
        path = ["reg_status", "dept", "major"]
    elif dept_or_year == "year":
        path = ["reg_status", "dept", "year"]
    if "reg_status" not in df.columns:
        path = path[1:]
    fig = px.sunburst(
        df,
        path=path,
        color="major",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hover_name="Department",
        custom_data=["Department"]
        # hover_data=["major"],
        # hover_data={"labels": False, "major": True},
        # color_continuous_scale="RdBu",
        # color_discrete_map={"Pre-registerd": "#C2C0BF"},
    )
    fig.update_traces(
        hovertemplate="%{customdata[0]}<br>Count: %{value} <extra></extra>",
    )
    # fig.update_traces(textinfo="label+percent entry+percent parent+value")
    fig.update_traces(textinfo="label+value")
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    # fig.update_layout(
    #     title={
    #         "text": CourseTitle,
    #         "y": 0.9,
    #         "x": 0.5,
    #         "xanchor": "center",
    #         "yanchor": "top",
    #     }
    # )

    # print(fig.data[0])
    return fig


def data_and_chart(f, dept_or_year="dept"):
    df, CourseTitle, subTitle = read_into_df(f)
    fig = enrollment_chart(df, CourseTitle=CourseTitle, dept_or_year=dept_or_year)
    return df, fig, CourseTitle


if __name__ == "__main__":
    base = "/Users/shenshen/Codes/courseAdmin/sheets/"
    term = "spring23"
    filename = "prereg.xls"
    file = base + term + "/" + filename
    # df, CourseTitle, subTitle = read_into_df(file)
    # fig = enrollment_chart(df, CourseTitle)
    df, fig, CourseTitle = data_and_chart(file)

    fig.show()
