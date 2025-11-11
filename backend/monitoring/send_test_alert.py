#!/usr/bin/env python3
"""Send a test alert to Alertmanager (useful to verify end-to-end Alertmanager -> notifier).

Usage:
  export ALERTMANAGER_URL=http://localhost:9093
  python backend/monitoring/send_test_alert.py --org org_demo --severity critical --summary "Test alert from repo" --instance test-instance

This script posts a single alert to Alertmanager's /api/v1/alerts endpoint.
"""
import os, sys, json, argparse, requests

def build_alert(org='org_demo', severity='critical', summary='Test alert', instance='test-instance'):
    alert = {
        "labels": {
            "alertname": "TestAlert",
            "org_id": org,
            "severity": severity,
            "job": "selftest"
        },
        "annotations": {
            "summary": summary,
            "description": "This is a test alert sent by send_test_alert.py"
        },
        "startsAt": None,
        "endsAt": None,
        "generatorURL": "https://example.com/test"
    }
    return alert

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--org', default='org_demo')
    parser.add_argument('--severity', default='critical')
    parser.add_argument('--summary', default='Test alert from repo')
    parser.add_argument('--instance', default='test-instance')
    parser.add_argument('--alertmanager', default=os.getenv('ALERTMANAGER_URL','http://localhost:9093'))
    args = parser.parse_args()
    url = args.alertmanager.rstrip('/') + '/api/v1/alerts'
    alert = build_alert(org=args.org, severity=args.severity, summary=args.summary, instance=args.instance)
    payload = [alert]
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        print('Posted test alert to', url, 'status:', r.status_code)
        print('Response:', r.text)
    except Exception as e:
        print('Failed to post alert:', e)
        sys.exit(2)

if __name__ == '__main__':
    main()
