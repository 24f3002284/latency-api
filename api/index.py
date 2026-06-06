from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, numpy as np, os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

here = os.path.dirname(__file__)
with open(os.path.join(here, "q-vercel-latency.json")) as f:
    data = json.load(f)

@app.post("/api/latency")
def latency(body: dict):
    regions = body["regions"]
    threshold = body["threshold_ms"]
    result = {}
    for region in regions:
        pings = [r["latency_ms"] for r in data if r["region"] == region]
        uptimes = [r["uptime_pct"] for r in data if r["region"] == region]
        result[region] = {
            "avg_latency": round(float(np.mean(pings)), 2),
            "p95_latency": round(float(np.percentile(pings, 95)), 2),
            "avg_uptime": round(float(np.mean(uptimes)), 4),
            "breaches": int(sum(p > threshold for p in pings))
        }
    return result
