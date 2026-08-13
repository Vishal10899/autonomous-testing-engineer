"use client";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getAuthToken } from './api';

export function useAuth(requireAuth = true) {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getAuthToken();
    if (requireAuth && !token) {
      router.push('/login');
    } else {
      setIsAuthenticated(Boolean(token));
    }
    setLoading(false);
  }, [requireAuth, router]);

  return { isAuthenticated, loading };
}
