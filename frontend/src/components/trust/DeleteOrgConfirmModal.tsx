'use client'
import React, {useState, useEffect, useRef} from 'react'

export default function DeleteOrgConfirmModal({onClose}:{onClose:()=>void}){
  const [confirm, setConfirm] = useState('')
  const [status, setStatus] = useState('')
  const inputRef = useRef<HTMLInputElement|null>(null)
  const modalRef = useRef<HTMLDivElement|null>(null)

  useEffect(()=>{
    // focus the input when modal opens
    inputRef.current?.focus()
    // simple focus trap
    function handleKey(e: KeyboardEvent){
      if(e.key === 'Tab' && modalRef.current){
        const focusable = modalRef.current.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')
        if(focusable.length === 0) return
        const first = focusable[0] as HTMLElement
        const last = focusable[focusable.length-1] as HTMLElement
        if(e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
        else if(!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
      }
      if(e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', handleKey)
    return ()=> document.removeEventListener('keydown', handleKey)
  },[onClose])

  async function submit(){
    if(!confirm) return alert('Type the confirmation text to continue.')
    setStatus('Requesting deletion...')
    try{
      const res = await fetch('/v1/org/request-delete', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({org_id: confirm, owner_id: 'owner-unknown'})})
      const data = await res.json()
      setStatus('Requested: ' + JSON.stringify(data))
    }catch(e){ setStatus('Error: '+String(e)) }
  }
  return (
    <div className='fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center' role='dialog' aria-modal='true' aria-label='Confirm organization deletion'>
      <div ref={modalRef} className='bg-white dark:bg-gray-800 p-6 rounded shadow max-w-lg w-full' role='document'>
        <h2 className='text-xl font-semibold'>Confirm deletion</h2>
        <p className='mt-2 text-sm'>Type your organization ID to confirm irreversible deletion.</p>
        <label htmlFor='org-confirm' className='sr-only'>Organization ID confirmation</label>
        <input id='org-confirm' ref={inputRef} value={confirm} onChange={(e)=>setConfirm(e.target.value)} className='w-full border p-2 mt-3' placeholder='Type organization id here' aria-required='true' aria-label='Organization confirmation input' />
        <div className='mt-4 flex justify-end space-x-2'>
          <button type='button' type='button' onClick={onClose} className='px-3 py-1 border rounded'>Cancel</button>
          <button type='button' type='button' onClick={submit} className='px-3 py-1 bg-red-600 text-white rounded'>Confirm Delete</button>
        </div>
        <div className='mt-3 text-sm' aria-live='polite'>Status: {status}</div>
      </div>
    </div>
  )
}
