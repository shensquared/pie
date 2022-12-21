def enrollment_chart(term, dept_or_year="dept", filename="classlst.xls"):
    term = "fall22"
    # term = "spring23"
    # filenmae = "prereg.xls"
    # If the class isn't active yet the registrar file would be called 'prereg.xls'

    # list = "/Users/shenshen/Codes/000admin/sheets/" + term + "/classlst.xls"
    list = "/Users/shenshen/Codes/3900/000admin/sheets/" + term + "/" + filename
    major_to_dept = {}
    detail_major_list = []
    dept_list = []
    reg_or_can_list = []
    year_list = []

    def group_majors(detail_major):
        if detail_major in major_to_dept:
            major_to_dept[detail_major]
        try:
            major_to_dept[detail_major] = str(int(detail_major))
        except:
            s = detail_major.split(" ")
            for j in s:
                if j != "":
                    if j == "NIH":
                        j = "Harvard"
                    if j == "NIW":
                        j = "Wellesley"
                    major_to_dept[detail_major] = j
                    break
        if major_to_dept[detail_major] == "NONE":
            major_to_dept[detail_major] = "no major"
        return major_to_dept[detail_major]

    def chop_off_white_spaces(s):
        # there must be better way
        # print(s)
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
        if new_s == "NONE" or new_s is None:
            return "no major"
        return new_s

    def year_format(s):
        return "Year " + str(s)

    def reg_cancel_spellout(s):
        if s == "Can":
            return "Cancelled"
        if s == "Reg":
            return "Registered"
        if s == "Lis":
            return "Listener"

    with open(list) as f:
        for (idx, line) in enumerate(f):
            if filename == "prereg.xls" and not line.startswith('"9'):
                continue
            fields = line.split("\t")
            if len(fields) <= 4:
                continue
            detial_major = fields[2]
            if detial_major == "Course" or detial_major.startswith("___"):
                continue
            detail_major_list.append(chop_off_white_spaces(detial_major))
            year_list.append(year_format(fields[3]))
            dept_list.append(group_majors(detial_major))
            reg_or_can_list.append(reg_cancel_spellout(fields[4]))

    import plotly.express as px
    import pandas as pd

    df = pd.DataFrame(
        dict(
            reg_or_can_list=reg_or_can_list,
            detail_major_list=detail_major_list,
            dept_list=dept_list,
            year_list=year_list,
        )
    )
    # print(df)

    if dept_or_year == "dept":
        path = ["reg_or_can_list", "dept_list", "detail_major_list"]
        if term == "spring23":
            path = path[1:]
        # path[1] = ["Registered"] * len(detail_major_list)
        fig = px.sunburst(
            df,
            path=path,
            color="detail_major_list",
            hover_data=["detail_major_list"],
            color_continuous_scale="RdBu",
            width=100
            # color_continuous_midpoint=np.average(df["reg_or_can_list"]),
        )
    else:
        path = ["reg_or_can_list", "year_list", "dept_list", "detail_major_list"]
        if term == "spring23":
            path = path[1:]
        fig = px.sunburst(
            df,
            path=path,
            color="dept_list",
            # hover_data=["detail_major_list"],
            color_continuous_scale="RdBu",
            # color_continuous_midpoint=np.average(df["reg_or_can_list"]),
        )
    fig.update_layout(margin=dict(t=10, l=0, r=0, b=0))
    return fig


if __name__ == "__main__":
    fig.show()
