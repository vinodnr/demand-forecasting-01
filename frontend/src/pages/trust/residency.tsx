'use client'
import React, {useEffect, useState} from 'react'
import Header from '../../components/Header'
import DataResidencyCard from '../../components/trust/DataResidencyCard'

export default function Residency(){
  const [meta, setMeta] = useState(null)
  useEffect(()=>{ fetch('/v1/org/metadata').then(r=>r.json()).then(setMeta).catch(()=>setMeta(null)) },[])
  return (
    <div className='min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100'>
      <Header />
      <main role='main' id='main' className='max-w-4xl mx-auto p-6'>
        <h1 className='text-3xl font-bold'>Data Residency</h1>
        <p className='mt-2 text-sm'>Where your data is stored and the guarantees we provide.</p>
        <DataResidencyCard meta={meta} />
      </main>
    </div>
  )
}
