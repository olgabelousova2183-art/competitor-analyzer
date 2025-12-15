"""FastAPI application for Competitor Analyzer"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import shutil
from datetime import datetime
import json

from openaiservice import analyze_image, analyze_text
from parsingservice import ParsingService, get_parsing_service
from config import HISTORY_DIR

app = FastAPI(title="Competitor Analyzer API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure history directory exists
os.makedirs(HISTORY_DIR, exist_ok=True)
os.makedirs("uploads", exist_ok=True)


class TextAnalysisRequest(BaseModel):
    text: str


@app.get("/")
async def root():
    return {"message": "Competitor Analyzer API", "version": "1.0.0"}


@app.post("/analyzeimage")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    """
    Analyze an uploaded image for competitor insights
    """
    try:
        # Save uploaded file temporarily
        file_path = f"uploads/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Analyze the image
        result = analyze_image(file_path)
        
        # Save to history
        history_entry = {
            "type": "image_analysis",
            "timestamp": datetime.now().isoformat(),
            "filename": file.filename,
            "result": result
        }
        history_file = os.path.join(HISTORY_DIR, f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_entry, f, ensure_ascii=False, indent=2)
        
        # Clean up temporary file
        try:
            os.remove(file_path)
        except:
            pass
        
        if result.get("success"):
            return JSONResponse(content=result)
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Analysis failed"))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyzetext")
async def analyze_text_endpoint(request: TextAnalysisRequest):
    """
    Analyze text content for competitor insights
    """
    try:
        # Analyze the text
        result = analyze_text(request.text)
        
        # Save to history
        history_entry = {
            "type": "text_analysis",
            "timestamp": datetime.now().isoformat(),
            "text_preview": request.text[:200] + "..." if len(request.text) > 200 else request.text,
            "result": result
        }
        history_file = os.path.join(HISTORY_DIR, f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_entry, f, ensure_ascii=False, indent=2)
        
        if result.get("success"):
            return JSONResponse(content=result)
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Analysis failed"))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/parsedemo")
async def parse_demo():
    """
    Demo endpoint to parse competitor websites
    """
    parsing_service = None
    try:
        parsing_service = get_parsing_service()
        
        # Parse all competitors
        results = parsing_service.parse_all_competitors()
        
        # Save to history
        history_file = parsing_service.save_to_history(results)
        
        return JSONResponse(content={
            "success": True,
            "results": results,
            "history_file": history_file,
            "message": f"Parsed {len(results)} competitor sites"
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Ensure driver is closed even if error occurs
        if parsing_service:
            try:
                parsing_service.close()
            except:
                pass


@app.get("/history")
async def get_history():
    """
    Get analysis history
    """
    try:
        history_files = []
        if os.path.exists(HISTORY_DIR):
            for filename in os.listdir(HISTORY_DIR):
                if filename.endswith('.json'):
                    file_path = os.path.join(HISTORY_DIR, filename)
                    file_stat = os.stat(file_path)
                    history_files.append({
                        "filename": filename,
                        "size": file_stat.st_size,
                        "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                    })
        
        return JSONResponse(content={
            "success": True,
            "files": sorted(history_files, key=lambda x: x["modified"], reverse=True)
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT
    uvicorn.run(app, host=API_HOST, port=API_PORT)

