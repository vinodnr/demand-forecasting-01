'use client'
import React from 'react'
import Header from '../../components/Header'

export default function PrivacyPolicy(){
  return (
    <div className='min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100'>
      <Header />
      <main role='main' id='main' className='max-w-4xl mx-auto p-6'>
        <h1 className='text-3xl font-bold'>Privacy Policy & Data Processing Addendum (DPA)</h1>
        <p className='mt-4'>This is a plain-language summary. For the full legal DPA and subprocessors list, download the PDFs below.</p>
        <div className='mt-6 grid gap-4 grid-cols-1 sm:grid-cols-2'>
          <a className='p-4 bg-white dark:bg-gray-800 rounded shadow block' href='#' download>
            <h3 className='font-semibold'>Download: Data Processing Addendum (DPA)</h3>
            <p className='text-sm mt-2'>Covers processing details, data exporter/importer roles, and subprocessors.</p>
          </a>
          <a className='p-4 bg-white dark:bg-gray-800 rounded shadow block' href='#' download>
            <h3 className='font-semibold'>Download: Subprocessors List</h3>
            <p className='text-sm mt-2'>Third-party subprocessors we use (hosting, analytics, email).</p>
          </a>
        </div>

        <section className='mt-6 bg-white dark:bg-gray-800 p-4 rounded shadow'>
          <h2 className='text-xl font-semibold'>Your rights</h2>
          <ul className='list-disc ml-6 mt-2 text-sm'>
            <li>Access your personal data</li>
            <li>Request correction or deletion</li>
            <li>Object to processing under certain conditions</li>
          </ul>
        </section>
      </main>
    </div>
  )
}
