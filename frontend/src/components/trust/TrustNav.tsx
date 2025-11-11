'use client'
import React from 'react'
export default function TrustNav(){
  return (
    <nav aria-label='Trust & Privacy' className='space-y-1'>
      <a href='/trust' className='block px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800'>Trust Center</a>
      <a href='/legal/privacy' className='block px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800'>Privacy & DPA</a>
      <a href='/app/trust/transparency' className='block px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800'>Transparency Dashboard</a>
      <a href='/app/trust/audit-logs' className='block px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800'>Audit Logs</a>
      <a href='/app/trust/residency' className='block px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800'>Data Residency</a>
      <a href='/app/settings/retention' className='block px-3 py-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800'>Retention</a>
    </nav>
  )
}
