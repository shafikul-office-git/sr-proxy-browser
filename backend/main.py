
import uvicorn
from config.app import app, Request

# =================================
# Initialize API route 
# =================================
from router.api import register_routers
register_routers(app)

# =================================
# Initialize WEB route 
# =================================
import router.web

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
