'use client'
import React from 'react'
import Header from '../components/Header'
import TrustNav from '../components/trust/TrustNav'

export default function AppLayout({children}:{children: React.ReactNode}){
  return (
    <div className='min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100'>
      <Header />
      <div className='max-w-7xl mx-auto p-4 grid grid-cols-1 md:grid-cols-4 gap-6'>
        <aside className='md:col-span-1 bg-white dark:bg-gray-800 p-4 rounded shadow'>
          <TrustNav />
        </aside>
        <main role='main' id='main' className='md:col-span-3'>
          {children}
        </main>
      </div>
    </div>
  )
}
