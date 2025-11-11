'use client'
import React, { useEffect, useState } from 'react'

export default function PermissionTemplatesPage(){
  const [templates, setTemplates] = useState([])
  const [roles, setRoles] = useState([])
  const [form, setForm] = useState({role_id:'', resource:'projects', can_create:false, can_read:true, can_update:false, can_delete:false})

  useEffect(()=>{
    fetch('/v1/admin/roles').then(r=>r.json()).then(setRoles).catch(()=>setRoles([]))
    fetch('/v1/admin/permission_templates').then(r=>r.json()).then(setTemplates).catch(()=>setTemplates([]))
  },[])

  async function saveTemplate(e){
    e.preventDefault()
    const res = await fetch('/v1/admin/permission_templates', {method:'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(form)})
    if(res.ok){ alert('Saved'); setTemplates([form, ...templates]) }
  }

  return (<div className='p-4'>
    <h1 className='text-2xl font-bold'>Permission Templates</h1>
    <form onSubmit={saveTemplate} className='mb-4 space-y-2'>
      <select value={form.role_id} onChange={e=>setForm({...form, role_id:e.target.value})} className='border p-2'>
        <option value=''>Select role</option>
        {roles.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
      </select>
      <input value={form.resource} onChange={e=>setForm({...form, resource:e.target.value})} className='border p-2' placeholder='resource (e.g., projects)' />
      <div>
        <label><input type='checkbox' checked={form.can_create} onChange={e=>setForm({...form, can_create:e.target.checked})}/> create</label>
        <label className='ml-4'><input type='checkbox' checked={form.can_read} onChange={e=>setForm({...form, can_read:e.target.checked})}/> read</label>
        <label className='ml-4'><input type='checkbox' checked={form.can_update} onChange={e=>setForm({...form, can_update:e.target.checked})}/> update</label>
        <label className='ml-4'><input type='checkbox' checked={form.can_delete} onChange={e=>setForm({...form, can_delete:e.target.checked})}/> delete</label>
      </div>
      <button className='px-3 py-2 bg-green-600 text-white rounded'>Save Template</button>
    </form>

    <h2 className='text-xl font-semibold'>Existing Templates (preview)</h2>
    <ul>
      {templates.length === 0 ? <li>No templates loaded</li> : templates.map((t,i)=>(<li key={i}>{JSON.stringify(t)}</li>))}
    </ul>
  </div>)
}
