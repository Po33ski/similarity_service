import './globals.css'
import Link from 'next/link'
import { ReactNode } from 'react'

export const metadata = {
  title: 'IPUM Lab GUI',
  description: 'RAG and Similarity Service GUI',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pl">
      <body>
        <nav style={{ display: 'flex', gap: 16, padding: 16, borderBottom: '1px solid #eee' }}>
          <Link href="/">Home</Link>
          <Link href="/rag">AI RAG</Link>
          <Link href="/similarity">Similarity Service</Link>
        </nav>
        <main style={{ padding: 16 }}>{children}</main>
      </body>
    </html>
  )
}


