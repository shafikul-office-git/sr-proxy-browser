async def json_response(data: dict, status_code: int = 200, message: str = "Success", status: str = "success"):
    return {"data": data, "status_code": status_code, "message": message, "status": status}
