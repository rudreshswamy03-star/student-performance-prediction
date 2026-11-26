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

interface AtRiskStudent {
  id: string;
  usn: string;
  name: string;
  section: string;
  tier: 'High' | 'Medium' | 'Low';
  attendance: number;
  cieAvg: number;
  backlogs: number;
  triggers: string[];
}

const MOCK_WARNING_DATA: AtRiskStudent[] = [
  {
    id: '1',
    usn: 'SNPSU2024CS012',
    name: 'Kavya Murthy',
    section: 'B',
    tier: 'High',
    attendance: 64,
    cieAvg: 18,
    backlogs: 2,
    triggers: ['Attendance critically low (64%)', '2 Active backlogs in Math & DSA'],
  },
  {
    id: '2',
    usn: 'SNPSU2024CS038',
    name: 'Rohan Sharma',
    section: 'A',
    tier: 'High',
    attendance: 69,
    cieAvg: 21,
    backlogs: 1,
    triggers: ['Attendance below VTU 75% threshold', 'Failing CIE in OS'],
  },
  {
    id: '3',
    usn: 'SNPSU2024CS055',
    name: 'Pooja Hegde',
    section: 'C',
    tier: 'High',
    attendance: 71,
    cieAvg: 23,
    backlogs: 1,
    triggers: ['Borderline attendance', 'Low continuous assessment in CN'],
  },
  {
    id: '4',
    usn: 'SNPSU2024CS004',
    name: 'Abhishek Kumar',
    section: 'A',
    tier: 'Medium',
    attendance: 76,
    cieAvg: 27,
    backlogs: 0,
    triggers: ['Marginal attendance (76%)', 'Drop in CIE-2 performance'],
  },
  {
    id: '5',
    usn: 'SNPSU2024CS021',
    name: 'Darshan Gowda',
    section: 'B',
    tier: 'Medium',
    attendance: 78,
    cieAvg: 29,
    backlogs: 0,
    triggers: ['Weak internal score in Transform Calculus'],
  },
  {
    id: '6',
    usn: 'SNPSU2024CS042',
    name: 'Aditya Rao',
    section: 'A',
    tier: 'Low',
    attendance: 84.5,
    cieAvg: 43,
    backlogs: 0,
    triggers: ['Consistently high academic indicators'],
  },
  {
    id: '7',
    usn: 'SNPSU2024CS078',
    name: 'Sneha Patel',
    section: 'C',
    tier: 'Low',
    attendance: 91,
    cieAvg: 46,
    backlogs: 0,
    triggers: ['Excellent CIE track record'],
  },
];

