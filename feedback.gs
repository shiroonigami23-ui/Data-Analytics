function doPost(e) {
  var sheet = SpreadsheetApp.openById('YOUR_SHEET_ID').getActiveSheet();
  var data = JSON.parse(e.postData.contents);
  var timestamp = new Date();
  sheet.appendRow([timestamp, data.name, data.email, data.message]);
  MailApp.sendEmail(data.email, "We got your feedback 🚀", "Hello " + data.name + ", thanks for your feedback! - Data Analytics Hub");
  MailApp.sendEmail("aryansingh19gh@gmail.com", "New Feedback Received", "Check the sheet for details.");
  return ContentService.createTextOutput("Success");
}