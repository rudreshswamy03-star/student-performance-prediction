import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { Colors } from '../theme/colors';

const SUBJECTS_DETAIL = [
  {
    code: 'MAT301',
    name: 'Transform Calculus & Numerical Techniques',
    credits: 3,
    faculty: 'Dr. Savitha K.',
    cie1: 22,
    cie2: 21,
    cieTotal: 43,
    maxCie: 50,
    attendance: 86,
    examTarget: 80,
    status: 'Distinction',
  },
  {
    code: 'CS302',
    name: 'Data Structures and Algorithms',
    credits: 4,
    faculty: 'Prof. Ramesh Rao',
    cie1: 20,
    cie2: 19,
    cieTotal: 39,
    maxCie: 50,
    attendance: 82,
    examTarget: 75,
    status: 'First Class',
  },
  {
    code: 'CS303',
    name: 'Database Management Systems',
    credits: 4,
    faculty: 'Dr. Suresh Kumar',
    cie1: 23,
    cie2: 22,
    cieTotal: 45,
    maxCie: 50,
    attendance: 90,
    examTarget: 85,
    status: 'Distinction',
  },
  {
    code: 'CS304',
    name: 'Operating Systems & Architecture',
    credits: 3,
    faculty: 'Prof. Ananya Hegde',
    cie1: 18,
    cie2: 19,
    cieTotal: 37,
    maxCie: 50,
    attendance: 78,
    examTarget: 70,
    status: 'First Class',
  },
  {
    code: 'CS305',
    name: 'Computer Networks & Cloud Protocols',
    credits: 4,
    faculty: 'Dr. Venkatesh M.',
    cie1: 21,
    cie2: 20,
    cieTotal: 41,
    maxCie: 50,
    attendance: 84,
    examTarget: 80,
    status: 'Distinction',
  },
  {
    code: 'CS306',
    name: 'Data Mining and Data Wrangling',
    credits: 4,
    faculty: 'Prof. Deepa R.',
    cie1: 24,
    cie2: 23,
    cieTotal: 47,
    maxCie: 50,
    attendance: 92,
    examTarget: 90,
    status: 'Distinction',
  },
];

