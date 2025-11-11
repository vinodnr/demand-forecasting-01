# Helper to produce stable, human-friendly worker labels for metrics
def get_worker_label(filename: str) -> str:
    # filename input like 'insights_worker.py' or 'billing_worker.py'
    if not filename:
        return 'worker'
    name = filename.replace('.py','')
    # replace underscores with spaces and title case
    pretty = name.replace('_',' ').replace('-', ' ').title()
    # shorten common suffixes
    pretty = pretty.replace('Worker', '').strip()
    return pretty or name
