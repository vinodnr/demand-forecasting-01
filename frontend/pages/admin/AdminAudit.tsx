'use client'
import React, {useEffect, useState} from 'react'

export default function AdminAudit(){
  const [audit, setAudit] = useState([])
  useEffect(()=>{ fetch('/v1/admin/audit').then(r=>r.json()).then(setAudit).catch(()=>setAudit([])) },[])
  return (<div className='p-4'>
    <h1 className='text-2xl font-bold'>Audit</h1>
    <ul className='mt-4'>{audit.map(a=>(<li key={a.id}>{a.created_at} - {a.action} - {JSON.stringify(a.details)}</li>))}</ul>
  </div>)
}
