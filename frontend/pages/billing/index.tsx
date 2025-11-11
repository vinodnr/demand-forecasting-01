'use client'
import React, { useEffect, useState } from 'react'

export default function BillingPage(){
  const [plans, setPlans] = useState([])
  useEffect(()=>{
    fetch('/v1/billing/plans').then(r=>r.json()).then(setPlans).catch(()=>setPlans([]))
  },[])
  return (<div className='p-4'>
    <h1 className='text-2xl font-bold'>Billing & Plans</h1>
    <ul>
      {plans.map(p=> (<li key={p.id}>{p.name} — ${ (p.price_monthly_cents||0)/100 }/mo</li>))}
    </ul>
  </div>)
}
