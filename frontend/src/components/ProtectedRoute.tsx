'use client'
import React, {useEffect, useState} from 'react'
import {useRouter} from 'next/navigation'

async function fetchMe(withAuthHeader=false){
  const headers = {}
  if(withAuthHeader){
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
    if(token) headers['Authorization'] = 'Bearer ' + token
  }
  try{
    const res = await fetch('/v1/auth/me', {credentials: 'include', headers})
    if(res.ok) return await res.json()
    return null
  }catch(e){
    return null
  }
}

export default function ProtectedRoute({children}:{children:React.ReactNode}){
  const [authed, setAuthed] = useState<boolean|null>(null)
  const router = useRouter()
  useEffect(()=>{
    let mounted = true
    async function check(){
      // First try cookie-based session (credentials include)
      const me = await fetchMe(false)
      if(me){
        if(mounted) setAuthed(true)
        return
      }
      // If cookie check failed, try Bearer token from localStorage if present
      const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
      if(token){
        const me2 = await fetchMe(true)
        if(me2){
          if(mounted) setAuthed(true)
          return
        }
      }
      if(mounted){
        setAuthed(false)
        router.push('/login')
      }
    }
    check()
    return ()=>{ mounted=false }
  },[router])
  if(authed===null) return <div className='p-4'>Checking authentication...</div>
  if(!authed) return <div className='p-4'>Redirecting to login...</div>
  return <>{children}</>
}
