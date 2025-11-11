'use client'
import React, {useEffect, useState} from 'react'
import Header from '../../components/Header'
import RetentionTable from '../../components/trust/RetentionTable'

export default function RetentionView(){
  const [plans, setPlans] = useState([])
  useEffect(()=>{ fetch('/v1/org/metadata').then(r=>r.json()).then(m=>setPlans(m?.plans || [])).catch(()=>setPlans([])) },[])
  return (
    <div className='min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100'>
      <Header />
      <main role='main' id='main' className='max-w-4xl mx-auto p-6'>
        <h1 className='text-3xl font-bold'>Retention Policy</h1>
        <p className='mt-2 text-sm'>Retention windows are defined per plan. Below are default values; enterprise customers can request custom retention.</p>
        <RetentionTable plans={plans} />
      </main>
    </div>
  )
}
