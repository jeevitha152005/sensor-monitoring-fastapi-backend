from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password@21",
    database="sensor_db"
)

cursor = db.cursor()

class Sensor(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float


@app.get("/")
def read_root():
    return {"message": "Backend running successfully"}


@app.get("/sensors")
def get_sensors():
    cursor.execute("SELECT * FROM sensor_data")
    result = cursor.fetchall()
    return {"data": result}


@app.post("/add_sensor")
def add_sensor(data: Sensor):

    cursor.execute(
        "INSERT INTO sensor_data (sensor_id, temperature, humidity) VALUES (%s,%s,%s)",
        (data.sensor_id, data.temperature, data.humidity)
    )
    db.commit()

    if data.temperature > 40:
        cursor.execute(
            "INSERT INTO alerts (sensor_id, alert_message) VALUES (%s,%s)",
            (data.sensor_id, "High Temperature Alert")
        )
        db.commit()

    return {"message": "Sensor data added successfully"}