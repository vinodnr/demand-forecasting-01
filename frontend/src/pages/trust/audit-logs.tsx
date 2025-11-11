'use client'
import React, {useEffect, useState} from 'react'
import Header from '../../components/Header'
import AuditLogTable from '../../components/trust/AuditLogTable'

export default function AuditLogs(){
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(true)
  useEffect(()=>{
    async function load(){
      setLoading(true)
      try{
        const res = await fetch('/v1/logs?limit=50')
        const data = await res.json()
        setLogs(data)
      }catch(e){ setLogs([]) }
      setLoading(false)
    }
    load()
  },[])
  return (
    <div className='min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100'>
      <Header />
      <main role='main' id='main' className='max-w-6xl mx-auto p-6'>
        <h1 className='text-3xl font-bold'>Audit Logs</h1>
        <p className='mt-2 text-sm'>Showing tenant-scoped audit logs (enforced by RLS on the backend).</p>
        <div className='mt-4'>
          <AuditLogTable logs={logs} loading={loading} />
        </div>
      </main>
    </div>
  )
}
