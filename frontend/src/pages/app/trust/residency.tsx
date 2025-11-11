'use client'
import React from 'react'
import ProtectedRoute from '../../components/ProtectedRoute'
import Residency from '../../pages/trust/residency'

export default function Page(){ return (<ProtectedRoute><Residency /></ProtectedRoute>) }
