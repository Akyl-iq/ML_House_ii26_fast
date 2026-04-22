from fastapi import APIRouter
import joblib
from my_project.database.schema import HousePredictSchema

predict_router = APIRouter(prefix='/predict', tags=['Predict'])


model = joblib.load('my_project/ml_model/log_model.pkl')
scaler = joblib.load('my_project/ml_model/scaler (2).pkl')

@predict_router.post("/")
async def predict(house: HousePredictSchema):
    house_dict = house.dict()

    neighborhood = house_dict.pop("Neighborhood")
    neighborhood_1_0 = [
        1 if neighborhood == "Blmngtn" else 0,  # ← добавь эту строку первой
        1 if neighborhood == "Blueste" else 0,
        1 if neighborhood == "BrDale" else 0,
        1 if neighborhood == "BrkSide" else 0,
        1 if neighborhood == "ClearCr" else 0,
        1 if neighborhood == "CollgCr" else 0,
        1 if neighborhood == "Crawfor" else 0,
        1 if neighborhood == "Edwards" else 0,
        1 if neighborhood == "Gilbert" else 0,
        1 if neighborhood == "IDOTRR" else 0,
        1 if neighborhood == "MeadowV" else 0,
        1 if neighborhood == "Mitchel" else 0,
        1 if neighborhood == "NAmes" else 0,
        1 if neighborhood == "NPkVill" else 0,
        1 if neighborhood == "NWAmes" else 0,
        1 if neighborhood == "NoRidge" else 0,
        1 if neighborhood == "NridgHt" else 0,
        1 if neighborhood == "OldTown" else 0,
        1 if neighborhood == "SWISU" else 0,
        1 if neighborhood == "Sawyer" else 0,
        1 if neighborhood == "SawyerW" else 0,
        1 if neighborhood == "Somerst" else 0,
        1 if neighborhood == "StoneBr" else 0,
        1 if neighborhood == "Timber" else 0,
        1 if neighborhood == "Veenker" else 0,
    ]

    data = list(house_dict.values()) + neighborhood_1_0

    scaled_data = scaler.transform([data])[0]
    print(scaled_data)
    pred = model.predict([scaled_data])[0]
    return {'predict price': round(pred, 2)}