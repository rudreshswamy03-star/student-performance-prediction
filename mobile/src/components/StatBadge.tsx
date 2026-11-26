import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Colors } from '../theme/colors';

interface StatBadgeProps {
  label: string;
  type?: 'success' | 'warning' | 'danger' | 'info';
}

export const StatBadge: React.FC<StatBadgeProps> = ({ label, type = 'info' }) => {
  const getBadgeStyle = () => {
    switch (type) {
      case 'success':
        return { bg: Colors.successBg, text: Colors.success, border: '#A7F3D0' };
      case 'warning':
        return { bg: Colors.warningBg, text: Colors.warning, border: '#FDE68A' };
      case 'danger':
        return { bg: Colors.dangerBg, text: Colors.danger, border: '#FECACA' };
      default:
        return { bg: Colors.infoBg, text: Colors.info, border: '#BFDBFE' };
    }
  };

  const current = getBadgeStyle();

  return (
    <View style={[styles.badge, { backgroundColor: current.bg, borderColor: current.border }]}>
      <Text style={[styles.text, { color: current.text }]}>{label}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  badge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    borderWidth: 1,
    alignSelf: 'flex-start',
  },
  text: {
    fontSize: 12,
    fontWeight: '700',
  },
});
