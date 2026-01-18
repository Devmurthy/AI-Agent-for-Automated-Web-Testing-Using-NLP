# 🔧 Streamlit Cloud Deployment Fix

## Issue: Error Installing Requirements

If you're seeing "Error installing requirements" on Streamlit Cloud, here's what was fixed:

### Changes Made:
1. ✅ Updated `requirements.txt` to use flexible versions (`>=` instead of `==`)
2. ✅ Updated `lxml` from `4.9.3` to `>=5.0.0` (fixes Python 3.13 compatibility)
3. ✅ Added `runtime.txt` to specify Python 3.11.9 (more stable for Streamlit Cloud)

### Files Updated:
- `requirements.txt` - Now uses compatible versions
- `runtime.txt` - Specifies Python 3.11.9

---

## 🚀 Next Steps:

1. **Wait for GitHub to sync** (usually instant, but wait 30 seconds)

2. **In Streamlit Cloud:**
   - Go to your app settings
   - Click **"Reboot app"** or **"Redeploy"**
   - This will reinstall requirements with the new versions

3. **If still failing:**
   - Check the logs in Streamlit Cloud (click "Manage app" → "Logs")
   - Look for specific package errors
   - Common issues:
     - Playwright browser installation (takes time, be patient)
     - Memory limits (Streamlit Cloud free tier has limits)

---

## 📋 Alternative: Minimal Requirements (if still failing)

If the error persists, you can try a minimal requirements.txt:

```txt
streamlit>=1.29.0
langgraph>=0.2.28
langchain>=0.2.16
langchain-openai>=0.1.23
langchain-community>=0.2.10
playwright>=1.41.0
python-dotenv>=1.0.0
requests>=2.31.0
beautifulsoup4>=4.12.2
fpdf2>=2.7.9
```

(Remove Flask dependencies if only using Streamlit)

---

## 🔍 Check Logs

To see the exact error:
1. In Streamlit Cloud, click **"Manage app"**
2. Click **"Logs"** tab
3. Look for the specific package causing the error
4. Share the error message for further troubleshooting

---

**The updated requirements.txt has been pushed to your repository!** ✅
