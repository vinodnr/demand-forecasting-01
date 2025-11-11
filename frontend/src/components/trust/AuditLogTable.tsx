'use client'
import React from 'react'

export default function AuditLogTable({logs, loading}:{logs:any[], loading:boolean}){
  if(loading) return <div className='p-4'>Loading...</div>
  if(!logs || logs.length===0) return <div className='p-4'>No audit logs available.</div>
  return (
    <div className='overflow-x-auto bg-white dark:bg-gray-800 rounded shadow' role='region' aria-label='Audit logs'>
      <table className='min-w-full divide-y' aria-describedby='audit-desc'>
        <caption id='audit-desc' className='sr-only'>Tenant-scoped audit logs table</caption>
        <thead className='bg-gray-50 dark:bg-gray-700'>
          <tr>
            <th scope='col' className='px-4 py-2 text-left text-sm font-medium'>Time</th>
            <th scope='col' className='px-4 py-2 text-left text-sm font-medium'>Actor</th>
            <th scope='col' className='px-4 py-2 text-left text-sm font-medium'>Action</th>
            <th scope='col' className='px-4 py-2 text-left text-sm font-medium'>Details</th>
          </tr>
        </thead>
        <tbody className='bg-white dark:bg-gray-800 divide-y'>
          {logs.map((l:any)=>(
            <tr key={l.id}>
              <td className='px-4 py-2 text-sm'>{l.created_at ? new Date(l.created_at).toLocaleString() : ''}</td>
              <td className='px-4 py-2 text-sm'>{l.actor_id || 'system'}</td>
              <td className='px-4 py-2 text-sm'>{l.action}</td>
              <td className='px-4 py-2 text-sm'><pre className='whitespace-pre-wrap'>{JSON.stringify(l.details)}</pre></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
