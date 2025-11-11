'use client'
import React, { useEffect, useState } from 'react'

export default function ManageSubscription(){
  const [subs, setSubs] = useState([])
  useEffect(()=>{
    // fetch subscriptions - backend endpoint not implemented fully; placeholder uses org_demo
    fetch('/v1/billing/subscriptions?org_id=org_demo').then(r=>r.json()).then(setSubs).catch(()=>setSubs([]))
  },[])

  async function cancelSub(sid){
    const res = await fetch('/v1/billing/cancel', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({subscription_id: sid})})
    if(res.ok) alert('Cancelled')
    else alert('Cancel failed')
  }

  return (<div className='p-4'>
    <h1 className='text-2xl font-bold'>Manage Subscription</h1>
    <ul>{subs.map(s=>(<li key={s.id}>{s.plan_id} - {s.status} <button onClick={()=>cancelSub(s.id)} className='ml-2 px-2 py-1 bg-red-600 text-white rounded'>Cancel</button></li>))}</ul>
  </div>)
