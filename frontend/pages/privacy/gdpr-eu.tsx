'use client'
import React from 'react'
import Header from '../../components/Header'

export default function GDPR_EU(){
  return (<div className='min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100'>
    <Header />
    <main className='max-w-4xl mx-auto p-6'>
      <h1 className='text-2xl font-bold'>EU GDPR Policy (Placeholder)</h1>
      <p className='mt-4'>Full GDPR policy placeholder. Replace with your legal text or upload a PDF to serve here.</p>
      <div className='mt-6 p-4 bg-white dark:bg-gray-800 rounded shadow'>
        <p>This document explains the legal basis for processing, data subject rights, data retention, processors & subprocessors, and contact details for the Data Protection Officer (DPO).</p>
      </div>
    </main>
  </div>)
}
