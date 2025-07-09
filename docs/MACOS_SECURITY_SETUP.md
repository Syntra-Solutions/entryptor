# macOS Security Setup Guide

## 🔒 Understanding the "Python.framework is damaged" Error

When you download and try to run the Entryptor application on macOS, you might encounter this error:

```
"Python.framework" is damaged and can't be opened. You should move it to the Trash.
```

**This is NOT a real problem!** This is macOS Gatekeeper's security feature blocking unsigned applications.

## 🚀 Solutions (Choose One)

### Method 1: Right-Click to Open (Recommended)
1. **Don't double-click** the application
2. **Right-click** on `Entryptor.app` 
3. Select **"Open"** from the context menu
4. Click **"Open"** again in the security dialog
5. The app will now run and be trusted for future use

### Method 2: Terminal Command (Advanced)
```bash
# Navigate to the app location
cd /path/to/downloaded/app

# Remove quarantine attributes
xattr -cr Entryptor.app

# Open the app
open Entryptor.app
```

### Method 3: System Preferences (One-time setup)
1. Go to **System Preferences** → **Security & Privacy**
2. Click **"General"** tab
3. Look for a message about blocked app and click **"Open Anyway"**
4. Authenticate with your password

## 🛡️ Why This Happens

macOS Gatekeeper requires applications to be:
- **Code signed** by an Apple Developer account
- **Notarized** by Apple's notarization service

Since Entryptor is an open-source project built via GitHub Actions, it's not signed with a paid Apple Developer certificate ($99/year).

## 🔍 What the Error Actually Means

The error message is misleading. It's not actually "damaged" - it's just:
- Downloaded from the internet (has quarantine attributes)
- Not signed by a registered Apple Developer
- Not notarized by Apple

## ✅ Is This Safe?

**Yes, if you downloaded from the official repository:**
- ✅ Source code is open and auditable
- ✅ Built automatically via GitHub Actions
- ✅ No malicious code can be hidden
- ✅ You can verify the build process yourself

**Only download from trusted sources:**
- ✅ Official GitHub releases
- ✅ GitHub Actions artifacts
- ❌ Random websites or file sharing services

## 🔧 For Developers: Building Locally

If you're concerned about security, you can build the app yourself:

```bash
# Clone the repository
git clone https://github.com/Syntra-Solutions/entryptor.git
cd entryptor

# Install dependencies
pip install -r requirements.txt

# Build the application
pyinstaller --onefile --windowed --name=Entryptor src/main.py

# The built app will be in dist/
```

## 🎯 Future Improvements

To eliminate this security warning, the project would need:
1. **Apple Developer Program** membership ($99/year)
2. **Code signing** certificate
3. **Notarization** process setup
4. **Automatic signing** in CI/CD pipeline

This is a common issue for all open-source macOS applications and is not specific to Entryptor.

## 📞 Still Having Issues?

1. **Check your macOS version** - older versions might have different security dialogs
2. **Verify the download** - make sure you downloaded from the official repository
3. **Try all methods** - different macOS versions respond better to different approaches
4. **Contact support** - create an issue in the GitHub repository

---

*This document is maintained as part of the Entryptor project documentation.*
