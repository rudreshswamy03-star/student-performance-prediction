# 📱 EduPredict AI — Mobile Application
### Sapthagiri NPS University, Bengaluru, Karnataka, India
#### Department of Computer Science and Engineering | 5th Semester B.E. (2026–2027)

EduPredict AI Mobile is the native mobile companion app to the EduPredict AI university platform. Developed with **React Native** and **Expo**, it delivers real-time AI performance prediction, early academic warning rosters, course tracking, and faculty mentorship protocols directly to Android and iOS devices.

---

## 🌟 Key Mobile Features

1. **🏛️ University Branding & Design:**
   - Deep Navy (`#1E3A8A`), Header Slate (`#0F172A`), and Subtle Purple (`#6366F1`) color palette.
   - Tailored specifically for Sapthagiri NPS University, Bengaluru (Department of Computer Science & Engineering, 5th Semester B.E.).

2. **🎓 Personalized Student Dashboard:**
   - Displays real-time CGPA, attendance status (with $\ge 75\%$ threshold highlight), weekly study hours, and active backlogs.
   - Early Academic Risk status indicator with automatic counseling advisories.

3. **🤖 Interactive AI Performance Predictor:**
   - Sliders and numeric input for all 6 core subjects, attendance, study hours, backlogs, and extracurriculars.
   - Connected directly to the trained **Random Forest Machine Learning model** hosted on the FastAPI backend (`/api/predict`).
   - One-touch scenario simulation presets: **Distinction**, **Average**, and **At Risk**.
   - Outputs predicted final percentage, projected SGPA, VTU performance tier, risk level, and personalized AI counseling recommendations.

4. **📚 6 Core Academic Courses:**
   - Transform Calculus, Fourier Series & Numerical Techniques (`MAT301`)
   - Data Structures & Algorithms (`CS302`)
   - Database Management Systems (`CS303`)
   - Operating Systems & Architecture (`CS304`)
   - Computer Networks & Cloud Protocols (`CS305`)
   - Data Mining & Data Wrangling (`CS306`)
   - CIE-1, CIE-2, attendance %, and VTU grade scale breakdown.

5. **⚠️ Early Academic Warning System (EAWS):**
   - Live roster categorized by **High Risk**, **Medium Risk**, and **Low Risk**.
   - Automatic triggers for attendance $< 75\%$, active backlogs, or failing CIE internal marks.
   - Quick actions to schedule faculty counseling sessions or issue academic recovery plans.

6. **📊 Class & Cohort Analytics:**
   - Distribution across Distinction ($\ge 75\%$), First Class ($60-74\%$), Second Class ($50-59\%$), and At-Risk ($< 50\%$).
   - Comparative section statistics (Section A vs Section B vs Section C).
   - Subject average benchmarks and data science correlation insights ($r = +0.78$ attendance correlation).

7. **🛡️ Role-Based Access & Demo Switcher:**
   - Student, Faculty, and Admin login modes with instant one-touch demo access.
   - Configurable Backend API host (supports Android Emulator `http://10.0.2.2:8000`, Web/iOS `http://localhost:8000`, or real device LAN IP `http://192.168.x.x:8000`).

---

## 👥 Default Demo Credentials

| Role | Institutional Email | Password | Access Rights |
| :--- | :--- | :--- | :--- |
| **🎓 Student** | `student@sapthagiri.edu.in` | `Student@123` | View own dashboard, 6 subjects, run AI simulator, view alerts |
| **👨‍🏫 Faculty** | `faculty@sapthagiri.edu.in` | `Faculty@123` | Cohort stats, student risk roster, counseling action triggers |
| **🛡️ Admin** | `admin@sapthagiri.edu.in` | `Admin@123` | System metrics, ML model status, dataset synchronization |

*(You can also click any of the "One-Touch Demo" buttons on the Login screen to instantly sign in without typing!)*

---

## 🚀 How to Run the Mobile App

### 1. Prerequisites
- **Node.js**: v18 or higher (v24 installed)
- **Python**: 3.10+ with FastAPI and Uvicorn installed (running in root directory)
- **Expo Go App**: Install free from Google Play Store (Android) or Apple App Store (iOS) on your physical phone.

---

### 2. Start the Backend API (FastAPI)
Open a terminal in the root project folder:
```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```
- API Documentation (Swagger UI): `http://localhost:8000/docs`
- Root Healthcheck: `http://localhost:8000/`

---

### 3. Start the Mobile App
Open a second terminal in the `mobile` directory:
```bash
cd mobile
npm run start
```
This will launch the Expo Developer Tools in your terminal and display a QR code.

#### Running on Your Physical Phone (Recommended):
1. Ensure your phone and computer are connected to the same Wi-Fi network.
2. Open the **Expo Go** app on Android (or Camera app on iOS).
3. Scan the QR code displayed in the terminal.
4. *Tip:* In the app, navigate to **Profile > Backend API Configuration** and enter your computer's Wi-Fi IP address (e.g. `http://192.168.1.15:8000`).

#### Running in Web Browser:
```bash
npm run web
```
Opens the app inside Google Chrome / Edge at `http://localhost:8081`.

#### Running on Android Emulator:
```bash
npm run android
```
(Requires Android Studio and an active Android Virtual Device).

---

## 📦 How to Build Standalone Android APK

To generate a standalone `.apk` file that can be installed on any Android device without Expo Go:

1. Install EAS CLI globally:
```bash
npm install -g eas-cli
```

2. Log in to your free Expo account:
```bash
eas login
```

3. Configure EAS build (already pre-configured in `app.json`):
```bash
eas build:configure
```

4. Run the APK build command:
```bash
eas build -p android --profile preview
```
- EAS will build the APK in the cloud.
- Once completed, it provides a direct download link and QR code to download the `.apk` directly to your phone!

---

## 📁 Mobile Directory Structure

```
mobile/
├── assets/                  # App icon, splash screen, adaptive icon, favicon
│   ├── icon.png
│   ├── splash.png
│   ├── adaptive-icon.png
│   └── favicon.png
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── StatBadge.tsx
│   ├── context/             # React Context state management
│   │   └── AuthContext.tsx  # User state, token persistence, demo logins
│   ├── navigation/          # React Navigation setup
│   │   └── RootNavigator.tsx # Bottom Tabs (Home, Academics, AI, Warning, Analytics, Profile)
│   ├── screens/             # Native Application Screens
│   │   ├── SplashScreen.tsx
│   │   ├── OnboardingScreen.tsx
│   │   ├── LoginScreen.tsx
│   │   ├── RegisterScreen.tsx
│   │   ├── HomeScreen.tsx
│   │   ├── AcademicsScreen.tsx
│   │   ├── PredictorScreen.tsx
│   │   ├── EarlyWarningScreen.tsx
│   │   ├── AnalyticsScreen.tsx
│   │   └── ProfileScreen.tsx
│   ├── services/            # API client
│   │   └── api.ts           # REST endpoints connecting to FastAPI
│   └── theme/               # Design tokens & color system
│       └── colors.ts        # Sapthagiri NPS University brand palette
├── App.tsx                  # Root component
├── app.json                 # Expo project configuration
├── package.json             # NPM dependencies & scripts
└── tsconfig.json            # TypeScript configuration
```

---

© 2026–2027 Sapthagiri NPS University, Bengaluru. Department of Computer Science & Engineering.
