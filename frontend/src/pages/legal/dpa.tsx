'use client'
import React from 'react'
import Header from '../../components/Header'

export default function DPA(){
  return (
    <div className='min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100'>
      <Header />
      <main role='main' id='main' className='max-w-4xl mx-auto p-6'>
        <h1 className='text-3xl font-bold'>Data Processing Addendum (DPA) — Draft</h1>
        <p className='mt-4'>This DPA outlines the processing, subprocessing, security measures, and obligations between Controller (Customer) and Processor (Service).</p>
        <section className='mt-6 bg-white dark:bg-gray-800 p-4 rounded shadow'>
          <h2 className='text-xl font-semibold'>1. Definitions</h2>
          <p className='text-sm mt-2'>Definitions used in this DPA align with EU GDPR: 'Personal Data', 'Processing', 'Data Subject', 'Controller', 'Processor'.</p>
        </section>
        <section className='mt-4 bg-white dark:bg-gray-800 p-4 rounded shadow'>
          <h2 className='text-xl font-semibold'>2. Subject Matter & Duration</h2>
          <p className='text-sm mt-2'>Processor will process personal data on behalf of Controller for the duration of the Agreement and as necessary to provide services.</p>
        </section>
        <section className='mt-4 bg-white dark:bg-gray-800 p-4 rounded shadow'>
          <h2 className='text-xl font-semibold'>3. Nature & Purpose</h2>
          <p className='text-sm mt-2'>Processing includes storage, analytics, forecasting, and support operations necessary to deliver the service.</p>
        </section>
        <section className='mt-4 bg-white dark:bg-gray-800 p-4 rounded shadow'>
          <h2 className='text-xl font-semibold'>4. Subprocessors</h2>
          <p className='text-sm mt-2'>A current list of subprocessors (hosting, storage, analytics, email) is published and updated. Customers may object in writing within 30 days.</p>
        </section>
        <section className='mt-4 bg-white dark:bg-gray-800 p-4 rounded shadow'>
          <h2 className='text-xl font-semibold'>5. Security Measures</h2>
          <ul className='list-disc ml-6 text-sm mt-2'>
            <li>Encryption at rest and in transit</li>
            <li>Access controls and least-privilege</li>
            <li>Regular vulnerability scans and patching</li>
          </ul>
        </section>
        <section className='mt-4'>
          <h2 className='text-lg font-semibold'>Contact</h2>
          <p className='text-sm'>Data Protection Officer: privacy@example.com</p>
        </section>
      </main>
    </div>
  )
}
