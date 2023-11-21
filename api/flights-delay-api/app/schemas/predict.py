from typing import Any, List, Optional

from pydantic import BaseModel
from model.processing.validation import DataInputSchema

# Esquema de los resultados de predicción
class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: Optional[List[float]]

# Esquema para inputs múltiples
class MultipleDataInputs(BaseModel):
    inputs: List[DataInputSchema]

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "Month": 5,
                        "DayOfWeek": 2,
                        "DestAirportID": 14747,
                        "AirportID": 14771,
                        "Day": 21,
                        "Visibility": 10.0,
                        "DryBulbCelsius": 15.0,
                        "WetBulbCelsius":10.5,
                        "DewPointCelsius":6.1,
                        "RelativeHumidity":56.0,
                        "WindSpeed":25.0,
                        "WindDirection":280.0,
                        "StationPressure":29.96,
                        "Altimeter":29.98,
                        "AA":True,
                        "SP":False,
                        "SYMT":False
                    }
                ]
            }
        }
