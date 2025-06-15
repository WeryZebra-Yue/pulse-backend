from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import os

router = APIRouter()


@router.get(
    "/", 
    response_class=HTMLResponse,
    summary="API Welcome Page",
    description="Welcome page for the AidAgent API with navigation links to interactive documentation and API exploration tools. Features a modern, responsive design showcasing the platform's key capabilities."
)
async def read_root():
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the aidagent_backend directory, then to templates
    template_path = os.path.join(os.path.dirname(current_dir), "templates", "home.html")
    
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        # Fallback HTML if template file is not found
        return HTMLResponse(content="""
        <html>
            <head>
                <title>AidAgent API</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="font-family: system-ui, -apple-system, sans-serif; margin: 0; padding: 20px; background: #f8fafc;">
                <div style="max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                    <h1 style="color: #1e293b; margin-bottom: 16px;">🚀 AidAgent API</h1>
                    <p style="color: #64748b; margin-bottom: 24px;">Template file not found. Please create templates/home.html</p>
                    <a href="/docs" style="display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px;">View API Documentation</a>
                </div>
            </body>
        </html>
        """) 