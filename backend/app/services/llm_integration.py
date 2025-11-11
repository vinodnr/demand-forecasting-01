from .llm_client import OpenAIClient
from . import llm_manager as manager
from .gemini_client import GeminiClient
from .grok_client import GrokClient

def get_llm_client_for_org(org_id=None, plan_id=None):
    provider_key = manager.get_provider_for_org(org_id=org_id, plan_id=plan_id)
    if provider_key == 'openai':
        return OpenAIClient(api_key_env='OPENAI_API_KEY')
    elif provider_key == 'gemini':
        return GeminiClient(api_key_env='GEMINI_API_KEY', api_host_env='GEMINI_API_HOST')
    elif provider_key == 'grok':
        return GrokClient(api_key_env='GROK_API_KEY', api_host_env='GROK_API_HOST')
    else:
        return OpenAIClient()
