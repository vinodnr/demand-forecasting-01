'use client'
import React from 'react'
import ProtectedRoute from '../../components/ProtectedRoute'
import Retention from '../../pages/settings/retention'

export default function Page(){ return (<ProtectedRoute><Retention /></ProtectedRoute>) }
