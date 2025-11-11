import os, logging, json
from ..services import usage_meter

# --- LLM integration helper injected by automation ---
try:
    from backend.app.services.llm_integration import get_llm_client
except Exception:
    # fallback: local import path
    try:
        from services.llm_integration import get_llm_client  # support alternative path
    except Exception:
        get_llm_client = None

def _call_llm_and_record(org_id='org_demo', messages=None, prompt=None, model='gpt-4o-mini', max_tokens=512, **kwargs):
    """Unified helper to call the LLM client and record usage. It wraps provider-specific clients.
    - If messages is provided, passes messages to client.chat_completion
    - If prompt provided, converts to a single-message chat format.
    """
    client = None
    try:
        if get_llm_client:
            client = get_llm_client()
    except Exception:
        client = None
    if messages is None and prompt is not None:
        messages = [{'role':'user','content': prompt}]
    if client is None:
        # no client available; estimate tokens and return placeholder
        prompt_text = ''
        if messages:
            prompt_text = ' '.join(m.get('content','') for m in messages)
        est = (len(prompt_text.split()) + max_tokens)
        try:
            # lazy import to avoid circular
            from backend.app.services.usage_meter import record_usage
            record_usage(org_id, 'llm_tokens', est, {'estimated': True, 'model': model})
        except Exception:
            pass
        return {'choices':[{'message':{'content':'(simulated response)'}}], 'usage': {'total_tokens': est}}
    # Use client's chat_completion
    try:
        resp = client.chat_completion(org_id=org_id, messages=messages, model=model, max_tokens=max_tokens, **kwargs)
        return resp
    except Exception:
        # fallback behavior: return placeholder
        return {'choices':[{'message':{'content':'(llm call failed)'}}], 'usage': {'total_tokens': 0}}
# --- end helper ---


logger = logging.getLogger('llm_client')

# Try to import OpenAI SDK; if missing, wrapper will still work but won't call provider
try:
    import openai
except Exception:
    openai = None

class OpenAIClient:
    def __init__(self, api_key_env='OPENAI_API_KEY'):
        self.api_key = os.getenv(api_key_env)
        if openai and self.api_key:
            openai.api_key = self.api_key

    def chat_completion(self, org_id: str, messages: list, model: str = 'gpt-4o-mini', max_tokens: int = 512, **kwargs):
        """Call OpenAI ChatCompletion and record token usage from response usage dict."""
        if openai is None or not self.api_key:
            # Fallback: estimate tokens and return placeholder
            prompt_text = ' '.join([m.get('content','') for m in messages])
            est_tokens = len(prompt_text.split()) + max_tokens
            try:
                usage_meter.record_usage(org_id, 'llm_tokens', est_tokens, {'provider':'openai','model':model,'estimated':True})
            except Exception as e:
                logger.exception('usage record failed: %s', e)
            return {'choices':[{'message':{'content':'(placeholder response)'}}], 'usage': {'total_tokens': est_tokens}}

        try:
            resp = _call_llm_and_record(messages=model=model, messages=messages, max_tokens=max_tokens, **kwargs)
            # OpenAI response includes usage.total_tokens
            usage = getattr(resp, 'usage', None) or resp.get('usage') if isinstance(resp, dict) else None
            total_tokens = 0
            if usage and isinstance(usage, dict):
                total_tokens = usage.get('total_tokens', 0)
            try:
                usage_meter.record_usage(org_id, 'llm_tokens', int(total_tokens), {'provider':'openai','model':model})
            except Exception as e:
                logger.exception('usage record failed: %s', e)
            return resp
        except Exception as e:
            logger.exception('OpenAI call failed: %s', e)
            raise