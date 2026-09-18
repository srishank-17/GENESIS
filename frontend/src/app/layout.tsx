import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'GENESIS - AI Adaptive Learning OS',
  description: 'AI that learns how you learn.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-slate-950 text-slate-50 antialiased">
        {children}
      </body>
    </html>
  );
}
