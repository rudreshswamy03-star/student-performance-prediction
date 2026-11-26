import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { ApiService, setAuthToken } from '../services/api';

export interface User {
  id?: number | string;
  name: string;
  email: string;
  role: 'student' | 'faculty' | 'admin';
  student_id?: string;
  department?: string;
  section?: string;
  semester?: number;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
  quickLogin: (role: 'student' | 'faculty' | 'admin') => Promise<void>;
  setUserProfile: (user: User) => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  isLoading: true,
  login: async () => false,
  logout: async () => {},
  quickLogin: async () => {},
  setUserProfile: () => {},
});

export const DEMO_USERS: Record<string, { email: string; pass: string; user: User }> = {
  student: {
    email: 'student@sapthagiri.edu.in',
    pass: 'Student@123',
    user: {
      name: 'Aditya Rao',
      email: 'student@sapthagiri.edu.in',
      role: 'student',
      student_id: 'SNPSU2024CS042',
      department: 'Computer Science and Engineering',
      section: 'A',
      semester: 5,
    },
  },
  faculty: {
    email: 'faculty@sapthagiri.edu.in',
    pass: 'Faculty@123',
    user: {
      name: 'Dr. Suresh Kumar',
      email: 'faculty@sapthagiri.edu.in',
      role: 'faculty',
      department: 'Computer Science and Engineering',
      semester: 5,
    },
  },
  admin: {
    email: 'admin@sapthagiri.edu.in',
    pass: 'Admin@123',
    user: {
      name: 'Prof. Ramesh Rao (HoD CSE)',
      email: 'admin@sapthagiri.edu.in',
      role: 'admin',
      department: 'Computer Science and Engineering',
    },
  },
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    // Check local storage session
    const checkSession = async () => {
      try {
        const storedToken = await AsyncStorage.getItem('edupredict_token');
        const storedUser = await AsyncStorage.getItem('edupredict_user');
        if (storedToken && storedUser) {
          setAuthToken(storedToken);
          setToken(storedToken);
          setUser(JSON.parse(storedUser));
        }
      } catch (e) {
        console.warn('Storage read error:', e);
      } finally {
        setIsLoading(false);
      }
    };
    checkSession();
  }, []);

  const login = async (email: string, password: string): Promise<boolean> => {
    setIsLoading(true);
    try {
      // 1. Try real backend
      const res = await ApiService.login(email, password);
      if (res && res.access_token) {
        setAuthToken(res.access_token);
        setToken(res.access_token);
        setUser(res.user);
        await AsyncStorage.setItem('edupredict_token', res.access_token);
        await AsyncStorage.setItem('edupredict_user', JSON.stringify(res.user));
        return true;
      }
    } catch (err: any) {
      console.warn('Backend login error, attempting offline demo fallback:', err.message);
      // Demo fallback match
      for (const key of Object.keys(DEMO_USERS)) {
        const demo = DEMO_USERS[key];
        if (demo.email.toLowerCase() === email.toLowerCase()) {
          const fakeToken = `offline_token_${key}`;
          setAuthToken(fakeToken);
          setToken(fakeToken);
          setUser(demo.user);
          await AsyncStorage.setItem('edupredict_token', fakeToken);
          await AsyncStorage.setItem('edupredict_user', JSON.stringify(demo.user));
          return true;
        }
      }
    } finally {
      setIsLoading(false);
    }
    return false;
  };

  const quickLogin = async (role: 'student' | 'faculty' | 'admin') => {
    const demo = DEMO_USERS[role];
    if (demo) {
      await login(demo.email, demo.pass);
    }
  };

  const logout = async () => {
    setAuthToken(null);
    setToken(null);
    setUser(null);
    try {
      await AsyncStorage.removeItem('edupredict_token');
      await AsyncStorage.removeItem('edupredict_user');
    } catch (e) {
      // Ignore
    }
  };

  const setUserProfile = (updatedUser: User) => {
    setUser(updatedUser);
    AsyncStorage.setItem('edupredict_user', JSON.stringify(updatedUser)).catch(() => {});
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        login,
        logout,
        quickLogin,
        setUserProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
