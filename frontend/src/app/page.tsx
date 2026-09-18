'use client';

import React, { useEffect, useState } from 'react';
import api from '../lib/api';

export default function Home() {
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function checkHealth() {
      try {
        const res = await api.get('/api/health');
        setHealth(res.data);
      } catch (err: any) {
        setHealth({ status: 'offline', error: err.message });
      } finally {
        setLoading(false);
      }
    }
    checkHealth();
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-gradient-to-b from-slate-950 to-slate-900 text-slate-100">
      <div className="z-10 max-w-4xl w-full items-center justify-between font-mono text-sm">
        <div className="text-center space-y-4">
          <div className="inline-block px-3 py-1 bg-indigo-500/10 border border-indigo-500/30 rounded-full text-indigo-400 text-xs font-semibold uppercase tracking-wider">
            Personal Learning Operating System
          </div>
          <h1 className="text-5xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400">
            GENESIS
          </h1>
          <p className="text-xl text-slate-400 max-w-2xl mx-auto">
            AI that learns how you learn. Dynamic knowledge graph, Bayesian mastery modeling, and root-cause diagnostic intelligence.
          </p>

          <div className="mt-8 p-6 bg-slate-900/80 border border-slate-800 rounded-xl shadow-2xl max-w-md mx-auto text-left">
            <h2 className="text-sm font-semibold text-slate-300 mb-3 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
              Core System Status
            </h2>
            {loading ? (
              <p className="text-xs text-slate-500">Checking system status...</p>
            ) : (
              <pre className="text-xs bg-slate-950 p-3 rounded border border-slate-800/80 text-emerald-400 overflow-x-auto">
                {JSON.stringify(health, null, 2)}
              </pre>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
