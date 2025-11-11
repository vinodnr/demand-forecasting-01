'use client'
import React, {useState} from 'react'
import Header from '../../components/Header'
import DeleteOrgConfirmModal from '../../components/trust/DeleteOrgConfirmModal'

export default function DeleteOrgPage(){
  const [show, setShow] = useState(false)
  return (
    <div className='min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100'>
      <Header />
      <main role='main' id='main' className='max-w-3xl mx-auto p-6'>
        <h1 className='text-2xl font-bold'>Delete Organization</h1>
        <p className='mt-2 text-sm'>This action is irreversible. Please ensure you have exported your data.</p>
        <div className='mt-4'>
          <button type='button' onClick={()=>setShow(true)} className='px-4 py-2 bg-red-600 text-white rounded'>Delete my organization</button>
        </div>
        {show && <DeleteOrgConfirmModal onClose={()=>setShow(false)} />}
      </main>
    </div>
  )
}
