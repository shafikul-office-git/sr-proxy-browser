
import uvicorn
from config.app import app, RedirectResponse, Request

# =================================
# ADD API route 
# =================================
from router.api import users

app.include_router(users.router)

# =================================
# ADD WEB route 
# =================================
from router.web import public
from router.web import auth
from router.web import error

# ======================
#  session or authention debug korar jonno
# ======================
@app.get("/debug")
async def debug(request: Request):
    return {
        "has_session_attr": hasattr(request, "session"),
        "session": getattr(request, "session", None)
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
