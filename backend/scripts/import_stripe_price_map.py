#!/usr/bin/env python3
import os, json, sys
from ..app.services import llm_manager as llm

# Usage: place a JSON file at backend/migrations/stripe_price_map.json and run this script
# JSON format: [{"plan_tier":"free","stripe_price_id":"price_xxx"}, ...] or [{"plan_id":"<uuid>","stripe_price_id":"price_xxx"}]

def load_and_apply(path='backend/migrations/stripe_price_map.json'):
    with open(path,'r') as f:
        data = json.load(f)
    conn = llm._get_conn()
    with conn.cursor() as cur:
        for item in data:
            if 'plan_id' in item:
                cur.execute('UPDATE public.plans SET stripe_price_id=%s WHERE id=%s RETURNING id',(item['stripe_price_id'], item['plan_id']))
            elif 'plan_tier' in item:
                cur.execute('UPDATE public.plans SET stripe_price_id=%s WHERE tier=%s RETURNING id',(item['stripe_price_id'], item['plan_tier']))
            else:
                print('Skipping invalid entry', item)
        conn.commit()
    conn.close()
    print('Applied mapping for', len(data), 'entries')

if __name__=='__main__':
    path = sys.argv[1] if len(sys.argv)>1 else 'backend/migrations/stripe_price_map.json'
    load_and_apply(path)
