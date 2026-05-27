from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

telemetry = [
    {"region": "apac", "latency": 150, "uptime": 99},
    {"region": "apac", "latency": 210, "uptime": 97},
    {"region": "amer", "latency": 180, "uptime": 98},
    {"region": "amer", "latency": 220, "uptime": 96},
]

class RequestData(BaseModel):
    regions: list[str]
    threshold_ms: int

@app.get("/")
def root():
    return {"message": "API Running"}

@app.post("/")
def analyze(data: RequestData):
    result = {}

    for region in data.regions:
        records = [r for r in telemetry if r["region"] == region]

        latencies = [r["latency"] for r in records]
        uptimes = [r["uptime"] for r in records]

        result[region] = {
            "avg_latency": sum(latencies) / len(latencies),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": sum(uptimes) / len(uptimes),
            "breaches": sum(1 for l in latencies if l > data.threshold_ms)
        }

    return result
