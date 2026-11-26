import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Alert,
} from 'react-native';
import { Colors } from '../theme/colors';
import { useAuth, DEMO_USERS } from '../context/AuthContext';

export const LoginScreen = ({ navigation }: any) => {
  const { login, quickLogin, isLoading } = useAuth();
  const [email, setEmail] = useState('student@sapthagiri.edu.in');
  const [password, setPassword] = useState('Student@123');
  const [selectedRole, setSelectedRole] = useState<'student' | 'faculty' | 'admin'>('student');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleRoleSelect = (role: 'student' | 'faculty' | 'admin') => {
    setSelectedRole(role);
    const demo = DEMO_USERS[role];
    if (demo) {
      setEmail(demo.email);
      setPassword(demo.pass);
    }
  };

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Required Fields', 'Please enter your email and password.');
      return;
    }
    setLoading(true);
    setErrorMessage(null);
    try {
      const success = await login(email, password);
      if (success) {
        navigation.replace('MainTabs');
      } else {
        setErrorMessage('Invalid credentials. Check email/password or use One-Touch Demo below.');
      }
    } catch (err: any) {
      setErrorMessage(err.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemo = async (role: 'student' | 'faculty' | 'admin') => {
    handleRoleSelect(role);
    setLoading(true);
    setErrorMessage(null);
    try {
      await quickLogin(role);
      navigation.replace('MainTabs');
    } catch (err: any) {
      setErrorMessage('Failed to sign in with demo account.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={{ flex: 1 }}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView contentContainerStyle={styles.scrollContent} keyboardShouldPersistTaps="handled">
        {/* University Header */}
        <View style={styles.header}>
          <View style={styles.badgeRow}>
            <Text style={styles.badgeText}>🏛️ Sapthagiri NPS University</Text>
          </View>
          <Text style={styles.headerTitle}>EduPredict AI</Text>
          <Text style={styles.headerSubtitle}>
            Dept of Computer Science & Engineering • 5th Sem
          </Text>
        </View>

        {/* Card Form */}
        <View style={styles.card}>
          <Text style={styles.cardTitle}>Sign In to Academic Portal</Text>
          <Text style={styles.cardSubtitle}>Choose your campus role to continue</Text>

          {/* Role Tabs */}
          <View style={styles.roleTabs}>
            {(['student', 'faculty', 'admin'] as const).map((role) => (
              <TouchableOpacity
                key={role}
                style={[
                  styles.roleTab,
                  selectedRole === role && styles.activeRoleTab,
                ]}
                onPress={() => handleRoleSelect(role)}
              >
                <Text
                  style={[
                    styles.roleTabText,
                    selectedRole === role && styles.activeRoleTabText,
                  ]}
                >
                  {role === 'student' ? '🎓 Student' : role === 'faculty' ? '👨‍🏫 Faculty' : '🛡️ Admin'}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          {errorMessage && (
            <View style={styles.errorBox}>
              <Text style={styles.errorText}>⚠️ {errorMessage}</Text>
            </View>
          )}

          {/* Input Fields */}
          <View style={styles.inputGroup}>
            <Text style={styles.label}>Institutional Email</Text>
            <TextInput
              style={styles.input}
              value={email}
              onChangeText={setEmail}
              placeholder="e.g. yourname@sapthagiri.edu.in"
              placeholderTextColor="#94A3B8"
              autoCapitalize="none"
              keyboardType="email-address"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.label}>Password</Text>
            <TextInput
              style={styles.input}
              value={password}
              onChangeText={setPassword}
              placeholder="••••••••"
              placeholderTextColor="#94A3B8"
              secureTextEntry
            />
          </View>

          {/* Sign In Button */}
          <TouchableOpacity
            style={styles.loginBtn}
            onPress={handleLogin}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#FFFFFF" />
            ) : (
              <Text style={styles.loginBtnText}>Sign In</Text>
            )}
          </TouchableOpacity>

          {/* Quick Demo One-Touch */}
          <View style={styles.demoSection}>
            <Text style={styles.demoDividerText}>── QUICK DEMO ACCESS ──</Text>
            <View style={styles.demoButtonsRow}>
              <TouchableOpacity
                style={styles.demoChip}
                onPress={() => handleQuickDemo('student')}
              >
                <Text style={styles.demoChipText}>🎓 Student</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.demoChip}
                onPress={() => handleQuickDemo('faculty')}
              >
                <Text style={styles.demoChipText}>👨‍🏫 Faculty</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.demoChip}
                onPress={() => handleQuickDemo('admin')}
              >
                <Text style={styles.demoChipText}>🛡️ Admin</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Register Link */}
          <TouchableOpacity
            style={styles.registerLink}
            onPress={() => navigation.navigate('Register')}
          >
            <Text style={styles.registerLinkText}>
              New Student? <Text style={styles.registerLinkBold}>Create Account</Text>
            </Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.footerNote}>
          Bengaluru, Karnataka, India • Academic Year 2026–2027
        </Text>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  scrollContent: {
    flexGrow: 1,
    backgroundColor: Colors.primaryDark,
    paddingHorizontal: 20,
    paddingTop: 50,
    paddingBottom: 30,
    justifyContent: 'center',
  },
  header: {
    alignItems: 'center',
    marginBottom: 24,
  },
  badgeRow: {
    backgroundColor: 'rgba(255, 255, 255, 0.12)',
    paddingVertical: 5,
    paddingHorizontal: 12,
    borderRadius: 20,
    marginBottom: 10,
  },
  badgeText: {
    fontSize: 12,
    fontWeight: '700',
    color: '#E2E8F0',
    letterSpacing: 0.5,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '800',
    color: '#FFFFFF',
    letterSpacing: -0.5,
  },
  headerSubtitle: {
    fontSize: 12,
    color: '#94A3B8',
    marginTop: 4,
    textAlign: 'center',
  },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    padding: 24,
    shadowColor: '#000000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.25,
    shadowRadius: 15,
    elevation: 8,
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  cardSubtitle: {
    fontSize: 13,
    color: Colors.textSecondary,
    marginTop: 2,
    marginBottom: 18,
  },
  roleTabs: {
    flexDirection: 'row',
    backgroundColor: Colors.surface,
    borderRadius: 10,
    padding: 4,
    marginBottom: 18,
  },
  roleTab: {
    flex: 1,
    paddingVertical: 8,
    alignItems: 'center',
    borderRadius: 8,
  },
  activeRoleTab: {
    backgroundColor: Colors.primary,
  },
  roleTabText: {
    fontSize: 12,
    fontWeight: '600',
    color: Colors.textSecondary,
  },
  activeRoleTabText: {
    color: '#FFFFFF',
    fontWeight: '700',
  },
  errorBox: {
    backgroundColor: Colors.dangerBg,
    borderRadius: 8,
    padding: 10,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: '#FECACA',
  },
  errorText: {
    fontSize: 12,
    color: Colors.danger,
    fontWeight: '600',
  },
  inputGroup: {
    marginBottom: 14,
  },
  label: {
    fontSize: 13,
    fontWeight: '600',
    color: Colors.textPrimary,
    marginBottom: 6,
  },
  input: {
    borderWidth: 1,
    borderColor: Colors.border,
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 14,
    color: Colors.textPrimary,
    backgroundColor: '#F8FAFC',
  },
  loginBtn: {
    backgroundColor: Colors.primary,
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: 'center',
    marginTop: 6,
  },
  loginBtnText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '700',
  },
  demoSection: {
    marginTop: 20,
    alignItems: 'center',
  },
  demoDividerText: {
    fontSize: 11,
    fontWeight: '700',
    color: '#94A3B8',
    letterSpacing: 1,
    marginBottom: 12,
  },
  demoButtonsRow: {
    flexDirection: 'row',
    gap: 8,
    width: '100%',
  },
  demoChip: {
    flex: 1,
    backgroundColor: Colors.accentLight,
    paddingVertical: 10,
    borderRadius: 8,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#C7D2FE',
  },
  demoChipText: {
    fontSize: 12,
    fontWeight: '700',
    color: Colors.accent,
  },
  registerLink: {
    marginTop: 18,
    alignItems: 'center',
  },
  registerLinkText: {
    fontSize: 13,
    color: Colors.textSecondary,
  },
  registerLinkBold: {
    color: Colors.primary,
    fontWeight: '700',
  },
  footerNote: {
    textAlign: 'center',
    fontSize: 11,
    color: '#64748B',
    marginTop: 20,
  },
});
