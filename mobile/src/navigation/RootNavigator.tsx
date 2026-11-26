import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { NavigationContainer } from '@react-navigation/native';

import { SplashScreen } from '../screens/SplashScreen';
import { OnboardingScreen } from '../screens/OnboardingScreen';
import { LoginScreen } from '../screens/LoginScreen';
import { RegisterScreen } from '../screens/RegisterScreen';
import { HomeScreen } from '../screens/HomeScreen';
import { AcademicsScreen } from '../screens/AcademicsScreen';
import { PredictorScreen } from '../screens/PredictorScreen';
import { EarlyWarningScreen } from '../screens/EarlyWarningScreen';
import { AnalyticsScreen } from '../screens/AnalyticsScreen';
import { ProfileScreen } from '../screens/ProfileScreen';
import { Colors } from '../theme/colors';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

// Bottom Tab Icons helper
const TabIcon = ({ label, icon, focused }: { label: string; icon: string; focused: boolean }) => (
  <View style={styles.tabIconContainer}>
    <Text style={[styles.tabEmoji, { opacity: focused ? 1 : 0.6 }]}>{icon}</Text>
    <Text style={[styles.tabLabel, focused && styles.tabLabelFocused]}>{label}</Text>
  </View>
);

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: Colors.primaryDark,
        },
        headerTintColor: '#FFFFFF',
        headerTitleStyle: {
          fontWeight: '800',
          fontSize: 16,
        },
        tabBarStyle: {
          backgroundColor: '#FFFFFF',
          borderTopColor: '#E2E8F0',
          height: 62,
          paddingBottom: 6,
          paddingTop: 6,
        },
        tabBarShowLabel: false,
      }}
    >
      <Tab.Screen
        name="HomeTab"
        component={HomeScreen}
        options={{
          headerTitle: 'EduPredict AI • Sapthagiri NPS Univ',
          tabBarIcon: ({ focused }) => <TabIcon label="Home" icon="🏠" focused={focused} />,
        }}
      />
      <Tab.Screen
        name="AcademicsTab"
        component={AcademicsScreen}
        options={{
          headerTitle: '5th Sem Core Curriculum',
          tabBarIcon: ({ focused }) => <TabIcon label="Academics" icon="📚" focused={focused} />,
        }}
      />
      <Tab.Screen
        name="PredictorTab"
        component={PredictorScreen}
        options={{
          headerTitle: 'AI Performance Predictor',
          tabBarIcon: ({ focused }) => <TabIcon label="AI Model" icon="🤖" focused={focused} />,
        }}
      />
      <Tab.Screen
        name="WarningTab"
        component={EarlyWarningScreen}
        options={{
          headerTitle: 'Early Warning Roster',
          tabBarIcon: ({ focused }) => <TabIcon label="Warning" icon="⚠️" focused={focused} />,
        }}
      />
      <Tab.Screen
        name="AnalyticsTab"
        component={AnalyticsScreen}
        options={{
          headerTitle: 'Cohort Analytics',
          tabBarIcon: ({ focused }) => <TabIcon label="Analytics" icon="📊" focused={focused} />,
        }}
      />
      <Tab.Screen
        name="ProfileTab"
        component={ProfileScreen}
        options={{
          headerTitle: 'Institutional Profile',
          tabBarIcon: ({ focused }) => <TabIcon label="Profile" icon="👤" focused={focused} />,
        }}
      />
    </Tab.Navigator>
  );
}

export const RootNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Splash"
        screenOptions={{
          headerShown: false,
          animation: 'fade',
        }}
      >
        <Stack.Screen name="Splash" component={SplashScreen} />
        <Stack.Screen name="Onboarding" component={OnboardingScreen} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Register" component={RegisterScreen} />
        <Stack.Screen name="MainTabs" component={MainTabs} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

const styles = StyleSheet.create({
  tabIconContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    minWidth: 50,
  },
  tabEmoji: {
    fontSize: 18,
  },
  tabLabel: {
    fontSize: 9,
    fontWeight: '600',
    color: '#64748B',
    marginTop: 2,
  },
  tabLabelFocused: {
    color: Colors.primary,
    fontWeight: '800',
  },
});
