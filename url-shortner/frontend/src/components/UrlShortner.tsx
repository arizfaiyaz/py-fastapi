import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

type UrlItem = {
  id?: number | string;
  original_url?: string;
  short_url?: string;
};

export function UrlShortner() {
  const [originalUrl, setOriginalUrl] = useState('');
  const [urls, setUrls] = useState<UrlItem[]>([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchUrls = async () => {
    try {
      const res = await axios.get(`${API_BASE}/all`);
      setUrls(res.data);
    } catch (error) {
      console.error('Error fetching URLs:', error);
    }
  };

  useEffect(() => {
    fetchUrls();
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!originalUrl.trim()) {
      setMessage('Please enter a URL to shorten.');
      setTimeout(() => setMessage(''), 3000);
      return;
    }

    setLoading(true);
    try {
      await axios.post(`${API_BASE}/shorten`, { url: originalUrl });
      setMessage('URL shortened successfully!');
      setOriginalUrl('');
      fetchUrls();
    } catch (error) {
      console.error('Error shortening URL:', error);
      setMessage('Error shortening URL.');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 3000);
    }
  };

  const copyToClipboard = (shortUrl?: string) => {
    if (!shortUrl) return;
    navigator.clipboard.writeText(shortUrl);
    setMessage('Copied to clipboard!');
    setTimeout(() => setMessage(''), 3000);
  };

  const deleteUrl = async (id?: number | string) => {
    if (!id) {
      setMessage('Invalid URL ID.');
      setTimeout(() => setMessage(''), 3000);
      return;
    }

    try {
      await axios.delete(`${API_BASE}/delete/${id}`);
      setMessage('URL deleted successfully!');
      fetchUrls();
    } catch (error) {
      console.error('Error deleting URL:', error);
      setMessage('Error deleting URL.');
    } finally {
      setTimeout(() => setMessage(''), 3000);
    }
  };

  return (
    <div className="shortener-shell">
      <div className="shortener-card">
        <div className="hero-panel">
          <p className="eyebrow">Smart link shortening</p>
          <h1>Turn long URLs into tidy links.</h1>
          <p>Paste a link, shorten it, and share it instantly.</p>
        </div>

        <form className="shortener-form" onSubmit={handleSubmit}>
          <input
            type="url"
            value={originalUrl}
            onChange={(e) => setOriginalUrl(e.target.value)}
            placeholder="https://example.com/very/long/path"
          />
          <button className="primary" type="submit" disabled={loading}>
            {loading ? 'Shortening...' : 'Shorten'}
          </button>
        </form>

        {message ? <div className="helper-text">{message}</div> : null}

        <div className="url-list">
          {urls.length === 0 ? (
            <div className="empty-state">No links yet. Create your first short URL.</div>
          ) : (
            urls.map((item, index) => (
              <div className="url-item" key={item.id ?? index}>
                <div className="url-content">
                  <strong>{item.original_url || 'Untitled link'}</strong>
                  <span>{item.short_url || 'Generating...'}</span>
                </div>
                <div className="url-actions">
                  <button type="button" className="secondary" onClick={() => copyToClipboard(item.short_url)}>
                    Copy
                  </button>
                  <button type="button" className="ghost" onClick={() => deleteUrl(item.id)}>
                    Delete
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}