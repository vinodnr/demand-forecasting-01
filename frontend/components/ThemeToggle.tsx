'use client'
import React, {useEffect, useState} from 'react'

export default function ThemeToggle(){
  const [theme, setTheme] = useState('light')
  useEffect(()=>{
    try{
      const saved = localStorage.getItem('theme') || 'light'
      setTheme(saved)
      if(saved === 'dark') document.documentElement.classList.add('dark')
      else document.documentElement.classList.remove('dark')
    }catch(e){}
  },[])
  function toggle(){
    const next = theme === 'dark' ? 'light' : 'dark'
    setTheme(next)
    try{ localStorage.setItem('theme', next) }catch(e){} 
    if(next === 'dark') document.documentElement.classList.add('dark')
    else document.documentElement.classList.remove('dark')
  }
  return (<button onClick={toggle} className='p-2 rounded bg-gray-100 dark:bg-gray-800'>
    {theme === 'dark' ? '🌙 Dark' : '☀️ Light'}
  </button>)
}
