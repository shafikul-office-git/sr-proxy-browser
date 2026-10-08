
from config.app import app, templates, os, HTMLResponse, Request

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/public/index.html",
        context={"request": request, "version": os.getenv("APP_VERSION")}
    )

