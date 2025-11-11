'use client'
import React from 'react'

export default function DataResidencyCard({meta}:{meta:any}){
  const region = meta?.region || 'US'
  const db = meta?.db_region || 'unknown'
  const r2 = meta?.r2_region || 'unknown'
  return (
    <div className='p-4 bg-white dark:bg-gray-800 rounded shadow'>
      <h2 className='text-xl font-semibold'>Your Org: {meta?.org_name || 'N/A'}</h2>
      <div className='mt-3 grid grid-cols-1 sm:grid-cols-2 gap-4'>
        <div className='p-3 border rounded'>
          <div className='text-sm font-medium'>Primary Region</div>
          <div className='text-lg'>{region}</div>
        </div>
        <div className='p-3 border rounded'>
          <div className='text-sm font-medium'>Database Region</div>
          <div className='text-lg'>{db}</div>
        </div>
        <div className='p-3 border rounded'>
          <div className='text-sm font-medium'>Object Storage Region</div>
          <div className='text-lg'>{r2}</div>
        </div>
      </div>
      <p className='mt-3 text-sm'>If you require stricter residency guarantees, contact support to arrange contractual terms.</p>
    </div>
  )
}
