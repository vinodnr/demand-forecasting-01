'use client'
import React from 'react'
import ProtectedRoute from '../../components/ProtectedRoute'
import DeleteOrg from '../../pages/settings/delete-org'

export default function Page(){ return (<ProtectedRoute><DeleteOrg /></ProtectedRoute>) }
