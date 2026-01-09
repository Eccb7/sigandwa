"""
LLM API Endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from .model_manager import ModelManager
from .config import LLMConfig
from .prompt_templates import (
    SYSTEM_PROMPT,
    get_event_analysis_prompt,
    get_prophecy_interpretation_prompt,
    get_chronology_question_prompt,
    get_pattern_analysis_prompt
)
from ..database import get_db

router = APIRouter(prefix="/api/v1/llm", tags=["LLM"])

# Global model manager (lazy loaded)
_model_manager: Optional[ModelManager] = None


def get_model_manager() -> ModelManager:
    """Get or create model manager singleton"""
    global _model_manager
    if _model_manager is None:
        config = LLMConfig()
        _model_manager = ModelManager(config)
        _model_manager.load_model()
    return _model_manager


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7


class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_used: int


class EventAnalysisRequest(BaseModel):
    event_id: int


class ProphecyInterpretationRequest(BaseModel):
    prophecy_text: str
    context: Optional[str] = ""


class ChronologyQuestionRequest(BaseModel):
    question: str
    max_events: int = 10


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """General chat interface with Biblical knowledge"""
    try:
        manager = get_model_manager()
        
        # Build conversation with system prompt
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(request.conversation_history)
        messages.append({"role": "user", "content": request.message})
        
        response_text = manager.chat(messages)
        
        return ChatResponse(
            response=response_text,
            model=manager.config.model_name,
            tokens_used=len(response_text.split())  # Approximate
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")


@router.post("/analyze-event")
async def analyze_event(request: EventAnalysisRequest, db: Session = Depends(get_db)):
    """Analyze a specific historical event"""
    from ..models.chronology import ChronologyEvent
    
    event = db.query(ChronologyEvent).filter(ChronologyEvent.id == request.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    manager = get_model_manager()
    
    event_dict = {
        "name": event.name,
        "year_start": event.year_start,
        "era": event.era.value if hasattr(event.era, 'value') else str(event.era),
        "description": event.description or "No description available",
        "biblical_source": event.biblical_source or "N/A"
    }
    
    prompt = get_event_analysis_prompt(event_dict)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    analysis = manager.chat(messages)
    
    return {"event": event_dict, "analysis": analysis}


@router.post("/interpret-prophecy")
async def interpret_prophecy(request: ProphecyInterpretationRequest):
    """Interpret a Biblical prophecy using historicist method"""
    manager = get_model_manager()
    
    prompt = get_prophecy_interpretation_prompt(request.prophecy_text, request.context)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    interpretation = manager.chat(messages)
    
    return {
        "prophecy": request.prophecy_text,
        "interpretation": interpretation,
        "method": "historicist"
    }


@router.post("/ask-chronology")
async def ask_chronology(request: ChronologyQuestionRequest, db: Session = Depends(get_db)):
    """Ask a question about Biblical chronology"""
    from ..models.chronology import ChronologyEvent
    from sqlalchemy import or_, func
    
    # Search for relevant events (simple keyword matching)
    keywords = request.question.lower().split()
    query = db.query(ChronologyEvent)
    
    # Build filter for keywords
    filters = []
    for keyword in keywords[:5]:  # Limit to 5 keywords
        filters.append(func.lower(ChronologyEvent.name).contains(keyword))
        filters.append(func.lower(ChronologyEvent.description).contains(keyword))
    
    if filters:
        query = query.filter(or_(*filters))
    
    relevant_events = query.limit(request.max_events).all()
    
    events_data = [{
        "name": e.name,
        "year_start": e.year_start,
        "biblical_source": e.biblical_source or "historical"
    } for e in relevant_events]
    
    manager = get_model_manager()
    prompt = get_chronology_question_prompt(request.question, events_data)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    answer = manager.chat(messages)
    
    return {
        "question": request.question,
        "answer": answer,
        "relevant_events": events_data
    }


@router.get("/model-info")
async def get_model_info():
    """Get information about the loaded model"""
    try:
        manager = get_model_manager()
        return {
            "model_name": manager.config.model_name,
            "quantization": manager.config.quantization,
            "context_window": manager.config.context_window,
            "device": "CPU (optimized)",
            "threads": os.cpu_count() or 4,
            "status": "loaded" if manager.model else "not_loaded"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@router.post("/reload-model")
async def reload_model(background_tasks: BackgroundTasks):
    """Reload the model (useful after updates)"""
    global _model_manager
    _model_manager = None
    
    def load_in_background():
        get_model_manager()
    
    background_tasks.add_task(load_in_background)
    
    return {"message": "Model reload initiated in background"}


import os