export const EarlyWarningScreen = () => {
  const [filterTier, setFilterTier] = useState<'All' | 'High' | 'Medium' | 'Low'>('All');
  const [search, setSearch] = useState('');

  const filteredStudents = MOCK_WARNING_DATA.filter((s) => {
    const matchesTier = filterTier === 'All' || s.tier === filterTier;
    const matchesSearch =
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.usn.toLowerCase().includes(search.toLowerCase());
    return matchesTier && matchesSearch;
  });

  const highCount = MOCK_WARNING_DATA.filter((s) => s.tier === 'High').length;
  const medCount = MOCK_WARNING_DATA.filter((s) => s.tier === 'Medium').length;
  const lowCount = MOCK_WARNING_DATA.filter((s) => s.tier === 'Low').length;

  const handleAction = (student: AtRiskStudent, action: string) => {
    Alert.alert(
      `${action} Scheduled`,
      `Protocol notification triggered for ${student.name} (${student.usn}) to Section ${student.section} faculty mentor.`
    );
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Early Academic Warning System</Text>
        <Text style={styles.subtitle}>
          Sapthagiri NPS University • Proactive Retention & Counseling Roster
        </Text>
      </View>

      {/* Summary KPI Cards */}
      <View style={styles.kpiRow}>
        <View style={[styles.kpiCard, { borderColor: Colors.danger }]}>
          <Text style={[styles.kpiNum, { color: Colors.danger }]}>{highCount}</Text>
          <Text style={styles.kpiLabel}>High Risk</Text>
        </View>
        <View style={[styles.kpiCard, { borderColor: Colors.warning }]}>
          <Text style={[styles.kpiNum, { color: Colors.warning }]}>{medCount}</Text>
          <Text style={styles.kpiLabel}>Medium Risk</Text>
        </View>
        <View style={[styles.kpiCard, { borderColor: Colors.success }]}>
          <Text style={[styles.kpiNum, { color: Colors.success }]}>{lowCount}</Text>
          <Text style={styles.kpiLabel}>Low Risk</Text>
        </View>
      </View>

      {/* Search Input */}
      <TextInput
        style={styles.searchInput}
        placeholder="🔍 Search student name or USN..."
        placeholderTextColor="#94A3B8"
        value={search}
        onChangeText={setSearch}
      />

      {/* Filter Tabs */}
      <View style={styles.tabsRow}>
        {(['All', 'High', 'Medium', 'Low'] as const).map((t) => (
          <TouchableOpacity
            key={t}
            style={[styles.tab, filterTier === t && styles.activeTab]}
            onPress={() => setFilterTier(t)}
          >
            <Text style={[styles.tabText, filterTier === t && styles.activeTabText]}>
              {t === 'All' ? 'All Cohort' : `${t} Risk`}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Student List */}
      {filteredStudents.map((st) => (
        <View key={st.id} style={styles.studentCard}>
          <View style={styles.cardTop}>
            <View style={{ flex: 1 }}>
              <Text style={styles.name}>{st.name}</Text>
              <Text style={styles.usn}>
                {st.usn} • Section {st.section}
              </Text>
            </View>
            <View
              style={[
                styles.tierBadge,
                st.tier === 'High'
                  ? styles.tierHigh
                  : st.tier === 'Medium'
                  ? styles.tierMedium
                  : styles.tierLow,
              ]}
            >
              <Text
                style={[
                  styles.tierText,
                  st.tier === 'High'
                    ? { color: Colors.danger }
                    : st.tier === 'Medium'
                    ? { color: Colors.warning }
                    : { color: Colors.success },
                ]}
              >
                ● {st.tier} Risk
              </Text>
            </View>
          </View>

          {/* Quick Stats Bar */}
          <View style={styles.statsBar}>
            <View style={styles.statItem}>
              <Text
                style={[
                  styles.statVal,
                  { color: st.attendance < 75 ? Colors.danger : Colors.textPrimary },
                ]}
              >
                {st.attendance}%
              </Text>
              <Text style={styles.statLabel}>Attendance</Text>
            </View>
            <View style={styles.statDivider} />
            <View style={styles.statItem}>
              <Text style={styles.statVal}>{st.cieAvg}/50</Text>
              <Text style={styles.statLabel}>Avg CIE</Text>
            </View>
            <View style={styles.statDivider} />
            <View style={styles.statItem}>
              <Text
                style={[
                  styles.statVal,
                  { color: st.backlogs > 0 ? Colors.danger : Colors.success },
                ]}
              >
                {st.backlogs}
              </Text>
              <Text style={styles.statLabel}>Backlogs</Text>
            </View>
          </View>

          {/* Risk Triggers */}
          <View style={styles.triggersBox}>
            <Text style={styles.triggersTitle}>Key Early Indicators:</Text>
            {st.triggers.map((trig, idx) => (
              <Text key={idx} style={styles.triggerText}>
                • {trig}
              </Text>
            ))}
          </View>

          {/* Action Buttons */}
          <View style={styles.actionsRow}>
            <TouchableOpacity
              style={styles.actionBtnOutline}
              onPress={() => handleAction(st, 'Counseling Session')}
            >
              <Text style={styles.actionBtnOutlineText}>📞 Schedule Mentor</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={styles.actionBtnFilled}
              onPress={() => handleAction(st, 'Academic Recovery Plan')}
            >
              <Text style={styles.actionBtnFilledText}>📋 Recovery Plan</Text>
            </TouchableOpacity>
          </View>
        </View>
      ))}

      {/* Intervention Protocol Guide */}
      <View style={styles.protocolCard}>
        <Text style={styles.protocolTitle}>📌 University Intervention Framework</Text>
        <Text style={styles.protocolBody}>
          • High Risk: Requires mandatory in-person session with Faculty Mentor within 48 hours and parent notification.
          {'\n'}• Medium Risk: Remedial assignment packs & weekly attendance monitoring.
          {'\n'}• Attendance &lt; 75%: Form 3B non-eligibility notice issued before final exam hall ticket release.
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
  kpiRow: {
    flexDirection: 'row',
    gap: 10,
    marginBottom: 16,
  },
  kpiCard: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    borderRadius: 14,
    padding: 14,
    alignItems: 'center',
    borderWidth: 1.5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 3,
    elevation: 1,
  },
  kpiNum: {
    fontSize: 24,
    fontWeight: '900',
  },
  kpiLabel: {
    fontSize: 11,
    color: Colors.textSecondary,
    fontWeight: '600',
    marginTop: 2,
  },
  searchInput: {
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: Colors.border,
    borderRadius: 12,
    paddingHorizontal: 14,
    paddingVertical: 10,
    fontSize: 13,
    color: Colors.textPrimary,
    marginBottom: 12,
  },
  tabsRow: {
    flexDirection: 'row',
    gap: 6,
    marginBottom: 14,
  },
  tab: {
    flex: 1,
    paddingVertical: 8,
    borderRadius: 8,
    alignItems: 'center',
    backgroundColor: '#E2E8F0',
  },
  activeTab: {
    backgroundColor: Colors.primary,
  },
  tabText: {
    fontSize: 12,
    fontWeight: '600',
    color: Colors.textSecondary,
  },
  activeTabText: {
    color: '#FFFFFF',
    fontWeight: '700',
  },
  studentCard: {
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
  cardTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  name: {
    fontSize: 15,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  usn: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  tierBadge: {
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 6,
  },
  tierHigh: {
    backgroundColor: Colors.dangerBg,
  },
  tierMedium: {
    backgroundColor: Colors.warningBg,
  },
  tierLow: {
    backgroundColor: Colors.successBg,
  },
  tierText: {
    fontSize: 11,
    fontWeight: '700',
  },
  statsBar: {
    flexDirection: 'row',
    backgroundColor: '#F8FAFC',
    borderRadius: 8,
    paddingVertical: 8,
    justifyContent: 'space-around',
    marginBottom: 10,
  },
  statItem: {
    alignItems: 'center',
  },
  statVal: {
    fontSize: 13,
    fontWeight: '700',
    color: Colors.textPrimary,
  },
  statLabel: {
    fontSize: 10,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  statDivider: {
    width: 1,
    height: 20,
    backgroundColor: '#E2E8F0',
  },
  triggersBox: {
    backgroundColor: '#FEF2F2',
    padding: 10,
    borderRadius: 8,
    marginBottom: 12,
  },
  triggersTitle: {
    fontSize: 11,
    fontWeight: '700',
    color: '#991B1B',
    marginBottom: 4,
  },
  triggerText: {
    fontSize: 11,
    color: '#B91C1C',
    lineHeight: 16,
  },
  actionsRow: {
    flexDirection: 'row',
    gap: 8,
  },
  actionBtnOutline: {
    flex: 1,
    borderWidth: 1,
    borderColor: Colors.primary,
    borderRadius: 8,
    paddingVertical: 8,
    alignItems: 'center',
  },
  actionBtnOutlineText: {
    fontSize: 12,
    fontWeight: '700',
    color: Colors.primary,
  },
  actionBtnFilled: {
    flex: 1,
    backgroundColor: Colors.primary,
    borderRadius: 8,
    paddingVertical: 8,
    alignItems: 'center',
  },
  actionBtnFilledText: {
    fontSize: 12,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  protocolCard: {
    backgroundColor: '#EFF6FF',
    borderWidth: 1,
    borderColor: '#BFDBFE',
    borderRadius: 12,
    padding: 14,
    marginTop: 8,
  },
  protocolTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: Colors.primary,
    marginBottom: 6,
  },
  protocolBody: {
    fontSize: 11,
    color: '#1E3A8A',
    lineHeight: 18,
  },
});
