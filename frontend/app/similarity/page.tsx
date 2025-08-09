'use client'
import { useState } from 'react'

type Game = {
  id: number
  name: string
  price: number
  windows: boolean
  linux: boolean
  mac: boolean
  description: string
}

export default function SimilarityPage() {
  const [description, setDescription] = useState('')
  const [maxPrice, setMaxPrice] = useState<string>('')
  const [limit, setLimit] = useState<number>(5)
  const [windows, setWindows] = useState<boolean | undefined>(undefined)
  const [linux, setLinux] = useState<boolean | undefined>(undefined)
  const [mac, setMac] = useState<boolean | undefined>(undefined)
  const [results, setResults] = useState<Game[]>([])
  const [loading, setLoading] = useState(false)

  const toggle = (setter: (v: boolean | undefined) => void, value: boolean) => {
    setter((prev) => (prev === value ? undefined : value))
  }

  const search = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    const payload: any = {
      description,
      limit,
    }
    if (maxPrice) payload.max_price = Number(maxPrice)
    if (windows !== undefined) payload.windows = windows
    if (linux !== undefined) payload.linux = linux
    if (mac !== undefined) payload.mac = mac

    const res = await fetch('/api/similarity/games/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    const data = await res.json()
    setResults(Array.isArray(data) ? data : [])
    setLoading(false)
  }

  return (
    <div>
      <h1>Similarity Service</h1>
      <form onSubmit={search} style={{ display: 'grid', gap: 8, maxWidth: 600 }}>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={4}
          placeholder="Opis gry..."
        />
        <div style={{ display: 'flex', gap: 8 }}>
          <input
            type="number"
            min={1}
            max={50}
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
          />
          <input
            type="number"
            step="0.01"
            placeholder="Max cena"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
          />
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button
            type="button"
            onClick={() => toggle(setWindows, true)}
            style={{ background: windows === true ? '#ddd' : undefined }}
          >
            Windows
          </button>
          <button
            type="button"
            onClick={() => toggle(setLinux, true)}
            style={{ background: linux === true ? '#ddd' : undefined }}
          >
            Linux
          </button>
          <button
            type="button"
            onClick={() => toggle(setMac, true)}
            style={{ background: mac === true ? '#ddd' : undefined }}
          >
            Mac
          </button>
        </div>
        <button disabled={loading || description.trim().length === 0} type="submit">
          {loading ? 'Szukam...' : 'Szukaj'}
        </button>
      </form>

      <ul style={{ marginTop: 16, display: 'grid', gap: 8 }}>
        {results.map((g) => (
          <li key={g.id} style={{ border: '1px solid #eee', padding: 12, borderRadius: 6 }}>
            <strong>{g.name}</strong> — {g.price?.toFixed?.(2)} $
            <div>{g.description}</div>
            <div style={{ fontSize: 12, opacity: 0.7 }}>
              Win: {String(g.windows)} | Linux: {String(g.linux)} | Mac: {String(g.mac)}
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}


