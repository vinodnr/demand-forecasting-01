'use client'
import React from 'react'

export default function TransparencyStats({meta, stats}:{meta:any, stats:any}){
  return (
    <div className='grid grid-cols-1 sm:grid-cols-3 gap-4 mt-4'>
      <div className='p-4 bg-white dark:bg-gray-800 rounded shadow'>
        <div className='text-sm font-medium'>Region</div>
        <div className='text-lg'>{meta?.region || 'US'}</div>
        <div className='text-sm text-gray-600 mt-1'>DB: {meta?.db_region || 'unknown'}</div>
      </div>
      <div className='p-4 bg-white dark:bg-gray-800 rounded shadow'>
        <div className='text-sm font-medium'>Datasets</div>
        <div className='text-lg'>{stats?.dataset_count ?? '—'}</div>
        <div className='text-sm text-gray-600 mt-1'>Storage: {stats?.storage_bytes ? Math.round(stats.storage_bytes/1024/1024) + ' MB' : '—'}</div>
      </div>
      <div className='p-4 bg-white dark:bg-gray-800 rounded shadow'>
        <div className='text-sm font-medium'>Forecasts</div>
        <div className='text-lg'>{stats?.forecast_count ?? '—'}</div>
        <div className='text-sm text-gray-600 mt-1'>Next purge: {stats?.next_purge || 'scheduled'}</div>
      </div>
    </div>
  )
}
