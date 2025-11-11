'use client'
import React, { useEffect, useState } from 'react'

export default function BillingSettings(){
  const [invoices, setInvoices] = useState([])
  const [plans, setPlans] = useState([])
  useEffect(()=>{
    fetch('/v1/billing/plans').then(r=>r.json()).then(setPlans).catch(()=>setPlans([]))
    // load invoices for demo org 'org_demo'
    fetch('/v1/billing/invoices/org_demo').then(r=>r.json()).then(setInvoices).catch(()=>setInvoices([]))
  },[])

  async function checkout(plan){
    // call backend to create checkout session
    const res = await fetch('/v1/stripe/create-checkout-session', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({org_id: 'org_demo', price_id: plan.price_id, success_url: window.location.href, cancel_url: window.location.href})})
    const data = await res.json()
    if(data && data.url){
      window.location.href = data.url
    } else {
      alert('Checkout failed (placeholder)')
    }
  }

  return (<div className='p-4'>
    <h1 className='text-2xl font-bold'>Billing Settings</h1>
    <h2 className='mt-4'>Plans</h2>
    <ul>{plans.map(p=>(<li key={p.id}>{p.name} - ${(p.price_monthly_cents||0)/100}/mo <button onClick={()=>checkout(p)} className='ml-2 px-2 py-1 bg-blue-600 text-white rounded'>Subscribe</button></li>))}</ul>
    <h2 className='mt-6'>Invoices</h2>
    <ul>{invoices.map(inv=>(<li key={inv.id}>Invoice {inv.id} - ${(inv.amount_cents||0)/100} - {inv.status}</li>))}</ul>
  </div>)
