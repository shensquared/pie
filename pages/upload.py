from dash import Dash, dcc, html, no_update, register_page, callback
from dash.dependencies import Input, Output, State
import base64, datetime
from enrollment_pie import data_and_chart
from pageDiv import *
import plotly.graph_objects as go
import io

register_page(__name__, path="/", title="Tim ❤ Enrollment Pie")

layout = html.Div(
    [
        tim_banner,
        demo_banner_block,
        upload_block,
        html.Div(
            [],
            id="real_pie",
            style={"width": "100%", "margin": "auto"},
        ),
    ],
)


@callback(
    Output("real_pie", "children"),
    Output("upload-data", "style"),
    Output("make_banner", "style"),
    Output("demo_banner", "style"),
    Input("upload-data", "contents"),
)
def upload_or_example(list_of_contents):
    if list_of_contents:
        return (
            uploaded_chart,
            {"display": "none"},
            {"display": "none"},
            {"display": "none"},
        )
    return [], no_update, no_update, no_update


@callback(
    Output("uploaded_pie", "children"),
    Output("upload_title", "children"),
    Output("download-chart", "href"),
    Output("download-chart", "style"),
    Input("dept_or_year_upload", "value"),
    State("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_output(tab, list_of_contents, list_of_names, list_of_dates):
    if list_of_contents:
        if len(list_of_contents) == 1:
            children = [
                parse_contents(c, tab, n, d)
                for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
            ]
            chart_component, title, download_href, download_style = children[0]
            
            return chart_component, title, download_href, download_style
        else:
            return html.H1("Multiple Course/Years Logic Not Implemented Yet"), "", "", {"display": "none"}
    
    return no_update, no_update, "", {"display": "none"}


def parse_contents(contents, tab, filename, date):
    try:
        decoded = base64.b64decode(contents)
        if "classlst" in filename:
            f = decoded.decode(encoding="windows-1252")[24:].split("\n")
        elif "prereg" in filename:
            f = decoded.decode(encoding="windows-1252")[25:].split("\n")
        
        # Generate both dept and year views
        df_dept, fig_dept, title_dept = data_and_chart(f, dept_or_year="dept")
        df_year, fig_year, title_year = data_and_chart(f, dept_or_year="year")
        
        # Use the current selection for the initial title
        current_title = title_dept if tab == "dept" else title_year
        
        # Read the wide tim logo base64 from file
        try:
            with open("assets/widetim_base64.txt", "r") as logo_file:
                widetim_base64 = logo_file.read().strip()
        except FileNotFoundError:
            widetim_base64 = ""  # Fallback if file not found
        
        # Generate HTML content for download with interactive buttons
        html_buffer = io.StringIO()
        
        # Create a custom HTML template with interactive buttons
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>Tim ❤ Enrollment Pie - {current_title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ font-family: 'Roboto', Arial, sans-serif; background: #f8f9fa; margin: 0; padding: 20px; }}
        .logo {{ width: 120px; display: block; margin: 0 auto 20px auto; }}
        .title {{ text-align: center; font-size: 2em; margin: 10px 0; color: #333; }}
        .controls {{ text-align: center; margin-bottom: 20px; }}
        .button-group {{ display: inline-flex; border-radius: 5px; overflow: hidden; border: 1px solid #ddd; }}
        .btn {{ padding: 8px 16px; border: none; background: #f8f9fa; color: #666; cursor: pointer; }}
        .btn.active {{ background: #007bff; color: white; }}
        .btn:first-child {{ border-radius: 5px 0 0 5px; }}
        .btn:last-child {{ border-radius: 0 5px 5px 0; }}
        .chart-container {{ width: 100%; height: 700px; margin: 0 auto; background: #f8f9fa !important; }}
        #chart {{ background: #f8f9fa !important; }}
        .js-plotly-plot {{ background: #f8f9fa !important; }}
        .footer {{ text-align: center; margin-top: 30px; color: #666; }}
        .footer a {{ color: #007bff; text-decoration: none; }}
        .footer a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    {f'<img class="logo" src="data:image/png;base64,{widetim_base64}" alt="Wide Tim Logo">' if widetim_base64 else ''}
    <div class="title" id="chart-title">{current_title}</div>
    <div class="controls">
        <div class="button-group">
            <button class="btn {'active' if tab == 'dept' else ''}" onclick="switchView('dept')">Department</button>
            <button class="btn {'active' if tab == 'year' else ''}" onclick="switchView('year')">Year</button>
        </div>
    </div>
    <div class="chart-container">
        <div id="chart" style="width: 100%; height: 700px; background: #f8f9fa;"></div>
    </div>

    <footer class="footer">
        <br>
        Made with ❤️ by <a href="https://shenshen.mit.edu" target="_blank">Shen²</a>
    </footer>

    <script>
        // Store both chart configurations
        const deptChart = {fig_dept.to_json()};
        const yearChart = {fig_year.to_json()};
        
        // Initialize with current view
        let currentView = '{tab}';
        
        // Function to switch between views
        function switchView(view) {{
            currentView = view;
            
            // Update button states
            document.querySelectorAll('.btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Update chart with background settings
            const chartData = view === 'dept' ? deptChart : yearChart;
            const layout = {{
                ...chartData.layout,
                paper_bgcolor: '#f8f9fa',
                plot_bgcolor: '#f8f9fa'
            }};
            Plotly.newPlot('chart', chartData.data, layout, {{width: null, height: 700}});
            
            // Update title
            const title = view === 'dept' ? '{title_dept}' : '{title_year}';
            document.getElementById('chart-title').textContent = title;
        }}
        
        // Initialize chart
        window.onload = function() {{
            const initialChart = currentView === 'dept' ? deptChart : yearChart;
            const layout = {{
                ...initialChart.layout,
                paper_bgcolor: '#f8f9fa',
                plot_bgcolor: '#f8f9fa'
            }};
            Plotly.newPlot('chart', initialChart.data, layout, {{width: null, height: 700}});
        }};
    </script>
</body>
</html>
"""
        
        # Write the HTML to the buffer
        html_buffer.write(html_template)
        html_content = html_buffer.getvalue()
        
        # Encode the HTML content for download
        encoded_html = base64.b64encode(html_content.encode()).decode()
        download_link = f"data:text/html;base64,{encoded_html}"
        
        # Return the current view for display
        current_fig = fig_dept if tab == "dept" else fig_year
        
        return [
            dcc.Graph(figure=current_fig, style={"width": "100%", "height": "700px", "margin": "auto"}),
            current_title,
            download_link,
            {"display": "block"}
        ]
    except Exception as e:
        print(e)
        return [
            html.Div(
                [
                    html.H3("There was an error processing this file."),
                    html.P(str(e)),
                ]
            ),
            f"Error processing file: {filename}",
            "",
            {"display": "none"}
        ]
