from fastapi import File, Form, Query

from .schema import Checker, Format, Dictionary, SortingStrategy, ResponseType


format_form = Form(
    default=Format.JSON,
    title="Response Format",
    description="Response format: json or text",
)

geometry_form = Form(
    default=False,
    title="GeoJSON Option",
    description=(
        "Return GeoJSON if possible, otherwise return an error message "
        " Option: True or False"
    ),
)

dictionary_form = Form(
    default=Dictionary.None_Given,
    title="Validation Dictionary",
    description="Version of AGS dictionary to validate against",
)

validate_form = Form(
    default=[Checker.ags],
    title="Validation Options",
    description="If set validate against AGS schema",
)

validation_file = File(
    ...,
    title="File to validate",
    description="An AGS file ending in .ags or a ZIP file containing AGS file(s)",
)

conversion_file = File(
    ...,
    title="File to convert",
    description="An AGS, XLSX file or a ZIP file containing AGS and XLSX file(s)",
)

sort_tables_form = Form(
    default=SortingStrategy.default,
    title="Sort worksheets",
    description=(
        "Sort the worksheets into alphabetical, hierarchical "
        "dictionary or default order, that found in the AGS file. "
        "This option is ignored when converting to AGS."
    ),
)

ags_log_query = Query(
    ...,
    title="BGS LOCA ID",
    description="BGS LOCA ID",
    openapi_examples={
        "single borehole": {
            "value": "20190430093402523419",
            "description": "Returns a PDF of borehole log",
        },
        "invalid borehole": {
            "value": "1234567890",
            "description": "Returns a 404 error",
        },
    },
)

ags_export_query = Query(
    ...,
    title="BGS LOCA ID",
    description="A single ID or multiple IDs separated by semicolons",
    openapi_examples={
        "single borehole": {
            "value": "20190430093402523419",
            "description": "Returns a zip file containing the GAS file single borehole log",
        },
        "multiple boreholes": {
            "value": "20190430093402523419;20190430093402523420",
            "description": "TReturns a zip file containing two borehole logs",
        },
        "invalid borehole": {
            "value": "1234567890",
            "description": "Returns a 404 error",
        },
    },
)

polygon_query = Query(
    ...,
    title="POLYGON",
    description="A polygon expressed in Well Known Text",
    openapi_examples={
        "4 boreholes": {
            "value": "POLYGON((-3.946 56.063,-3.640 56.063,-3.640 55.966,-3.946 55.966,-3.946 56.063))",
            "description": "Returns 4 AGS files in a zip file if count is false or not set, "
            "returns a count of 4 if count is true",
        },
        "28 boreholes": {
            "value": "POLYGON((-3.946 56.065,-3.640 56.065,-3.640 55.966,-3.946 55.966,-3.946 56.065))",
            "description": "Returns 28 AGS files in a zip file if count is false or not set, "
            "returns a count of 28 if count is true",
        },
        "No boreholes": {
            "value": "POLYGON((-3.946 56.061,-3.640 56.061,-3.640 55.966,-3.946 55.966,-3.946 56.061))",
            "description": "Returns 422 error with a message if count is false or not set, "
            "returns a count of 0 if count is true",
        },
        "More than 50 boreholes": {
            "value": "POLYGON((-3.109 55.895,-3.109 55.906,-3.077 55.906,-3.077 55.895,-3.109 55.895))",
            "description": "Returns 422 error with a message if count is false or not set, "
            "returns a count of 1952 if count is true",
        },
    },
)

count_only_query = Query(
    default=False,
    title="Return count only",
    description="Return count of found boreholes only",
)

response_type_query = Query(
    default=ResponseType.inline,
    title="PDF Response Type",
    description="PDF response type: inline or attachment",
)
