import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

type UrlItem = {
  id?: number | string;
  original_url?: string;
  short_code?: string;
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
      await axios.post(`${API_BASE}/shorten`, { original_url: originalUrl });
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

  const deleteUrl = async (shortCode?: string) => {
    if (!shortCode) {
      setMessage('Invalid short code.');
      setTimeout(() => setMessage(''), 3000);
      return;
    }

    try {
      await axios.delete(`${API_BASE}/delete/${shortCode}`);
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
    <main className="relative mx-auto flex min-h-screen w-full max-w-7xl items-center px-4 py-10 sm:px-6 lg:px-8">
      <section className="relative w-full overflow-hidden rounded-[2.5rem] border border-white/70 bg-white/75 shadow-[0_28px_90px_rgba(255,190,145,0.22)] backdrop-blur">
        <div className="grid gap-6 border-b border-amber-200/70 bg-gradient-to-r from-[#FFBE91] via-[#FFDDB0] to-[#CFEBFF] p-7 sm:p-10 lg:grid-cols-[1.15fr_0.85fr] lg:items-end">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.35em] text-[#6a4c2c]">Smart link shortening</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight text-[#4f3422] sm:text-4xl">
              Turn long URLs into tidy links.
            </h1>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-[#5c4534] sm:text-base">
              Paste a link, shorten it, and manage every generated URL in a clean table.
            </p>
          </div>

          <form className="flex flex-col gap-3 rounded-[1.75rem] bg-white/72 p-4 shadow-sm ring-1 ring-white/60 sm:flex-row" onSubmit={handleSubmit}>
            <input
              type="url"
              value={originalUrl}
              onChange={(e) => setOriginalUrl(e.target.value)}
              placeholder="https://example.com/very/long/path"
              className="min-w-0 flex-1 rounded-2xl border border-amber-200 bg-white px-4 py-3 text-sm text-[#4f3422] outline-none transition placeholder:text-[#b08a6d] focus:border-[#FFBE91] focus:ring-2 focus:ring-[#CFEBFF]"
            />
            <button
              className="inline-flex items-center justify-center rounded-2xl bg-[#FFBE91] px-5 py-3 text-sm font-semibold text-[#4f3422] transition hover:-translate-y-0.5 hover:shadow-md disabled:cursor-not-allowed disabled:opacity-60"
              type="submit"
              disabled={loading}
            >
              {loading ? 'Shortening...' : 'Shorten'}
            </button>
          </form>
        </div>

        <div className="p-5 sm:p-7">
          {message ? (
            <div className="mb-4 rounded-2xl border border-[#CFEBFF] bg-[#CFEBFF]/50 px-4 py-3 text-sm font-medium text-[#24506f]">
              {message}
            </div>
          ) : null}

          <div className="overflow-x-auto rounded-[1.75rem] border border-amber-200 bg-white shadow-sm">
            <table className="min-w-full divide-y divide-amber-100 text-left">
              <thead className="bg-[#FFFCE1]">
                <tr>
                  <th className="px-4 py-4 text-xs font-bold uppercase tracking-[0.24em] text-[#6a4c2c]">Original URL</th>
                  <th className="px-4 py-4 text-xs font-bold uppercase tracking-[0.24em] text-[#6a4c2c]">Short URL</th>
                  <th className="px-4 py-4 text-xs font-bold uppercase tracking-[0.24em] text-[#6a4c2c]">Code</th>
                  <th className="px-4 py-4 text-xs font-bold uppercase tracking-[0.24em] text-[#6a4c2c]">Actions</th>
                </tr>
              </thead>

              <tbody className="divide-y divide-amber-100 bg-white">
                {urls.length === 0 ? (
                  <tr>
                    <td className="px-4 py-8 text-center text-sm text-[#73543c]" colSpan={4}>
                      No links yet. Create your first short URL.
                    </td>
                  </tr>
                ) : (
                  urls.map((item, index) => (
                    <tr key={item.id ?? index} className="hover:bg-[#FFFCE1]/60">
                      <td className="max-w-[24rem] px-4 py-4 text-sm text-[#4f3422]">
                        <span className="block truncate font-medium">{item.original_url || 'Untitled link'}</span>
                      </td>
                      <td className="px-4 py-4 text-sm text-[#5f77a8]">
                        <a
                          className="break-all font-medium underline decoration-[#CFEBFF] decoration-2 underline-offset-4 hover:text-[#24506f]"
                          href={item.short_url}
                          target="_blank"
                          rel="noreferrer"
                        >
                          {item.short_url || 'Generating...'}
                        </a>
                      </td>
                      <td className="px-4 py-4 text-sm text-[#4f3422]">{item.short_code || '-'}</td>
                      <td className="px-4 py-4">
                        <div className="flex flex-wrap gap-2">
                          <button
                            type="button"
                            className="rounded-full bg-[#CFEBFF] px-4 py-2 text-sm font-semibold text-[#1f2d39] transition hover:-translate-y-0.5 hover:shadow-sm"
                            onClick={() => copyToClipboard(item.short_url)}
                          >
                            Copy
                          </button>
                          <button
                            type="button"
                            className="rounded-full bg-[#FFFCE1] px-4 py-2 text-sm font-semibold text-[#6a4c2c] transition hover:-translate-y-0.5 hover:shadow-sm"
                            onClick={() => deleteUrl(item.short_code)}
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </main>
  );
}