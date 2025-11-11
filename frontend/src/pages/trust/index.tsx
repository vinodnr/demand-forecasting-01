'use client'
import React from 'react'
import Link from 'next/link'
import Header from '../../components/Header'

export default function TrustCenter(){
  return (
    <div className='min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100'>
      <Header />
      <main role='main' id='main' className='max-w-5xl mx-auto p-6'>
        <h1 className='text-4xl font-bold'>Trust Center</h1>
        <p className='mt-4 text-lg'>We prioritise security, privacy and transparency. Below are our commitments, compliance artifacts, and operational transparency tools.</p>

        <section className='mt-6 grid gap-4 grid-cols-1 sm:grid-cols-2'>
          <div className='p-4 bg-white dark:bg-gray-800 rounded shadow'>
            <h2 className='text-xl font-semibold'>Security & SOC2</h2>
            <p className='mt-2 text-sm'>We follow SOC2 principles – controls for security, availability, and confidentiality. Contact us for SOC2 reports.</p>
            <Link href='/trust/transparency' className='mt-3 inline-block text-sm text-blue-600 dark:text-blue-400'>View transparency dashboard →</Link>
          </div>
          <div className='p-4 bg-white dark:bg-gray-800 rounded shadow'>
            <h2 className='text-xl font-semibold'>Data Residency</h2>
            <p className='mt-2 text-sm'>Choose where your data is stored: US or EU. Learn more about our residency guarantees and encryption.</p>
            <Link href='/trust/residency' className='mt-3 inline-block text-sm text-blue-600 dark:text-blue-400'>View residency details →</Link>
          </div>
          <div className='p-4 bg-white dark:bg-gray-800 rounded shadow'>
            <h2 className='text-xl font-semibold'>Privacy & DPA</h2>
            <p className='mt-2 text-sm'>Review our privacy policy and download the Data Processing Agreement for enterprise customers.</p>
            <Link href='/legal/privacy' className='mt-3 inline-block text-sm text-blue-600 dark:text-blue-400'>Read privacy policy →</Link>
          </div>
          <div className='p-4 bg-white dark:bg-gray-800 rounded shadow'>
            <h2 className='text-xl font-semibold'>Uptime & Incidents</h2>
            <p className='mt-2 text-sm'>We track service availability and publish past incidents and uptimes.</p>
            <a href='#' className='mt-3 inline-block text-sm text-blue-600 dark:text-blue-400'>View status page →</a>
          </div>
        </section>

        <section className='mt-8'>
          <h2 className='text-2xl font-semibold'>Compliance artifacts</h2>
          <ul className='mt-3 list-disc ml-6 text-sm'>
            <li>SOC2 report (available on request)</li>
            <li>Data Processing Addendum (DPA) — <a href='/legal/privacy' className='underline'>download</a></li>
            <li>Subprocessors list — <a href='/legal/privacy' className='underline'>download</a></li>
          </ul>
        </section>
      </main>
    </div>
  )
}
