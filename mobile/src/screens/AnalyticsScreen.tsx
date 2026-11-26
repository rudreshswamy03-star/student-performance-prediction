import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { Colors } from '../theme/colors';

export const AnalyticsScreen = () => {
  const cohortDist = [
    { label: 'Distinction (≥ 75%)', count: 48, pct: 40, color: Colors.success },
    { label: 'First Class (60–74%)', count: 44, pct: 37, color: Colors.primary },
    { label: 'Second Class (50–59%)', count: 18, pct: 15, color: Colors.warning },
    { label: 'At Academic Risk (< 50%)', count: 10, pct: 8, color: Colors.danger },
  ];

  const sections = [
    { name: 'Section A', avgCgpa: 8.14, att: '83.2%', atRisk: 4, leader: 'Dr. Suresh Kumar' },
    { name: 'Section B', avgCgpa: 7.91, att: '81.0%', atRisk: 6, leader: 'Prof. Ananya Hegde' },
    { name: 'Section C', avgCgpa: 7.82, att: '79.5%', atRisk: 8, leader: 'Dr. Savitha K.' },
  ];

  const subjectAverages = [
    { name: 'Data Mining & DW', avg: 81, high: 98 },
    { name: 'DBMS', avg: 79, high: 96 },
    { name: 'Transform Calculus', avg: 76, high: 95 },
    { name: 'Computer Networks', avg: 74, high: 92 },
    { name: 'DSA', avg: 72, high: 94 },
    { name: 'Operating Systems', avg: 69, high: 90 },
  ];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Cohort Academic Analytics</Text>
        <Text style={styles.subtitle}>
          Sapthagiri NPS University • 5th Sem CSE (120 Students)
        </Text>
      </View>

      {/* Cohort Grade Distribution */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Grade Distribution Overview</Text>
        <Text style={styles.cardSub}>VTU / University Standard Classification</Text>

        <View style={styles.distBars}>
          {cohortDist.map((item) => (
            <View key={item.label} style={styles.distItem}>
              <View style={styles.distLabelRow}>
                <Text style={styles.distName}>{item.label}</Text>
                <Text style={styles.distCount}>
                  {item.count} students ({item.pct}%)
                </Text>
              </View>
              <View style={styles.barBg}>
                <View
                  style={[
                    styles.barFill,
                    { width: `${item.pct}%`, backgroundColor: item.color },
                  ]}
                />
              </View>
            </View>
          ))}
        </View>
      </View>

      {/* Section Performance Comparison */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Section-wise Comparative Performance</Text>
        <Text style={styles.cardSub}>Sections A, B, and C Academic Metrics</Text>

        <View style={styles.sectionGrid}>
          {sections.map((sec) => (
            <View key={sec.name} style={styles.sectionBox}>
              <Text style={styles.secName}>{sec.name}</Text>
              <Text style={styles.secCgpa}>{sec.avgCgpa.toFixed(2)}</Text>
              <Text style={styles.secCgpaLabel}>Avg CGPA</Text>
              <View style={styles.secDivider} />
              <Text style={styles.secDetail}>Avg Attendance: {sec.att}</Text>
              <Text style={styles.secDetail}>At-Risk Students: {sec.atRisk}</Text>
              <Text style={styles.secLeader}>Faculty: {sec.leader}</Text>
            </View>
          ))}
        </View>
      </View>

      {/* Subject Marks Benchmarking */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Subject Benchmark Averages</Text>
        <Text style={styles.cardSub}>Class Average vs Highest Scored Marks</Text>

        {subjectAverages.map((sub) => (
          <View key={sub.name} style={styles.subBenchmarkRow}>
            <View style={{ flex: 1 }}>
              <Text style={styles.subBenchName}>{sub.name}</Text>
              <View style={styles.barBg}>
                <View style={[styles.barFill, { width: `${sub.avg}%`, backgroundColor: Colors.accent }]} />
              </View>
            </View>
            <View style={styles.subBenchScores}>
              <Text style={styles.benchAvg}>{sub.avg}% avg</Text>
              <Text style={styles.benchHigh}>Top: {sub.high}%</Text>
            </View>
          </View>
        ))}
      </View>

      {/* Statistical Correlation Findings */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Data Science & AI Findings</Text>
        <View style={styles.findingItem}>
          <Text style={styles.findingIcon}>📈</Text>
          <View style={{ flex: 1 }}>
            <Text style={styles.findingTitle}>Attendance Correlation (+0.78)</Text>
            <Text style={styles.findingDesc}>
              Students maintaining &gt;85% attendance scored on average 1.6 CGPA points higher than those below 75%.
            </Text>
          </View>
        </View>

        <View style={styles.findingItem}>
          <Text style={styles.findingIcon}>⏰</Text>
          <View style={{ flex: 1 }}>
            <Text style={styles.findingTitle}>Study Hours Plateau (+0.65)</Text>
            <Text style={styles.findingDesc}>
              Optimal academic benefit observed between 18–24 hours/week. Diminishing returns detected beyond 30 hours without rest.
            </Text>
          </View>
        </View>
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
  title: {
    fontSize: 20,
    fontWeight: '800',
    color: Colors.textPrimary,
  },
  subtitle: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 16,
    marginBottom: 14,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 5,
    elevation: 2,
  },
  cardTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  cardSub: {
    fontSize: 11,
    color: Colors.textSecondary,
    marginTop: 2,
    marginBottom: 14,
  },
  distBars: {
    gap: 12,
  },
  distItem: {},
  distLabelRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 4,
  },
  distName: {
    fontSize: 12,
    fontWeight: '600',
    color: Colors.textPrimary,
  },
  distCount: {
    fontSize: 11,
    color: Colors.textSecondary,
  },
  barBg: {
    height: 7,
    backgroundColor: '#E2E8F0',
    borderRadius: 4,
    overflow: 'hidden',
  },
  barFill: {
    height: '100%',
    borderRadius: 4,
  },
  sectionGrid: {
    flexDirection: 'row',
    gap: 8,
  },
  sectionBox: {
    flex: 1,
    backgroundColor: '#F8FAFC',
    borderRadius: 10,
    padding: 10,
    borderWidth: 1,
    borderColor: Colors.border,
    alignItems: 'center',
  },
  secName: {
    fontSize: 12,
    fontWeight: '700',
    color: Colors.primary,
  },
  secCgpa: {
    fontSize: 20,
    fontWeight: '900',
    color: Colors.textPrimary,
    marginTop: 4,
  },
  secCgpaLabel: {
    fontSize: 9,
    color: Colors.textSecondary,
  },
  secDivider: {
    width: '100%',
    height: 1,
    backgroundColor: '#E2E8F0',
    marginVertical: 6,
  },
  secDetail: {
    fontSize: 10,
    color: Colors.textSecondary,
    textAlign: 'center',
  },
  secLeader: {
    fontSize: 9,
    color: Colors.accent,
    fontWeight: '600',
    marginTop: 4,
    textAlign: 'center',
  },
  subBenchmarkRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    marginBottom: 12,
  },
  subBenchName: {
    fontSize: 12,
    fontWeight: '600',
    color: Colors.textPrimary,
    marginBottom: 4,
  },
  subBenchScores: {
    width: 65,
    alignItems: 'flex-end',
  },
  benchAvg: {
    fontSize: 12,
    fontWeight: '700',
    color: Colors.primary,
  },
  benchHigh: {
    fontSize: 10,
    color: Colors.textMuted,
  },
  findingItem: {
    flexDirection: 'row',
    gap: 10,
    marginTop: 10,
    backgroundColor: '#F8FAFC',
    padding: 10,
    borderRadius: 8,
  },
  findingIcon: {
    fontSize: 20,
  },
  findingTitle: {
    fontSize: 12,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  findingDesc: {
    fontSize: 11,
    color: Colors.textSecondary,
    marginTop: 2,
    lineHeight: 16,
  },
});
