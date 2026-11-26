import React, { useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Colors } from '../theme/colors';

export const SplashScreen = ({ navigation }: any) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      navigation.replace('Onboarding');
    }, 2200);
    return () => clearTimeout(timer);
  }, [navigation]);

  return (
    <View style={styles.container}>
      <View style={styles.logoContainer}>
        <View style={styles.iconCircle}>
          <Text style={styles.iconText}>🎓</Text>
        </View>
        <Text style={styles.title}>EduPredict AI</Text>
        <Text style={styles.subtitle}>Smart Student Academic Performance System</Text>
      </View>

      <View style={styles.footer}>
        <Text style={styles.university}>SAPTHAGIRI NPS UNIVERSITY</Text>
        <Text style={styles.location}>Bengaluru, Karnataka, India</Text>
        <Text style={styles.tagline}>Smarter Insights, Better Academic Performance</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.primaryDark,
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 60,
    paddingHorizontal: 24,
  },
  logoContainer: {
    alignItems: 'center',
    marginTop: 140,
  },
  iconCircle: {
    width: 90,
    height: 90,
    borderRadius: 45,
    backgroundColor: 'rgba(255, 255, 255, 0.12)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
    borderWidth: 1.5,
    borderColor: 'rgba(255, 255, 255, 0.25)',
  },
  iconText: {
    fontSize: 44,
  },
  title: {
    fontSize: 28,
    fontWeight: '800',
    color: '#FFFFFF',
    letterSpacing: -0.5,
  },
  subtitle: {
    fontSize: 13,
    color: '#94A3B8',
    marginTop: 6,
    textAlign: 'center',
  },
  footer: {
    alignItems: 'center',
  },
  university: {
    fontSize: 13,
    fontWeight: '700',
    color: '#E2E8F0',
    letterSpacing: 1.2,
  },
  location: {
    fontSize: 11,
    color: '#94A3B8',
    marginTop: 2,
  },
  tagline: {
    fontSize: 12,
    color: Colors.accent,
    marginTop: 12,
    fontWeight: '600',
  },
});
