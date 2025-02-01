from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from check_imei import CheckIMEI
from other import is_valid_imei

app = FastAPI()


class IMEIRequest(BaseModel):
    imei: str


@app.post("/api/check-imei")
async def check_imei(request: IMEIRequest):
    imei = request.imei
    if not is_valid_imei(imei):
        raise HTTPException(status_code=400, detail="Неверный IMEI. IMEI должен содержать 15 цифр.")

    check_imei_instance = CheckIMEI(imei=imei, request_api=True)
    result = check_imei_instance.get_data_imei()

    if "Не удалось получить результаты проверки" in result or "Сервис недоступен, попробуйте позже" in result:
        raise HTTPException(status_code=500, detail=result)

    return {"result": result}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
