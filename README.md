# TimPie 🥧

A web-based visualization tool for MIT course enrollment data. Upload registrar enrollment sheets and get interactive sunburst charts showing student distribution by department and year.

![Wide Tim](assets/widetim.png)

## Features

- **Drag & drop upload** - supports `classlst.xls` and `prereg.xls` from the MIT registrar
- **Interactive sunburst charts** - drill down by department or year
- **Privacy-first** - data stays in your browser, nothing is stored on the server
- **Download as HTML** - export standalone interactive charts

## Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install dash dash-bootstrap-components pandas plotly gunicorn chardet

# Run development server
python dashboard.py
```

Visit http://localhost:8050

## Production Deployment

```bash
# Set URL prefix for reverse proxy
URL_PREFIX=/pie/ gunicorn wsgi:app -b 127.0.0.1:4999
```

Example nginx configuration in `config_files/nginx.conf`.

## License

MIT
