'use client'
import React, { useEffect, useState } from 'react'

export default function CheckoutPage(){
  const [plans, setPlans] = useState([])
  useEffect(()=>{
    fetch('/v1/billing/plans').then(r=>r.json()).then(setPlans).catch(()=>setPlans([]))
  },[])

  async function subscribeWithPlan(plan){
    const body = { org_id: 'org_demo', price_id: plan.stripe_price_id, success_url: window.location.href, cancel_url: window.location.href }
    const res = await fetch('/v1/stripe/create-checkout-session', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)})
    const data = await res.json()
    if(data && data.url){
      window.location.href = data.url
    } else {
      alert('Failed to create checkout session')
    }
  }

  return (<div className='p-4'>
    <h1 className='text-2xl font-bold'>Checkout</h1>
    <ul>
      {plans.map(p=>(<li key={p.id}>{p.name} - ${(p.price_monthly_cents||0)/100}/mo <button onClick={()=>subscribeWithPlan(p)} className='ml-2 px-2 py-1 bg-blue-600 text-white rounded'>Subscribe</button></li>))}
    </ul>
  </div>)
}
