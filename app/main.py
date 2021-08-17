from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app import routes

app = FastAPI()

# Add routes
app.include_router(routes.router)


@app.get("/")
async def main():
    content = """
<!DOCTYPE html>
<html>
<head>
<title>AGS File Validator</title>
</head>
<body>
<h1>AGS File Validator</h1>
<br>
<h2>AGS File Size</h2>
<form action="/validate/" enctype="multipart/form-data" method="post">
<input name="file" type="file" multiple>
<input type="submit">
</form>
<br>
<h2>AGS File Name</h2>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
</html>
    """
    return HTMLResponse(content=content)
