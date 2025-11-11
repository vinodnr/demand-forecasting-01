# Paste this into your FastAPI app startup (or import and call it there).
# It registers the DB get_conn helper with llm_manager so provider resolution works reliably.
from backend.app.services.llm_manager import register_db_get_conn
try:
    # Adjust this import path to your project's DB helper
    from backend.app.services.db import get_conn as project_get_conn
    register_db_get_conn(project_get_conn)
    print('llm_manager: registered DB get_conn from backend.app.services.db.get_conn')
except Exception as e:
    import logging
    logging.getLogger('startup').warning('Could not register DB get_conn automatically: %s', e)
    # As a fallback you can register manually in your startup event:
    # import backend.app.services.llm_manager as lm; lm.register_db_get_conn(your_get_conn_function)