export const AcademicsScreen = () => {
  const [selectedSubject, setSelectedSubject] = useState<string | null>(null);

  const totalCredits = SUBJECTS_DETAIL.reduce((acc, s) => acc + s.credits, 0);
  const avgAttendance = Math.round(
    SUBJECTS_DETAIL.reduce((acc, s) => acc + s.attendance, 0) / SUBJECTS_DETAIL.length
  );
  const avgCie = Math.round(
    SUBJECTS_DETAIL.reduce((acc, s) => acc + s.cieTotal, 0) / SUBJECTS_DETAIL.length
  );

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>5th Semester Curriculum</Text>
        <Text style={styles.headerSub}>
          B.E. Computer Science & Engineering • 2026–2027
        </Text>
      </View>

      {/* Summary Cards */}
      <View style={styles.summaryRow}>
        <View style={styles.summaryCard}>
          <Text style={styles.summaryNum}>{totalCredits}</Text>
          <Text style={styles.summaryLabel}>Total Credits</Text>
        </View>
        <View style={styles.summaryCard}>
          <Text style={[styles.summaryNum, { color: Colors.primary }]}>{avgCie}/50</Text>
          <Text style={styles.summaryLabel}>Avg CIE Score</Text>
        </View>
        <View style={styles.summaryCard}>
          <Text style={[styles.summaryNum, { color: Colors.success }]}>{avgAttendance}%</Text>
          <Text style={styles.summaryLabel}>Avg Attendance</Text>
        </View>
      </View>

      {/* Subjects Accordion / List */}
      <Text style={styles.sectionTitle}>6 Core Prescribed Courses</Text>

      {SUBJECTS_DETAIL.map((sub) => {
        const isExpanded = selectedSubject === sub.code;
        return (
          <TouchableOpacity
            key={sub.code}
            style={styles.card}
            activeOpacity={0.8}
            onPress={() => setSelectedSubject(isExpanded ? null : sub.code)}
          >
            <View style={styles.cardHeader}>
              <View style={styles.codeBadge}>
                <Text style={styles.codeText}>{sub.code}</Text>
              </View>
              <View style={{ flex: 1 }}>
                <Text style={styles.courseName}>{sub.name}</Text>
                <Text style={styles.facultyText}>Faculty: {sub.faculty} • {sub.credits} Credits</Text>
              </View>
              <Text style={styles.expandIcon}>{isExpanded ? '▲' : '▼'}</Text>
            </View>

            {/* Quick Metrics Bar */}
            <View style={styles.quickBar}>
              <View style={styles.quickItem}>
                <Text style={styles.quickVal}>{sub.cieTotal}/50</Text>
                <Text style={styles.quickLabel}>Internal CIE</Text>
              </View>
              <View style={styles.quickDivider} />
              <View style={styles.quickItem}>
                <Text
                  style={[
                    styles.quickVal,
                    { color: sub.attendance >= 75 ? Colors.success : Colors.danger },
                  ]}
                >
                  {sub.attendance}%
                </Text>
                <Text style={styles.quickLabel}>Attendance</Text>
              </View>
              <View style={styles.quickDivider} />
              <View style={styles.quickItem}>
                <Text style={[styles.quickVal, { color: Colors.accent }]}>{sub.status}</Text>
                <Text style={styles.quickLabel}>Standing</Text>
              </View>
            </View>

            {/* Expanded Detailed Breakdown */}
            {isExpanded && (
              <View style={styles.expandedContent}>
                <View style={styles.detailRow}>
                  <Text style={styles.detailKey}>CIE-1 (Cycle 1):</Text>
                  <Text style={styles.detailVal}>{sub.cie1} / 25</Text>
                </View>
                <View style={styles.detailRow}>
                  <Text style={styles.detailKey}>CIE-2 (Cycle 2):</Text>
                  <Text style={styles.detailVal}>{sub.cie2} / 25</Text>
                </View>
                <View style={styles.detailRow}>
                  <Text style={styles.detailKey}>Total Internal Marks:</Text>
                  <Text style={[styles.detailVal, { fontWeight: '700', color: Colors.primary }]}>
                    {sub.cieTotal} / 50 ({((sub.cieTotal / 50) * 100).toFixed(0)}%)
                  </Text>
                </View>
                <View style={styles.detailRow}>
                  <Text style={styles.detailKey}>Projected SEE Target:</Text>
                  <Text style={styles.detailVal}>{sub.examTarget} / 100</Text>
                </View>
                <View style={styles.detailRow}>
                  <Text style={styles.detailKey}>Eligibility Status:</Text>
                  <Text style={[styles.detailVal, { color: Colors.success, fontWeight: '700' }]}>
                    ✓ Eligible for Final University Exam
                  </Text>
                </View>
              </View>
            )}
          </TouchableOpacity>
        );
      })}

      {/* Credit Evaluation Notice */}
      <View style={styles.gradingCard}>
        <Text style={styles.gradingTitle}>VTU / Sapthagiri NPS Grading Scheme</Text>
        <Text style={styles.gradingItem}>• 90–100%: Grade O (Outstanding, 10 Grade Points)</Text>
        <Text style={styles.gradingItem}>• 80–89%: Grade A+ (Excellent, 9 Grade Points)</Text>
        <Text style={styles.gradingItem}>• 70–79%: Grade A (Very Good, 8 Grade Points)</Text>
        <Text style={styles.gradingItem}>• 60–69%: Grade B+ (Good, 7 Grade Points)</Text>
        <Text style={styles.gradingItem}>• Below 40%: Grade F (Fail / Arrear)</Text>
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
  header: {
    marginBottom: 16,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '800',
    color: Colors.textPrimary,
  },
  headerSub: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  summaryRow: {
    flexDirection: 'row',
    gap: 10,
    marginBottom: 18,
  },
  summaryCard: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 14,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 3,
    elevation: 1,
  },
  summaryNum: {
    fontSize: 20,
    fontWeight: '800',
    color: Colors.textPrimary,
  },
  summaryLabel: {
    fontSize: 11,
    color: Colors.textSecondary,
    marginTop: 4,
  },
  sectionTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: Colors.textPrimary,
    marginBottom: 12,
  },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 5,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  codeBadge: {
    backgroundColor: Colors.accentLight,
    paddingVertical: 6,
    paddingHorizontal: 8,
    borderRadius: 8,
  },
  codeText: {
    fontSize: 11,
    fontWeight: '800',
    color: Colors.accent,
  },
  courseName: {
    fontSize: 14,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  facultyText: {
    fontSize: 11,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  expandIcon: {
    fontSize: 12,
    color: Colors.textMuted,
  },
  quickBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    backgroundColor: '#F8FAFC',
    borderRadius: 10,
    paddingVertical: 10,
    marginTop: 12,
  },
  quickItem: {
    alignItems: 'center',
  },
  quickVal: {
    fontSize: 13,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  quickLabel: {
    fontSize: 10,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  quickDivider: {
    width: 1,
    height: 24,
    backgroundColor: '#E2E8F0',
  },
  expandedContent: {
    borderTopWidth: 1,
    borderTopColor: '#F1F5F9',
    marginTop: 12,
    paddingTop: 12,
    gap: 6,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 3,
  },
  detailKey: {
    fontSize: 12,
    color: Colors.textSecondary,
  },
  detailVal: {
    fontSize: 12,
    color: Colors.textPrimary,
  },
  gradingCard: {
    backgroundColor: '#EEF2FF',
    borderRadius: 12,
    padding: 14,
    marginTop: 10,
    borderWidth: 1,
    borderColor: '#C7D2FE',
  },
  gradingTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: Colors.accent,
    marginBottom: 6,
  },
  gradingItem: {
    fontSize: 11,
    color: '#3730A3',
    lineHeight: 18,
  },
});
