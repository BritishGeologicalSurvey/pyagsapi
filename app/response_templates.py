# Text templates used to build responses.
from textwrap import dedent

from jinja2 import Template

RESPONSE_TEMPLATE = dedent("""
    File Name: \t {filename}
    File Size: \t {filesize:0.0f} kB
    Time (UTC): \t {time_utc}

    {message}
    """).strip()

PLAIN_TEXT_TEMPLATE = Template("""
{{ filename }}: {{ message }}

# Metadata

File size: {{ filesize }} bytes
Checker: {{ checker }}
{%- if dictionary != '' %}
Dictionary: {{ dictionary }}
{%- endif %}
Time: {{ time }}

{% if not valid -%}
# Errors

{% for key in errors -%}
## {{ key }}

{% for item in errors[key] -%}
{%- if item.line == '-' -%}
Group: {{ item.group }} - {{ item.desc }}
{% else -%}
Line: {{ item.line }} - {{ item.desc }}
{% endif %}
{%- endfor %}
{% endfor %}
{%- endif -%}
""".strip())
