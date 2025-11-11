import React from 'react'
import {render, screen} from '@testing-library/react'
import TrustCenter from '../../frontend/src/pages/trust/index'

test('renders Trust Center heading', ()=>{
  render(<TrustCenter />)
  expect(screen.getByText(/Trust Center/i)).toBeInTheDocument()
})
