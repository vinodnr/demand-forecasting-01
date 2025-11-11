'use client'
import {useEffect, useState} from 'react'
export default function useTrustData(ttl=60000){ // 60s default
  const [meta, setMeta] = useState(null)
  const [stats, setStats] = useState(null)
  const [logs, setLogs] = useState([])
  useEffect(()=>{
    let mounted = true
    async function fetchAll(){
      try{ const m = await fetch('/v1/org/metadata').then(r=>r.json()); if(mounted) setMeta(m) }catch(e){}
      try{ const s = await fetch('/v1/datasets/stats').then(r=>r.json()); if(mounted) setStats(s) }catch(e){}
      try{ const l = await fetch('/v1/logs?limit=20').then(r=>r.json()); if(mounted) setLogs(l) }catch(e){}
    }
    fetchAll()
    const id = setInterval(fetchAll, ttl)
    return ()=>{ mounted=false; clearInterval(id) }
  },[ttl])
  return {meta, stats, logs}
}
