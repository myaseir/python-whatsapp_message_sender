# WhatsApp Automation Script (Testing Only)

This project automates sending WhatsApp messages using **Selenium** and **WhatsApp Web**.  
It reads phone numbers from a CSV file and sends a pre-defined message to each valid contact.

⚠️ **Important Warning:**  
- This script is for **educational/testing purposes only**.  
- Bulk messaging on WhatsApp **violates WhatsApp’s Terms of Service**.  
- Your number may be **blocked or banned** if you use it for spam.  
- For business use, consider the [official WhatsApp Business API](https://www.whatsapp.com/business/api).

---

## 📦 Requirements

- Python **3.8+**
- Google Chrome installed
- ChromeDriver (must match your Chrome version)  
  - [Download here](https://chromedriver.chromium.org/downloads)

### Install dependencies:
```bash
pip install pandas selenium
