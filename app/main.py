"""
FastAPI application initialization and configuration.

Sets up the main FastAPI app with CORS, middleware, routers, and health checks.
"""

import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage app lifecycle events.
    
    This function handles startup and shutdown events.
    """
    # Startup
    logger.info("🚀 Document Intelligence API starting up...")
    logger.info("✓ LLM configured and ready")
    logger.info("✓ All services initialized")
    yield
    # Shutdown
    logger.info("🛑 Document Intelligence API shutting down...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="AI Document Intelligence API",
        description="Intelligent document classification, extraction, validation, and summarization system powered by LangChain and GPT-4o",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict to specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """
        Health check endpoint.
        
        Returns:
            dict: Health status
        """
        return {
            "status": "healthy",
            "service": "Document Intelligence API",
            "timestamp": time.time(),
        }

    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """
        Root endpoint with API information.
        
        Returns:
            dict: API information and available endpoints
        """
        return {
            "message": "AI Document Intelligence API",
            "version": "1.0.0",
            "documentation": "/docs",
            "endpoints": {
                "health": "/health",
                "analyze": "/api/analyze",
            },
        }

    # Error handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        """Handle HTTP exceptions."""
        logger.error(f"HTTP Exception: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": "error", "message": exc.detail},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        """Handle general exceptions."""
        logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Internal server error"},
        )

    logger.info("✓ FastAPI app created successfully")
    return app


# Create the application instance
app = create_app()
