# backend/app/startup_register_jwt.py
# Import and call this from your FastAPI startup event
from backend.src.auth.jwt_middleware import jwt_dependency
from backend.src.db.session import db_session
from backend.app.services.llm_manager import register_db_get_conn
from backend.app.services.db import get_conn as project_get_conn

def register_startup(app):
    # register DB helper for llm_manager (explicit)
    try:
        register_db_get_conn(project_get_conn)
        print('Registered DB get_conn for llm_manager')
    except Exception as e:
        print('Could not register llm_manager DB helper:', e)

    # Example: include jwt dependency globally if desired (or use per-route)
    # app.dependency_overrides[jwt_dependency] = jwt_dependency  # don't override blindly; use Depends(jwt_dependency) on routes
    print('Startup registration complete. To use JWT middleware, add Depends(jwt_dependency) to protected routes.')
