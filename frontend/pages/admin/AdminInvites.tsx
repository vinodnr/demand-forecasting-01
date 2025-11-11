'use client'
import React, {useEffect, useState} from 'react'

export default function AdminInvites(){
  const [email, setEmail] = useState('')
  const [role, setRole] = useState('viewer')
  async function sendInvite(){
    await fetch('/v1/admin/invites', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email, role})})
    alert('Invite created/sent')
    setEmail('')
  }
  return (<div className='p-4'>
    <h1 className='text-2xl font-bold'>Invites</h1>
    <div className='mt-4'>
      <input value={email} onChange={(e)=>setEmail(e.target.value)} className='border p-1' placeholder='Email' />
      <select value={role} onChange={(e)=>setRole(e.target.value)} className='ml-2 border p-1'>
        <option value='viewer'>Viewer</option>
        <option value='analyst'>Analyst</option>
        <option value='admin'>Admin</option>
      </select>
      <button onClick={sendInvite} className='ml-2 px-2 py-1 bg-green-500 text-white'>Send Invite</button>
    </div>
  </div>)
}
