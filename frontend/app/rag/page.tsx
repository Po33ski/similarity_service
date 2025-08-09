'use client'
import { useState } from 'react'

export default function RagPage() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const ask = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setAnswer(null)
    const res = await fetch('/api/rag/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    })
    const data = await res.json()
    setAnswer(data.answer ?? JSON.stringify(data))
    setLoading(false)
  }

  return (
    <div>
      <h1>AI RAG</h1>
      <form onSubmit={ask} style={{ display: 'grid', gap: 8 }}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={5}
          placeholder="Twoje pytanie..."
        />
        <button disabled={loading || question.trim().length === 0} type="submit">
          {loading ? 'Czekaj...' : 'Zapytaj'}
        </button>
      </form>
      {answer && (
        <section style={{ marginTop: 16 }}>
          <h3>Odpowiedź</h3>
          <pre>{answer}</pre>
        </section>
      )}
    </div>
  )
}


