'use client'
import React from 'react'
import Link from 'next/link'
export default function Sidebar(){ 
  return (
    <aside role='navigation' className='w-64 border-r dark:border-gray-700 bg-white dark:bg-gray-900 min-h-screen p-4 hidden md:block'>
      <div className='mb-6'>
        <div className='w-10 h-10 bg-gray-200 dark:bg-gray-700 rounded-full flex items-center justify-center font-bold'>B</div>
        <div className='mt-2 text-sm font-semibold'>{process.env.NEXT_PUBLIC_COMPANY_NAME || 'Your Brand'}</div>
      </div>
      <nav className='space-y-2 text-sm'>
        <Link href='/' className='block py-2 px-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800'>Home</Link>
        <Link href='/app/trust/transparency' className='block py-2 px-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800'>Transparency</Link>
        <Link href='/app/trust/audit-logs' className='block py-2 px-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800'>Audit Logs</Link>
        <Link href='/app/trust/residency' className='block py-2 px-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800'>Residency</Link>
        <Link href='/app/settings/retention' className='block py-2 px-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800'>Retention</Link>
        <Link href='/app/settings/delete-org' className='block py-2 px-2 rounded text-red-600 hover:bg-gray-100 dark:hover:bg-gray-800'>Delete Org</Link>
        <Link href='/trust' className='block py-2 px-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800'>Trust Center</Link>
        <Link href='/legal/privacy' className='block py-2 px-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800'>Privacy Policy</Link>
      </nav>
    </aside>
  )
}
