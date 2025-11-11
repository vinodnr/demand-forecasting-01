def test_get_provider_for_org_override(monkeypatch):
    from backend.app.services import llm_manager as lm
    # monkeypatch DB connection to return rows for override
    class FakeCursor:
        def __init__(self, rows):
            self._rows = rows
            self._i = 0
        def execute(self, q, params=None):
            self._q = q.lower()
            # set next fetch based on query
            if 'from public.org_llm_override' in self._q:
                self._rows = [('gemini',)]
            elif 'from public.org_subscriptions' in self._q:
                self._rows = [( 'plan-uuid', )]
            elif 'from public.plan_llm_map' in self._q:
                self._rows = [('openai',)]
            elif 'from public.llm_providers' in self._q:
                self._rows = [('openai',)]
        def fetchone(self):
            return self._rows[0] if self._rows else None
        def fetchall(self):
            return self._rows
    class FakeConn:
        def cursor(self): return FakeCursor([])
        def close(self): pass
    monkeypatch.setattr(lm, '_get_conn', lambda: FakeConn())
    # override present -> should return 'gemini'
    prov = lm.get_provider_for_org(org_id='org1')
    assert prov == 'gemini'

def test_get_provider_for_org_plan_mapping(monkeypatch):
    from backend.app.services import llm_manager as lm
    class FakeCursor:
        def execute(self, q, params=None):
            self._q = q.lower()
            if 'from public.org_llm_override' in self._q:
                self._rows = [None]
            elif 'from public.org_subscriptions' in self._q:
                self._rows = [('plan-uuid',)]
            elif 'from public.plan_llm_map' in self._q:
                self._rows = [('openai',)]
            elif 'from public.llm_providers' in self._q:
                self._rows = [('openai',)]
        def fetchone(self): return self._rows[0] if self._rows else None
        def fetchall(self): return self._rows
    class FakeConn:
        def cursor(self): return FakeCursor()
        def close(self): pass
    monkeypatch.setattr(lm, '_get_conn', lambda: FakeConn())
    prov = lm.get_provider_for_org(org_id='org1')
    assert prov == 'openai'
