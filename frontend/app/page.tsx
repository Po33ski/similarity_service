import Link from 'next/link'

export default function Home() {
  return (
    <div>
      <h1>IPUM Lab GUI</h1>
      <p>Wybierz moduł:</p>
      <ul>
        <li><Link href="/rag">AI RAG</Link></li>
        <li><Link href="/similarity">Similarity Service</Link></li>
      </ul>
    </div>
  )
}


