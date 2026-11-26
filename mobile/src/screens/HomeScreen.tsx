import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { Colors } from '../theme/colors';
import { useAuth } from '../context/AuthContext';
import { ApiService } from '../services/api';

const DEFAULT_SUBJECTS = [
  { code: 'MAT301', name: 'Transform Calculus & Numerical', marks: 82, cie: 42 },
  { code: 'CS302', name: 'Data Structures & Algorithms', marks: 78, cie: 39 },
  { code: 'CS303', name: 'Database Management Systems', marks: 85, cie: 45 },
  { code: 'CS304', name: 'Operating Systems', marks: 74, cie: 38 },
  { code: 'CS305', name: 'Computer Networks', marks: 80, cie: 41 },
  { code: 'CS306', name: 'Data Mining & Data Wrangling', marks: 88, cie: 46 },
];

export const HomeScreen = ({ navigation }: any) => {
  const { user } = useAuth();
  const [refreshing, setRefreshing] = useState(false);
  const [studentData, setStudentData] = useState<any>({
    name: user?.name || 'Aditya Rao',
    usn: user?.student_id || 'SNPSU2024CS042',
    department: 'Computer Science and Engineering',
    semester: '5th Semester B.E.',
    section: 'A',
    cgpa: 8.12,
    attendance: 84.5,
    study_hours: 19.0,
    backlogs: 0,
    risk_level: 'Low',
    risk_label: 'Good Academic Standing',
  });

  const loadData = async () => {
    try {
      const res = await ApiService.getMyStudentProfile();
      if (res && res.name) {
        setStudentData(res);
      }
    } catch (e) {
      // Keep robust defaults
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  };

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      {/* Top University Branding Banner */}
      <View style={styles.univBanner}>
        <View style={styles.univBannerLeft}>
          <Text style={styles.univName}>SAPTHAGIRI NPS UNIVERSITY</Text>
          <Text style={styles.univDept}>Dept. of Computer Science & Engineering</Text>
          <Text style={styles.univLoc}>Bengaluru, Karnataka • Academic Year 2026–27</Text>
        </View>
        <View style={styles.univBadge}>
          <Text style={styles.univBadgeText}>5th SEM</Text>
        </View>
      </View>

      {/* Student Welcome Card */}
      <View style={styles.studentCard}>
        <View style={styles.studentInfoRow}>
          <View style={styles.avatarCircle}>
            <Text style={styles.avatarText}>
              {studentData.name.split(' ').map((n: string) => n[0]).join('').slice(0, 2)}
            </Text>
          </View>
          <View style={styles.studentDetails}>
            <Text style={styles.studentName}>{studentData.name}</Text>
            <Text style={styles.studentUsn}>USN: {studentData.usn || 'SNPSU2024CS042'}</Text>
            <Text style={styles.studentMeta}>
              Section {studentData.section || 'A'} • Role: {user?.role ? user.role.toUpperCase() : 'STUDENT'}
            </Text>
          </View>
        </View>

        {/* Academic Risk Banner */}
        <View
          style={[
            styles.riskBadgeRow,
            studentData.risk_level === 'High'
              ? styles.riskHigh
              : studentData.risk_level === 'Medium'
              ? styles.riskMedium
              : styles.riskLow,
          ]}
        >
          <Text style={styles.riskBadgeIcon}>
            {studentData.risk_level === 'High' ? '🔴' : studentData.risk_level === 'Medium' ? '🟡' : '🟢'}
          </Text>
          <View style={{ flex: 1 }}>
            <Text style={styles.riskBadgeTitle}>
              {studentData.risk_level} Academic Risk — {studentData.risk_label}
            </Text>
            <Text style={styles.riskBadgeSub}>
              {studentData.risk_level === 'High'
                ? 'Mandatory faculty counseling recommended.'
                : 'Eligible for Distinction honor roll. Attendance exceeds 75% threshold.'}
            </Text>
          </View>
        </View>
      </View>

      {/* 4 Key Academic Metrics Grid */}
      <View style={styles.metricsGrid}>
        <View style={styles.metricCard}>
          <Text style={styles.metricLabel}>Current CGPA</Text>
          <Text style={styles.metricVal}>{studentData.cgpa.toFixed(2)}</Text>
          <Text style={styles.metricSub}>Scale 10.0</Text>
        </View>

        <View style={styles.metricCard}>
          <Text style={styles.metricLabel}>Attendance</Text>
          <Text style={[styles.metricVal, { color: studentData.attendance >= 75 ? Colors.success : Colors.danger }]}>
            {studentData.attendance}%
          </Text>
          <Text style={styles.metricSub}>Min 75% Req.</Text>
        </View>

        <View style={styles.metricCard}>
          <Text style={styles.metricLabel}>Study Time</Text>
          <Text style={styles.metricVal}>{studentData.study_hours}h</Text>
          <Text style={styles.metricSub}>Per Week</Text>
        </View>

        <View style={styles.metricCard}>
          <Text style={styles.metricLabel}>Backlogs</Text>
          <Text style={[styles.metricVal, { color: studentData.backlogs === 0 ? Colors.success : Colors.warning }]}>
            {studentData.backlogs}
          </Text>
          <Text style={styles.metricSub}>Active</Text>
        </View>
      </View>

      {/* Quick Actions Hub */}
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Academic Intelligence Hub</Text>
      </View>

      <View style={styles.actionGrid}>
        <TouchableOpacity
          style={[styles.actionTile, { backgroundColor: '#EEF2FF', borderColor: '#C7D2FE' }]}
          onPress={() => navigation.navigate('Predictor')}
        >
          <Text style={styles.actionIcon}>🤖</Text>
          <Text style={styles.actionTitle}>AI Predictor</Text>
          <Text style={styles.actionDesc}>Simulate marks & final SGPA</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.actionTile, { backgroundColor: '#F0FDF4', borderColor: '#BBF7D0' }]}
          onPress={() => navigation.navigate('Academics')}
        >
          <Text style={styles.actionIcon}>📚</Text>
          <Text style={styles.actionTitle}>6 Core Subjects</Text>
          <Text style={styles.actionDesc}>CIE & Attendance audit</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.actionTile, { backgroundColor: '#FFFBEB', borderColor: '#FDE68A' }]}
          onPress={() => navigation.navigate('EarlyWarning')}
        >
          <Text style={styles.actionIcon}>⚠️</Text>
          <Text style={styles.actionTitle}>Early Warning</Text>
          <Text style={styles.actionDesc}>Risk tier & counseling</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.actionTile, { backgroundColor: '#F8FAFC', borderColor: '#E2E8F0' }]}
          onPress={() => navigation.navigate('Analytics')}
        >
          <Text style={styles.actionIcon}>📊</Text>
          <Text style={styles.actionTitle}>Class Analytics</Text>
          <Text style={styles.actionDesc}>Section & batch stats</Text>
        </TouchableOpacity>
      </View>

      {/* 6 Subjects Quick View */}
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>5th Semester Course Progress</Text>
        <TouchableOpacity onPress={() => navigation.navigate('Academics')}>
          <Text style={styles.sectionLink}>View All →</Text>
        </TouchableOpacity>
      </View>

      {DEFAULT_SUBJECTS.map((sub) => (
        <View key={sub.code} style={styles.subjectRow}>
          <View style={styles.subjectLeft}>
            <View style={styles.codeTag}>
              <Text style={styles.codeTagText}>{sub.code}</Text>
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.subName} numberOfLines={1}>{sub.name}</Text>
              <Text style={styles.subCie}>CIE: {sub.cie}/50 • Target: 85%</Text>
            </View>
          </View>
          <View style={styles.subjectRight}>
            <Text style={styles.subMarks}>{sub.marks}%</Text>
            <View style={styles.progressBarBg}>
              <View style={[styles.progressBarFill, { width: `${sub.marks}%` }]} />
            </View>
          </View>
        </View>
      ))}

      {/* Institutional Advisory */}
      <View style={styles.advisoryCard}>
        <Text style={styles.advisoryHeader}>📢 Department Notice</Text>
        <Text style={styles.advisoryBody}>
          Continuous Internal Evaluation (CIE-2) begins next Monday. Students below 75% attendance must meet their respective faculty mentors before Friday 4:00 PM.
        </Text>
      </View>
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
  univBanner: {
    backgroundColor: Colors.primaryDark,
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 14,
  },
  univBannerLeft: {
    flex: 1,
  },
  univName: {
    fontSize: 13,
    fontWeight: '800',
    color: '#F8FAFC',
    letterSpacing: 0.8,
  },
  univDept: {
    fontSize: 11,
    color: '#94A3B8',
    marginTop: 2,
  },
  univLoc: {
    fontSize: 10,
    color: '#64748B',
    marginTop: 2,
  },
  univBadge: {
    backgroundColor: Colors.accent,
    paddingVertical: 6,
    paddingHorizontal: 10,
    borderRadius: 8,
    marginLeft: 8,
  },
  univBadgeText: {
    color: '#FFFFFF',
    fontWeight: '800',
    fontSize: 11,
  },
  studentCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    marginBottom: 14,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 6,
    elevation: 2,
  },
  studentInfoRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  avatarCircle: {
    width: 52,
    height: 52,
    borderRadius: 26,
    backgroundColor: Colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 14,
  },
  avatarText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '800',
  },
  studentDetails: {
    flex: 1,
  },
  studentName: {
    fontSize: 17,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  studentUsn: {
    fontSize: 12,
    fontWeight: '600',
    color: Colors.accent,
    marginTop: 2,
  },
  studentMeta: {
    fontSize: 11,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  riskBadgeRow: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 10,
    padding: 10,
    marginTop: 14,
    gap: 8,
  },
  riskLow: {
    backgroundColor: Colors.successBg,
    borderColor: '#A7F3D0',
    borderWidth: 1,
  },
  riskMedium: {
    backgroundColor: Colors.warningBg,
    borderColor: '#FDE68A',
    borderWidth: 1,
  },
  riskHigh: {
    backgroundColor: Colors.dangerBg,
    borderColor: '#FECACA',
    borderWidth: 1,
  },
  riskBadgeIcon: {
    fontSize: 18,
  },
  riskBadgeTitle: {
    fontSize: 12,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  riskBadgeSub: {
    fontSize: 11,
    color: Colors.textSecondary,
    marginTop: 1,
  },
  metricsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
    marginBottom: 16,
  },
  metricCard: {
    flex: 1,
    minWidth: '46%',
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 14,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 1,
  },
  metricLabel: {
    fontSize: 12,
    color: Colors.textSecondary,
    fontWeight: '600',
  },
  metricVal: {
    fontSize: 22,
    fontWeight: '800',
    color: Colors.textPrimary,
    marginTop: 4,
  },
  metricSub: {
    fontSize: 10,
    color: Colors.textMuted,
    marginTop: 2,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
    marginTop: 4,
  },
  sectionTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  sectionLink: {
    fontSize: 13,
    fontWeight: '600',
    color: Colors.primary,
  },
  actionGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
    marginBottom: 18,
  },
  actionTile: {
    flex: 1,
    minWidth: '46%',
    borderRadius: 14,
    padding: 14,
    borderWidth: 1,
  },
  actionIcon: {
    fontSize: 24,
    marginBottom: 8,
  },
  actionTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  actionDesc: {
    fontSize: 11,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  subjectRow: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 12,
    marginBottom: 8,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  subjectLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    gap: 10,
  },
  codeTag: {
    backgroundColor: Colors.accentLight,
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 6,
  },
  codeTagText: {
    fontSize: 10,
    fontWeight: '700',
    color: Colors.accent,
  },
  subName: {
    fontSize: 13,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  subCie: {
    fontSize: 11,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  subjectRight: {
    alignItems: 'flex-end',
    width: 65,
  },
  subMarks: {
    fontSize: 13,
    fontWeight: '700',
    color: Colors.primary,
    marginBottom: 4,
  },
  progressBarBg: {
    width: '100%',
    height: 5,
    backgroundColor: '#E2E8F0',
    borderRadius: 3,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: Colors.primary,
    borderRadius: 3,
  },
  advisoryCard: {
    backgroundColor: '#EFF6FF',
    borderColor: '#BFDBFE',
    borderWidth: 1,
    borderRadius: 12,
    padding: 14,
    marginTop: 10,
  },
  advisoryHeader: {
    fontSize: 13,
    fontWeight: '700',
    color: Colors.primary,
    marginBottom: 4,
  },
  advisoryBody: {
    fontSize: 12,
    color: '#334155',
    lineHeight: 18,
  },
});
