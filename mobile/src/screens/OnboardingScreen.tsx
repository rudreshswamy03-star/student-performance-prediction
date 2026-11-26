import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Dimensions } from 'react-native';
import { Colors } from '../theme/colors';

const { width } = Dimensions.get('window');

const SLIDES = [
  {
    id: 1,
    emoji: '🏛️',
    title: 'Sapthagiri NPS University',
    subtitle: 'Bengaluru, Karnataka',
    description:
      'Official academic intelligence portal for Department of Computer Science & Engineering, 5th Semester B.E. (2026–2027).',
  },
  {
    id: 2,
    emoji: '🤖',
    title: 'AI Performance Predictor',
    subtitle: 'Machine Learning Engine',
    description:
      'Predict your final semester exam marks and SGPA in real time using our trained Random Forest ML regression model.',
  },
  {
    id: 3,
    emoji: '⚠️',
    title: 'Early Academic Warning',
    subtitle: 'Proactive Mentorship & Retention',
    description:
      'Automated risk detection flags borderline attendance, low internal CIE scores, and backlog risks before university exams.',
  },
  {
    id: 4,
    emoji: '📊',
    title: 'Comprehensive Subject Insights',
    subtitle: '6 Core Engineering Courses',
    description:
      'Deep tracking across Mathematics, DSA, DBMS, Operating Systems, Computer Networks, and Data Mining & Wrangling.',
  },
];

export const OnboardingScreen = ({ navigation }: any) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const handleNext = () => {
    if (currentIndex < SLIDES.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      navigation.replace('Login');
    }
  };

  const handleSkip = () => {
    navigation.replace('Login');
  };

  const currentSlide = SLIDES[currentIndex];

  return (
    <View style={styles.container}>
      {/* Top Header */}
      <View style={styles.topBar}>
        <Text style={styles.brandText}>EduPredict AI</Text>
        <TouchableOpacity onPress={handleSkip} style={styles.skipButton}>
          <Text style={styles.skipText}>Skip</Text>
        </TouchableOpacity>
      </View>

      {/* Slide Body */}
      <View style={styles.content}>
        <View style={styles.iconCircle}>
          <Text style={styles.icon}>{currentSlide.emoji}</Text>
        </View>

        <Text style={styles.title}>{currentSlide.title}</Text>
        <Text style={styles.subtitle}>{currentSlide.subtitle}</Text>
        <Text style={styles.description}>{currentSlide.description}</Text>
      </View>

      {/* Pagination & Next Button */}
      <View style={styles.footer}>
        <View style={styles.dotsRow}>
          {SLIDES.map((_, i) => (
            <View
              key={i}
              style={[
                styles.dot,
                currentIndex === i ? styles.activeDot : styles.inactiveDot,
              ]}
            />
          ))}
        </View>

        <TouchableOpacity style={styles.actionButton} onPress={handleNext}>
          <Text style={styles.actionButtonText}>
            {currentIndex === SLIDES.length - 1 ? 'Get Started' : 'Next →'}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
    justifyContent: 'space-between',
    paddingHorizontal: 24,
    paddingTop: 56,
    paddingBottom: 40,
  },
  topBar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  brandText: {
    fontSize: 16,
    fontWeight: '800',
    color: Colors.primary,
    letterSpacing: 0.5,
  },
  skipButton: {
    paddingVertical: 6,
    paddingHorizontal: 12,
  },
  skipText: {
    fontSize: 14,
    color: Colors.textSecondary,
    fontWeight: '600',
  },
  content: {
    alignItems: 'center',
    paddingHorizontal: 12,
  },
  iconCircle: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: Colors.accentLight,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 32,
    borderWidth: 2,
    borderColor: '#E0E7FF',
  },
  icon: {
    fontSize: 54,
  },
  title: {
    fontSize: 22,
    fontWeight: '800',
    color: Colors.textPrimary,
    textAlign: 'center',
    marginBottom: 6,
  },
  subtitle: {
    fontSize: 14,
    fontWeight: '600',
    color: Colors.accent,
    textAlign: 'center',
    marginBottom: 16,
    textTransform: 'uppercase',
    letterSpacing: 0.8,
  },
  description: {
    fontSize: 15,
    color: Colors.textSecondary,
    textAlign: 'center',
    lineHeight: 22,
  },
  footer: {
    gap: 20,
  },
  dotsRow: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: 8,
  },
  dot: {
    height: 8,
    borderRadius: 4,
  },
  activeDot: {
    width: 28,
    backgroundColor: Colors.primary,
  },
  inactiveDot: {
    width: 8,
    backgroundColor: Colors.border,
  },
  actionButton: {
    backgroundColor: Colors.primary,
    paddingVertical: 16,
    borderRadius: 14,
    alignItems: 'center',
    shadowColor: Colors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
    elevation: 4,
  },
  actionButtonText: {
    fontSize: 16,
    fontWeight: '700',
    color: '#FFFFFF',
  },
});
