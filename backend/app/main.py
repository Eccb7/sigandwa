"""
Main FastAPI application entry point.
Configures middleware, routers, and startup/shutdown events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.api.routes import chronology, events, patterns, prophecies, simulation, graph
from app.llm.api import router as llm_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Biblical Cliodynamic Analysis System with Local LLM",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chronology.router, prefix="/api/v1/chronology", tags=["chronology"])
app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
app.include_router(patterns.router, prefix="/api/v1/patterns", tags=["patterns"])
app.include_router(prophecies.router, prefix="/api/v1/prophecies", tags=["prophecies"])
app.include_router(simulation.router, prefix="/api/v1/simulation", tags=["simulation"])
app.include_router(graph.router, prefix="/api/v1/graph", tags=["graph"])
app.include_router(llm_router)


@app.get("/")
async def root():
    """Root endpoint with system information."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": "Biblical Cliodynamic Analysis System with Local LLM",
        "features": ["chronology", "patterns", "prophecy", "simulation", "graph", "llm"],
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.VERSION}
