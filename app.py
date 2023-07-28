from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
import joblib
from pathlib import Path
import pandas as pd

from src.data_model.data_model import Property


model_path = Path.cwd() / "models" / "model.pkl"
model = joblib.load(model_path)

app = FastAPI()


@app.get("/")
def read_root():
    return {"response": "Ready!"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    key = exc.errors()[0]['loc'][1]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": f"{key} {exc.errors()[0]['msg']}"},
    )


@app.post("/predict")
def prediction(prop: Property):
    try:
        dict_prop = jsonable_encoder(prop)
        dict_prop = pd.DataFrame([dict_prop])
        y_pred = model.predict(dict_prop)
        price = float(y_pred[0])
        return {
            "prediction": price,
            "status_code": status.HTTP_200_OK
        }
    except RequestValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=e,
        )
