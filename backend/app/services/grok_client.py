import os, logging, json
logger = logging.getLogger('grok_client')
try:
    import requests
except Exception:
    requests = None
try:
    import grok_sdk as grok
except Exception:
    grok = None
from .llm_client import OpenAIClient

class GrokClient:
    def __init__(self, api_key_env='GROK_API_KEY', api_host_env='GROK_API_HOST'):
        self.api_key = os.getenv(api_key_env)
        self.api_host = os.getenv(api_host_env)
        if grok and self.api_key:
            try:
                self.client = grok.Client(api_key=self.api_key)
            except Exception:
                self.client = None
        else:
            self.client = None

    def chat_completion(self, org_id: str, messages: list, model: str='grok-1', max_tokens: int=512, **kwargs):
        if self.client is not None:
            try:
                resp = self.client.chat(messages=messages, model=model, max_tokens=max_tokens, **kwargs)
                usage = getattr(resp, 'usage', None) or (resp.get('usage') if isinstance(resp, dict) else None)
                return {'choices':[{'message':{'content': resp.get('text') if isinstance(resp, dict) else str(resp)}}], 'usage': usage or {}}
            except Exception as e:
                logger.exception('Grok SDK call failed: %s', e)
        if requests and self.api_host and self.api_key:
            try:
                payload = {'messages': messages, 'model': model, 'max_tokens': max_tokens, 'metadata': {'org_id': org_id}}
                headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
                r = requests.post(self.api_host, json=payload, headers=headers, timeout=30)
                r.raise_for_status()
                data = r.json()
                usage = data.get('usage') if isinstance(data, dict) else {}
                text = data.get('choices',[{}])[0].get('message',{}).get('content') if isinstance(data, dict) else str(data)
                return {'choices':[{'message':{'content': text}}], 'usage': usage or {}}
            except Exception as e:
                logger.exception('Grok HTTP fallback failed: %s', e)
        fallback = OpenAIClient(api_key_env='GROK_API_KEY')
        return fallback.chat_completion(org_id=org_id, messages=messages, model=model, max_tokens=max_tokens, **kwargs)
