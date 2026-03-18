from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import pandas as pd
from analysis import analyze_data, generate_charts
from model import predict_trends
from report import create_pdf_report

app = FastAPI(title="AI Data Analyst")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static charts
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")
    
    # Save uploaded file
    filepath = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Analyze
    df_summary = analyze_data(filepath)
    charts = generate_charts(filepath)
    predictions = predict_trends(filepath)
    
    report_path = create_pdf_report(filepath, charts, predictions)
    
    return {
        "summary": df_summary,
        "charts": charts,
        "predictions": predictions,
        "report_url": f"/static/{os.path.basename(report_path)}"
    }

@app.get("/")
def root():
    return {"message": "AI Data Analyst Backend Running"}
