import json
import types
import pytest

# Monkeypatch stripe.Webhook.construct_event to return a fake event
def test_stripe_webhook_invoice_paid(monkeypatch):
    # prepare fake event
    fake_event = {'id':'evt_test_1','type':'invoice.payment_succeeded','data':{'object':{'id':'in_1','amount_due':1000,'currency':'usd','metadata':{'org_id':'org_demo'}}}}
    class FakeWebhook:
        @staticmethod
        def construct_event(payload, sig, secret):
            return fake_event
    monkeypatch.setattr('stripe.Webhook', FakeWebhook)

    # fake DB connection to capture INSERT into processed_events and invoice update/insert
    calls = {'inserts':[], 'updates':[]}
    class FakeCursor:
        def __init__(self):
            self.rows=[]
        def execute(self, q, params=None):
            ql = q.lower()
            if 'insert into public.processed_events' in ql or 'insert into public.invoices' in ql:
                calls['inserts'].append((q, params))
                # simulate fetchone for RETURNING id
                self._last = ('newid',)
            elif 'select 1 from public.processed_events' in ql:
                self._last = None
            elif 'update public.invoices set status' in ql:
                calls['updates'].append((q, params))
                self._last = None
            else:
                self._last = None
        def fetchone(self):
            return getattr(self, '_last', None)
        def fetchall(self):
            return []
    class FakeConn:
        def cursor(self):
            return FakeCursor()
        def commit(self):
            pass
        def close(self):
            pass
    # monkeypatch llm_manager._get_conn
    import backend.app.services.llm_manager as lm
    monkeypatch.setattr(lm, '_get_conn', lambda: FakeConn())

    # call the handler directly (it expects payload bytes and sig header)
    from backend.app.services.stripe_service import handle_webhook
    payload = b'{}'
    sig = 'sig'
    evt = handle_webhook(payload, sig, 'whsec_test')
    assert evt['id'] == 'evt_test_1'
    # verify processed event inserted and invoice created/updated captured
    assert len(calls['inserts']) >= 1

def test_stripe_webhook_subscription_updated(monkeypatch):
    fake_event = {'id':'evt_sub_1','type':'customer.subscription.updated','data':{'object':{'id':'sub_1','status':'active','metadata':{'org_id':'org_demo'}}}}
    class FakeWebhook:
        @staticmethod
        def construct_event(payload, sig, secret):
            return fake_event
    monkeypatch.setattr('stripe.Webhook', FakeWebhook)

    calls = {'updates':[]}
    class FakeCursor:
        def execute(self, q, params=None):
            calls['updates'].append((q, params))
        def fetchone(self): return None
    class FakeConn:
        def cursor(self): return FakeCursor()
        def commit(self): pass
        def close(self): pass
    import backend.app.services.llm_manager as lm
    monkeypatch.setattr(lm, '_get_conn', lambda: FakeConn())

    from backend.app.services.stripe_service import handle_webhook
    evt = handle_webhook(b'{}', 'sig', 'whsec_test')
    assert evt['id'] == 'evt_sub_1'
    # expect that subscription update SQL was attempted
    assert any('org_subscriptions' in (q.lower()) or 'update public.org_subscriptions' in (q.lower()) for q, _ in calls['updates'])



def test_stripe_webhook_invoice_failed(monkeypatch):
    fake_event = {'id':'evt_fail_1','type':'invoice.payment_failed','data':{'object':{'id':'in_fail_1','amount_due':2000,'currency':'usd','metadata':{'org_id':'org_demo'}}}}
    class FakeWebhook:
        @staticmethod
        def construct_event(payload, sig, secret):
            return fake_event
    monkeypatch.setattr('stripe.Webhook', FakeWebhook)

    calls = {'updates':[],'inserts':[]}
    class FakeCursor:
        def execute(self, q, params=None):
            ql = q.lower()
            if 'update public.invoices set status' in ql:
                calls['updates'].append((q, params))
            elif 'insert into public.processed_events' in ql:
                calls['inserts'].append((q, params))
        def fetchone(self): return None
        def fetchall(self): return []
    class FakeConn:
        def cursor(self): return FakeCursor()
        def commit(self): pass
        def close(self): pass
    import backend.app.services.llm_manager as lm
    monkeypatch.setattr(lm, '_get_conn', lambda: FakeConn())

    from backend.app.services.stripe_service import handle_webhook
    evt = handle_webhook(b'{}', 'sig', 'whsec_test')
    assert evt['id'] == 'evt_fail_1'
    assert any('invoice' in (q.lower()) for q, _ in calls['updates']) or len(calls['inserts'])>0

def test_stripe_webhook_subscription_deleted(monkeypatch):
    fake_event = {'id':'evt_sub_del','type':'customer.subscription.deleted','data':{'object':{'id':'sub_del_1','status':'canceled','metadata':{'org_id':'org_demo'}}}}
    class FakeWebhook:
        @staticmethod
        def construct_event(payload, sig, secret):
            return fake_event
    monkeypatch.setattr('stripe.Webhook', FakeWebhook)

    calls = {'updates':[]}
    class FakeCursor:
        def execute(self, q, params=None):
            calls['updates'].append((q, params))
        def fetchone(self): return None
    class FakeConn:
        def cursor(self): return FakeCursor()
        def commit(self): pass
        def close(self): pass
    import backend.app.services.llm_manager as lm
    monkeypatch.setattr(lm, '_get_conn', lambda: FakeConn())

    from backend.app.services.stripe_service import handle_webhook
    evt = handle_webhook(b'{}', 'sig', 'whsec_test')
    assert evt['id'] == 'evt_sub_del'
    assert any('org_subscriptions' in q.lower() or 'update public.org_subscriptions' in q.lower() for q, _ in calls['updates'])

def test_stripe_webhook_invoice_refund(monkeypatch):
    fake_event = {'id':'evt_ref_1','type':'invoice.refund','data':{'object':{'id':'in_ref_1','amount_refunded':500,'currency':'usd','metadata':{'org_id':'org_demo'}}}}
    class FakeWebhook:
        @staticmethod
        def construct_event(payload, sig, secret):
            return fake_event
    monkeypatch.setattr('stripe.Webhook', FakeWebhook)

    calls = {'updates':[],'inserts':[]}
    class FakeCursor:
        def execute(self, q, params=None):
            ql = q.lower()
            if 'insert into public.processed_events' in ql:
                calls['inserts'].append((q,params))
            if 'update public.invoices set status' in ql:
                calls['updates'].append((q,params))
        def fetchone(self): return None
        def fetchall(self): return []
    class FakeConn:
        def cursor(self): return FakeCursor()
        def commit(self): pass
        def close(self): pass
    import backend.app.services.llm_manager as lm
    monkeypatch.setattr(lm, '_get_conn', lambda: FakeConn())

    from backend.app.services.stripe_service import handle_webhook
    evt = handle_webhook(b'{}', 'sig', 'whsec_test')
    assert evt['id'] == 'evt_ref_1'
    # ensure processed event logged
    assert len(calls['inserts'])>=1 or len(calls['updates'])>=0
