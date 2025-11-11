'use client'
import React, {useEffect, useState} from 'react'
import Header from '../../components/Header'
import TransparencyStats from '../../components/trust/TransparencyStats'

export default function Transparency(){
  const [meta, setMeta] = useState(null)
  const [stats, setStats] = useState(null)
  useEffect(()=>{
    async function fetchAll(){
      try{
        const m = await fetch('/v1/org/metadata').then(r=>r.json())
        setMeta(m)
      }catch(e){ setMeta(null) }
      try{
        const s = await fetch('/v1/datasets/stats').then(r=>r.json())
        setStats(s)
      }catch(e){ setStats(null) }
    }
    fetchAll()
    const t = setInterval(fetchAll, 60000)
    return ()=>clearInterval(t)
  },[])
  return (
    <div className='min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100'>
      <Header />
      <main role='main' id='main' className='max-w-5xl mx-auto p-6'>
        <h1 className='text-3xl font-bold'>Transparency Dashboard</h1>
        <p className='mt-2 text-sm'>Live view of your org's location, usage and retention clocks.</p>
        <TransparencyStats meta={meta} stats={stats} />
      </main>
    </div>
  )
}
