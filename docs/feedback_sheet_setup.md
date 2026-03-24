# Feedback System Setup
1. Create a new Google Sheet.
2. Copy its ID (from the URL).
3. Replace `YOUR_SHEET_ID` in `feedback.gs` with the Sheet ID.
4. Go to Extensions > Apps Script, paste `feedback.gs` code.
5. Deploy as a Web App, set access to Anyone with link.
6. Use the Web App URL in your form handler (script.js).