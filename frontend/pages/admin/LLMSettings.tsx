'use client'
import React, { useEffect, useState } from 'react'

export default function LLMSettings(){
  const [providers, setProviders] = useState([])
  const [mappings, setMappings] = useState([])
  const [filter, setFilter] = useState('')
  const [audit, setAudit] = useState([])
  useEffect(()=>{
    fetch('/v1/admin/llm/providers').then(r=>r.json()).then(setProviders).catch(()=>setProviders([]))
    fetch('/v1/admin/llm/plan-mapping').then(r=>r.json()).then(setMappings).catch(()=>setMappings([]))
  },[])

  async function updateMapping(plan_id, provider_key){
    if(!confirm('Change LLM provider mapping for this plan? This may affect cost and behavior. Proceed?')) return;
    await fetch('/v1/admin/llm/plan-mapping/' + plan_id, {method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify({provider_key})})
    alert('Updated mapping (may require refresh)')
    // record audit fetch
    fetch('/v1/admin/llm/plan-mapping').then(r=>r.json()).then(setMappings)
  }

  async function fetchAudit(plan_id){
    const res = await fetch('/v1/admin/llm/plan-mapping') // placeholder: admin API for audit not implemented; reuse mapping endpoint
    const data = await res.json()
    setAudit(data.slice(0,10))
  }

  const filtered = mappings.filter(m => m.plan_name.toLowerCase().includes(filter.toLowerCase()) || m.tier.toLowerCase().includes(filter.toLowerCase()))

  return (<div className='p-4'>
    <h1 className='text-2xl font-bold'>LLM Provider Management</h1>
    <div className='mt-2'><input placeholder='Search plans' value={filter} onChange={(e)=>setFilter(e.target.value)} className='border p-1' /></div>
    <h2 className='mt-4'>Providers</h2>
    <ul>{providers.map(p=>(<li key={p.provider_key}>{p.display_name} ({p.provider_key})</li>))}</ul>
    <h2 className='mt-4'>Plan mappings</h2>
    <table className='table-auto mt-2'>
      <thead><tr><th>Plan</th><th>Tier</th><th>Mapped Provider</th><th>Action</th></tr></thead>
      <tbody>
        {filtered.map(m=>(
          <tr key={m.plan_id}>
            <td>{m.plan_name}</td>
            <td>{m.tier}</td>
            <td>{m.provider_key || 'default'}</td>
            <td>
              <select defaultValue={m.provider_key || ''} onChange={(e)=> updateMapping(m.plan_id, e.target.value)}>
                <option value=''>--select--</option>
                {providers.map(p=>(<option value={p.provider_key} key={p.provider_key}>{p.display_name}</option>))}
              </select>
              <button className='ml-2 px-2 py-1 bg-gray-200' onClick={()=> fetchAudit(m.plan_id)}>Audit</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
    <h2 className='mt-6'>Recent audit / mappings (sample)</h2>
    <ul>{audit.map((a, idx)=>(<li key={idx}>{JSON.stringify(a)}</li>))}</ul>
  </div>)
}
