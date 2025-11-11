'use client'
import React from 'react'

export default function RetentionTable({plans}:{plans:any[]}){
  const defaults = plans && plans.length>0 ? plans : [{name:'Free',days:90},{name:'Pro',days:365},{name:'Business',days:1095}]
  return (
    <div className='p-4 bg-white dark:bg-gray-800 rounded shadow'>
      <table className='min-w-full'>
        <thead className='bg-gray-50 dark:bg-gray-700'><tr><th scope='col' className='px-4 py-2 text-left'>Plan</th><th scope='col' className='px-4 py-2 text-left'>Retention (days)</th></tr></thead>
        <tbody>{defaults.map((p:any)=> (<tr key={p.name}><td className='px-4 py-2'>{p.name}</td><td className='px-4 py-2'>{p.days}</td></tr>))}</tbody>
      </table>
    </div>
  )
}
