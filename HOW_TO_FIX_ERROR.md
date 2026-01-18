# 🔧 How to Fix "Error Installing Requirements" on Streamlit Cloud

## Step 1: Get the Exact Error Message

**This is the most important step!**

1. In Streamlit Cloud, click **"Manage app"** (top right)
2. Click the **"Logs"** tab
3. Scroll down to find the error
4. Look for lines that say:
   - `ERROR: Could not install packages`
   - `ERROR: Failed building wheel for...`
   - `ERROR: No matching distribution found for...`
   - `ERROR: ... returned a non-zero exit status`

5. **Copy the full error message** and share it

---

## Step 2: Common Issues & Quick Fixes

### Issue A: Playwright Installation Failing

**Error might say**: `playwright` or `greenlet` related

**Quick Fix**: Temporarily remove Playwright:
1. In your repository, rename `requirements.txt` to `requirements_full.txt`
2. Rename `requirements_streamlit.txt` to `requirements.txt`
3. Push the change
4. Reboot app in Streamlit Cloud

This will deploy without Playwright first, then we can add it back.

### Issue B: lxml Building Failing

**Error might say**: `lxml` or `Failed building wheel`

**Quick Fix**: The current requirements.txt uses `lxml>=5.0.0` which should work. If not, try:
```txt
lxml==5.1.0
```

### Issue C: Greenlet Version Conflict

**Error might say**: `greenlet` version conflict

**Quick Fix**: Playwright 1.41.0 requires greenlet==3.0.3, but this might conflict. Try:
```txt
playwright==1.40.0
```

---

## Step 3: Try This Now

I've created `requirements_streamlit.txt` without Playwright. To use it:

```bash
# Option 1: Replace requirements.txt temporarily
cd "/Users/nklakshminarasimhamurthy/Desktop/infosys springboard"
cp requirements.txt requirements_backup.txt
cp requirements_streamlit.txt requirements.txt
git add requirements.txt
git commit -m "Temporarily remove Playwright for Streamlit Cloud testing"
git push personal main
```

Then reboot your app in Streamlit Cloud.

---

## Step 4: Share the Error

**Please share:**
1. The exact error message from Streamlit Cloud logs
2. Which package is failing (if shown)
3. Any traceback or additional error details

With that information, I can create a perfect `requirements.txt` that will work! 🎯

---

## Alternative: Check if It's Just Taking Time

Playwright installation can take 5-10 minutes on Streamlit Cloud because it downloads browser binaries. 

**Check**: Are you seeing "Installing..." or "Building..." that's just taking a long time? If so, wait 10 minutes before assuming it failed.
