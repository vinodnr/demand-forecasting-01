'use client'
import React, {useState} from 'react'
import Header from '../components/Header'

export default function PrivacyPage(){
  const [status, setStatus] = useState('')
  async function requestDelete(){
    if(!confirm('Are you sure you want to request deletion of your data? This action is irreversible.')) return;
    setStatus('Requesting...')
    try{
      const res = await fetch('/v1/privacy/delete-request', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ /* user identification handled by auth */ })})
      const data = await res.json()
      setStatus(JSON.stringify(data))
    }catch(e){
      setStatus('Error: ' + String(e))
    }
  }
  return (<div className='min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100'>
    <Header />
    <main className='max-w-4xl mx-auto p-6'>
      <h1 className='text-3xl font-bold'>Privacy & Data Protection</h1>
      <p className='mt-4'>This page contains a summary of our data protection and GDPR-related policies for users in the US and EU. Below is a short summary; full legal texts are available for download.</p>
      <section className='mt-6 bg-white dark:bg-gray-800 p-4 rounded shadow'>
        <h2 className='text-xl font-semibold'>EU (GDPR) Summary</h2>
        <ul className='list-disc ml-6 mt-2'>
          <li>Right to access personal data</li>
          <li>Right to rectification, erasure ('right to be forgotten')</li>
          <li>Right to restrict processing and data portability</li>
          <li>Right to object to processing and automated decision-making</li>
        </ul>
        <p className='mt-2 text-sm'>We process personal data as described in our full GDPR policy below. To download the full GDPR policy, click the button below.</p>
        <div className='mt-3'>
          <a href='/privacy/gdpr-eu' className='underline mr-3'>Download EU GDPR policy (PDF)</a>
          <a href='/privacy/gdpr-us' className='underline'>Download US privacy summary (PDF)</a>
        </div>
      </section>

      <section className='mt-6 bg-white dark:bg-gray-800 p-4 rounded shadow'>
        <h2 className='text-xl font-semibold'>US Privacy Summary</h2>
        <p className='mt-2'>We comply with applicable US privacy regulations. For California residents, we honor CCPA-style data subject requests including access, deletion, and opt-out options.</p>
      </section>

      <section className='mt-6 bg-white dark:bg-gray-800 p-4 rounded shadow'>
        <h2 className='text-xl font-semibold'>Delete my data</h2>
        <p className='mt-2'>If you choose not to continue, you may request deletion of your personal data. This will remove your data from our systems where possible and schedule permanent deletion of backups per our retention policy.</p>
        <button onClick={requestDelete} className='mt-3 px-4 py-2 bg-red-600 text-white rounded'>Request Data Deletion</button>
        <div className='mt-3 text-sm'>Status: {status}</div>
      </section>

      <section className='mt-6 text-sm'>
        <p>Placeholder brand assets: a generic logo and brand name are shown until you upload your own. To change the company name, set NEXT_PUBLIC_COMPANY_NAME env var in your frontend build.</p>
      </section>
    </main>
  </div>)
}
