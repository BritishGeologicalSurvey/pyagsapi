# Text templates used to build responses.
from jinja2 import Template

PLAIN_TEXT_TEMPLATE = Template("""
{{ filename }}: {{ message }}

# Metadata

File size: {{ filesize }} bytes
{%- if checkers != [] %}
Checkers: {{ checkers }}
{%- endif %}
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
