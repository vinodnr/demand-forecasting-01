'use client'
import React from 'react'
import ProtectedRoute from '../../components/ProtectedRoute'
import AuditLogs from '../../pages/trust/audit-logs'

export default function Page(){ return (<ProtectedRoute><AuditLogs /></ProtectedRoute>) }
