def calculator(expr: str):
    try:
        return {"ok": True, "result": eval(expr)}
    except Exception as e:
        return {"ok": False, "error": str(e)}
