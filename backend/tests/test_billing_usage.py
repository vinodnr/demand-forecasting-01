def test_usage_service_imports():
    try:
        from backend.app.services import usage_meter as um
        from backend.app.workers import billing_worker as bw
    except Exception as e:
        assert False, f'import failed: {e}'
    assert hasattr(um, 'record_usage')
    assert hasattr(bw, 'generate_monthly_invoices')
