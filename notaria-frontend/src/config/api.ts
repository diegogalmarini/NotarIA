// API Configuration - Updated for Vercel deployment
const DEFAULT_LOCAL = 'http://localhost:8000';

// In client-side (browser), prefer same-origin relative calls when NEXT_PUBLIC_API_URL is not set
// In server-side (build/SSR), fall back to local dev URL
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? (typeof window !== 'undefined' ? '' : DEFAULT_LOCAL);

export const getApiUrl = (endpoint: string) => `${API_BASE_URL}${endpoint}`;

// Force redeploy - Vercel deployment fix 2025-11-13 21:58:50

