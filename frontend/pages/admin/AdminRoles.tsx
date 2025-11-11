'use client'
import React, {useEffect, useState} from 'react'

export default function AdminRoles(){
  const [roles, setRoles] = useState([])
  const [newRole, setNewRole] = useState('')
  useEffect(()=>{ fetch('/v1/admin/roles').then(r=>r.json()).then(setRoles).catch(()=>setRoles([])) },[])
  async function createRole(){
    if(!newRole) return alert('enter name')
    await fetch('/v1/admin/roles', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({name:newRole, description:''})})
    setNewRole(''); setRoles([]); fetch('/v1/admin/roles').then(r=>r.json()).then(setRoles)
  }
  return (<div className='p-4'>
    <h1 className='text-2xl font-bold'>Roles</h1>
    <div className='mt-4'>
      <input value={newRole} onChange={(e)=>setNewRole(e.target.value)} className='border p-1' placeholder='Role name' />
      <button onClick={createRole} className='ml-2 px-2 py-1 bg-blue-500 text-white'>Create</button>
    </div>
    <ul className='mt-4'>{roles.map(r=>(<li key={r.id}>{r.name} - {r.description}</li>))}</ul>
  </div>)
}
