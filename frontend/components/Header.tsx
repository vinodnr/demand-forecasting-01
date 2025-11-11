'use client'
import React from 'react'
import ThemeToggle from './ThemeToggle'

export default function Header({companyName}:{companyName?:string}){
  const brand = companyName || process.env.NEXT_PUBLIC_COMPANY_NAME || 'Your Brand'
  return (
    <header className='flex items-center justify-between p-4 border-b bg-white dark:bg-gray-900 dark:border-gray-700'>
      <div className='flex items-center space-x-3'>
        <div className='w-10 h-10 bg-gray-200 dark:bg-gray-700 rounded-full flex items-center justify-center'>
          {/* Placeholder logo image */}
          <span className='text-gray-600 dark:text-gray-200 font-bold'>B</span>
        </div>
        <div>
          <div className='text-lg font-semibold text-gray-800 dark:text-gray-100'>{brand}</div>
          <div className='text-sm text-gray-500 dark:text-gray-400'>Dashboard</div>
        </div>
      </div>
      <div className='flex items-center space-x-4'>
        <nav className='hidden sm:flex space-x-4 text-sm'>
          <a href='/' className='hover:underline'>Home</a>
          <a href='/admin/AdminRoles' className='hover:underline'>Admin</a>
          <a href='/privacy' className='hover:underline'>Privacy</a>
        </nav>
        <ThemeToggle />
      </div>
    </header>
  )
}
