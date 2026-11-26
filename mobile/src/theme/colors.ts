/**
 * Sapthagiri NPS University Brand Colors & Design Tokens
 */
export const Colors = {
  // Brand colors
  primary: '#1E3A8A',       // Deep Navy Blue
  primaryDark: '#0F172A',   // Header Slate Navy
  primaryLight: '#3B82F6',  // Bright Royal Blue
  accent: '#6366F1',        // Indigo / Subtle Purple
  accentLight: '#EEF2FF',   // Subtle Purple Tint

  // Surfaces & Backgrounds
  background: '#F8FAFC',    // Light Neutral Slate
  card: '#FFFFFF',          // Crisp White Card
  surface: '#F1F5F9',       // Slightly tinted gray
  border: '#E2E8F0',        // Border gray

  // Text Hierarchy
  textPrimary: '#0F172A',   // High-contrast Navy/Charcoal
  textSecondary: '#64748B', // Muted Slate
  textMuted: '#94A3B8',     // Subtext
  textWhite: '#FFFFFF',

  // Semantic Status
  success: '#10B981',       // Distinction / Low Risk
  successBg: '#ECFDF5',
  warning: '#F59E0B',       // Borderline / Medium Risk
  warningBg: '#FFFBEB',
  danger: '#EF4444',        // High Academic Risk
  dangerBg: '#FEF2F2',
  info: '#3B82F6',
  infoBg: '#EFF6FF',
};

export const Typography = {
  headerTitle: {
    fontSize: 20,
    fontWeight: '700' as const,
    color: Colors.textWhite,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '700' as const,
    color: Colors.textPrimary,
  },
  body: {
    fontSize: 14,
    color: Colors.textPrimary,
  },
  caption: {
    fontSize: 12,
    color: Colors.textSecondary,
  },
};
