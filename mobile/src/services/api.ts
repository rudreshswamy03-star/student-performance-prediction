/**
 * EduPredict AI API Client Service
 * Sapthagiri NPS University, Bengaluru
 */

import { Platform } from 'react-native';

// Standard Android emulator uses 10.0.2.2 to access host localhost.
// iOS simulator and Web use localhost.
const getBaseUrl = () => {
  if (Platform.OS === 'android') {
    return 'http://10.0.2.2:8000';
  }
  return 'http://localhost:8000';
};

export const API_BASE_URL = getBaseUrl();

let authToken: string | null = null;

export const setAuthToken = (token: string | null) => {
  authToken = token;
};

const request = async (endpoint: string, options: RequestInit = {}) => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (authToken) {
    headers['Authorization'] = `Bearer ${authToken}`;
  }

  try {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'API Error' }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }
    return await res.json();
  } catch (error: any) {
    console.warn(`[API] Fallback for ${endpoint}:`, error.message);
    throw error;
  }
};

export const ApiService = {
  // Authentication
  login: async (email: string, password: string) => {
    return request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  },

  register: async (userData: any) => {
    return request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  },

  getProfile: async () => {
    return request('/api/auth/me');
  },

  getNotifications: async () => {
    return request('/api/auth/notifications');
  },

  // Student Profiles & Cohort
  getMyStudentProfile: async () => {
    return request('/api/students/me');
  },

  getStudents: async (params: { search?: string; section?: string; risk?: string } = {}) => {
    const query = new URLSearchParams();
    if (params.search) query.append('search', params.search);
    if (params.section) query.append('section', params.section);
    if (params.risk) query.append('risk', params.risk);
    return request(`/api/students?${query.toString()}`);
  },

  getStudentById: async (id: string) => {
    return request(`/api/students/${id}`);
  },

  // Academics & Subjects
  getSubjects: async () => {
    return request('/api/academics/subjects');
  },

  getCohortAnalytics: async () => {
    return request('/api/academics/analytics');
  },

  getStudentReport: async (studentId: string) => {
    return request(`/api/academics/report/${studentId}`);
  },

  // Machine Learning Prediction
  predictPerformance: async (data: any) => {
    return request('/api/predict', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // Early Academic Warning System
  getEarlyWarningRoster: async (tier?: string) => {
    const query = tier ? `?tier=${tier}` : '';
    return request(`/api/early-warning${query}`);
  },

  // Faculty & Admin
  getFacultyDashboard: async () => {
    return request('/api/faculty/dashboard');
  },

  getAdminMetrics: async () => {
    return request('/api/admin/metrics');
  },
};
