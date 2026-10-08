
from config.app import app, templates, Request, JSONResponse
from starlette.exceptions import HTTPException as NotFoundException

@app.exception_handler(NotFoundException)
async def http_exception_handler(request: Request, exc: NotFoundException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            request=request,
            name = 'pages/error/notfound.html',
            context={'request': request},
            status_code=404
        )
    return JSONResponse(
         status_code=exc.status_code,
        content={"detail": exc.detail},
    )

