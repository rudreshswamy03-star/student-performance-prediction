import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
} from 'react-native';
import { Colors } from '../theme/colors';
import { useAuth, DEMO_USERS } from '../context/AuthContext';
import { API_BASE_URL } from '../services/api';

export const ProfileScreen = ({ navigation }: any) => {
  const { user, logout, quickLogin } = useAuth();
  const [customServerUrl, setCustomServerUrl] = useState(API_BASE_URL);
  const [connectionStatus, setConnectionStatus] = useState<string | null>(null);

  const handleTestConnection = async () => {
    setConnectionStatus('Testing connection...');
    try {
      const res = await fetch(`${customServerUrl}/`);
      if (res.ok) {
        setConnectionStatus('✅ Connected to EduPredict AI Backend!');
      } else {
        setConnectionStatus(`⚠️ Server returned HTTP ${res.status}`);
      }
    } catch (e: any) {
      setConnectionStatus(`❌ Connection error: ${e.message}`);
    }
  };

  const handleLogout = async () => {
    Alert.alert('Sign Out', 'Are you sure you want to sign out of EduPredict AI?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Sign Out',
        style: 'destructive',
        onPress: async () => {
          await logout();
          navigation.replace('Login');
        },
      },
    ]);
  };

  const handleSwitchRole = async (role: 'student' | 'faculty' | 'admin') => {
    await quickLogin(role);
    Alert.alert('Role Switched', `Active user changed to ${role.toUpperCase()}`);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Profile Card */}
      <View style={styles.profileCard}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>
            {user?.name ? user.name.split(' ').map((n) => n[0]).join('').slice(0, 2) : 'SN'}
          </Text>
        </View>
        <Text style={styles.userName}>{user?.name || 'Aditya Rao'}</Text>
        <Text style={styles.userEmail}>{user?.email || 'student@sapthagiri.edu.in'}</Text>

        <View style={styles.roleBadge}>
          <Text style={styles.roleBadgeText}>
            {user?.role ? user.role.toUpperCase() : 'STUDENT'} ACCOUNT
          </Text>
        </View>

        <View style={styles.divider} />

        <View style={styles.infoRow}>
          <Text style={styles.infoKey}>University:</Text>
          <Text style={styles.infoVal}>Sapthagiri NPS University</Text>
        </View>
        <View style={styles.infoRow}>
          <Text style={styles.infoKey}>Department:</Text>
          <Text style={styles.infoVal}>Computer Science & Engg.</Text>
        </View>
        <View style={styles.infoRow}>
          <Text style={styles.infoKey}>Semester & Section:</Text>
          <Text style={styles.infoVal}>5th Semester • Section A</Text>
        </View>
        {user?.student_id && (
          <View style={styles.infoRow}>
            <Text style={styles.infoKey}>University USN:</Text>
            <Text style={[styles.infoVal, { fontWeight: '700', color: Colors.primary }]}>
              {user.student_id}
            </Text>
          </View>
        )}
      </View>

      {/* Switch Persona / Demo Testing */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Quick Persona Switcher</Text>
        <Text style={styles.cardSub}>Switch roles instantly for evaluation & demo</Text>

        <View style={styles.switchRow}>
          <TouchableOpacity
            style={[styles.switchBtn, user?.role === 'student' && styles.switchBtnActive]}
            onPress={() => handleSwitchRole('student')}
          >
            <Text style={[styles.switchText, user?.role === 'student' && styles.switchTextActive]}>
              🎓 Student
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.switchBtn, user?.role === 'faculty' && styles.switchBtnActive]}
            onPress={() => handleSwitchRole('faculty')}
          >
            <Text style={[styles.switchText, user?.role === 'faculty' && styles.switchTextActive]}>
              👨‍🏫 Faculty
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.switchBtn, user?.role === 'admin' && styles.switchBtnActive]}
            onPress={() => handleSwitchRole('admin')}
          >
            <Text style={[styles.switchText, user?.role === 'admin' && styles.switchTextActive]}>
              🛡️ Admin
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Backend API Configuration */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Backend API Configuration</Text>
        <Text style={styles.cardSub}>
          Android Emulator: http://10.0.2.2:8000 • iOS/Web: http://localhost:8000 • Real Device: http://&lt;your-pc-ip&gt;:8000
        </Text>

        <TextInput
          style={styles.serverInput}
          value={customServerUrl}
          onChangeText={setCustomServerUrl}
          placeholder="http://10.0.2.2:8000"
          placeholderTextColor="#94A3B8"
          autoCapitalize="none"
        />

        <TouchableOpacity style={styles.testBtn} onPress={handleTestConnection}>
          <Text style={styles.testBtnText}>⚡ Test Backend Connection</Text>
        </TouchableOpacity>

        {connectionStatus && (
          <Text style={styles.connStatusText}>{connectionStatus}</Text>
        )}
      </View>

      {/* Institutional Info */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>About EduPredict AI Mobile</Text>
        <Text style={styles.aboutText}>
          Version: 2.0.0 (Native React Native / Expo)
          {'\n'}Institution: Sapthagiri NPS University
          {'\n'}Campus: 14/5, Chikkasandra, Hesaraghatta Main Rd, Bengaluru
          {'\n'}Model: Scikit-Learn Random Forest (R² = 0.86)
          {'\n'}Backend: FastAPI v0.111.0 on Uvicorn
        </Text>
      </View>

      {/* Logout Button */}
      <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
        <Text style={styles.logoutText}>🚪 Sign Out</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F1F5F9',
  },
  content: {
    padding: 16,
    paddingBottom: 40,
  },
  profileCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 20,
    alignItems: 'center',
    marginBottom: 14,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 5,
    elevation: 2,
  },
  avatar: {
    width: 68,
    height: 68,
    borderRadius: 34,
    backgroundColor: Colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  avatarText: {
    fontSize: 24,
    fontWeight: '800',
    color: '#FFFFFF',
  },
  userName: {
    fontSize: 18,
    fontWeight: '800',
    color: Colors.textPrimary,
  },
  userEmail: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  roleBadge: {
    backgroundColor: Colors.accentLight,
    paddingVertical: 4,
    paddingHorizontal: 12,
    borderRadius: 20,
    marginTop: 8,
  },
  roleBadgeText: {
    fontSize: 10,
    fontWeight: '800',
    color: Colors.accent,
    letterSpacing: 0.5,
  },
  divider: {
    width: '100%',
    height: 1,
    backgroundColor: '#F1F5F9',
    marginVertical: 14,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
    paddingVertical: 4,
  },
  infoKey: {
    fontSize: 12,
    color: Colors.textSecondary,
  },
  infoVal: {
    fontSize: 12,
    fontWeight: '600',
    color: Colors.textPrimary,
  },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 16,
    marginBottom: 14,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 3,
    elevation: 1,
  },
  cardTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  cardSub: {
    fontSize: 11,
    color: Colors.textSecondary,
    marginTop: 2,
    marginBottom: 12,
    lineHeight: 16,
  },
  switchRow: {
    flexDirection: 'row',
    gap: 8,
  },
  switchBtn: {
    flex: 1,
    paddingVertical: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: Colors.border,
    alignItems: 'center',
    backgroundColor: '#F8FAFC',
  },
  switchBtnActive: {
    backgroundColor: Colors.primary,
    borderColor: Colors.primary,
  },
  switchText: {
    fontSize: 12,
    fontWeight: '600',
    color: Colors.textSecondary,
  },
  switchTextActive: {
    color: '#FFFFFF',
    fontWeight: '700',
  },
  serverInput: {
    borderWidth: 1,
    borderColor: Colors.border,
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 13,
    color: Colors.textPrimary,
    backgroundColor: '#F8FAFC',
    marginBottom: 10,
  },
  testBtn: {
    backgroundColor: Colors.surface,
    paddingVertical: 10,
    borderRadius: 8,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: Colors.border,
  },
  testBtnText: {
    fontSize: 12,
    fontWeight: '700',
    color: Colors.primary,
  },
  connStatusText: {
    fontSize: 11,
    marginTop: 8,
    color: Colors.textPrimary,
    textAlign: 'center',
    fontWeight: '600',
  },
  aboutText: {
    fontSize: 12,
    color: Colors.textSecondary,
    lineHeight: 18,
  },
  logoutBtn: {
    backgroundColor: '#FEE2E2',
    borderWidth: 1,
    borderColor: '#FECACA',
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: 6,
  },
  logoutText: {
    color: Colors.danger,
    fontSize: 14,
    fontWeight: '700',
  },
});
