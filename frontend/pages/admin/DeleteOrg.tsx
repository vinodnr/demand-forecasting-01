# frontend/pages/admin/DeleteOrg.tsx (React client scaffold)
'use client'
import React, {useState} from 'react'
export default function DeleteOrg(){
  const [org, setOrg] = useState('')
  const [confirm, setConfirm] = useState('')
  async function submit(){
    if(confirm !== ('DELETE ' + org)) return alert('Type DELETE <org_id> to confirm')
    const res = await fetch('/v1/org/request-delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({org_id:org, owner_id:'owner-uuid', reason:'requested via UI'})})
    alert('Requested: '+(await res.text()))
  }
  return (<div className='p-4'><h1>Delete Org</h1><input value={org} onChange={e=>setOrg(e.target.value)} placeholder='org id' className='border p-1' /><div className='mt-2'>Type: <code>DELETE {org}</code></div><input value={confirm} onChange={e=>setConfirm(e.target.value)} className='border p-1 mt-2' /><button onClick={submit} className='ml-2 bg-red-600 text-white px-2 py-1'>Delete Org</button></div>)
}
