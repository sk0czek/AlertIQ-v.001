<!-- App Logo -->
<p align="center">
  <img src="logo.png" alt="AlertIQ Logo" width="200"/>
</p>

# AlertIQ – Intelligent Allegro Sales Reports

🚀 **Automated sales reporting system** for Allegro sellers. AlertIQ automates the data retrieval process, analyzes your orders from the Allegro API, and generates a beautiful, highly detailed HTML report with charts, sent directly to the specified email addresses.

Thanks to its modern architecture, the project supports both **Single-User mode (for personal use via `.env`)** and scales easily to **Multi-User mode (multiple connected accounts)** using a Supabase database.

## ✨ Main Features

### 📊 **Core Sales Analysis**
- **Daily revenue** with dynamic comparison to previous days
- **Number of orders and volume**
- **Average Order Value (AOV)** with historical trend
- **Week-over-Week (WoW)** comparison

### 🏆 **Product Performance**
- **Bestsellers:** Top 3 best-selling products of the week
- **Underperformers:** Products with low (or zero) sales (reminder to withdraw / discount them)
- **New Arrivals:** Recognition of new products introduced on a given day and monitoring of their first sale
- **Products with stopped sales:** Detection of zero sales on products that had revenue yesterday (e.g., out-of-stock alerts)

### 📈 **Advanced Metrics & Trends (SVG Charts)**
- **Built-in charts:** Auto-generated monthly/weekly trend charts in SVG embedded in the email
- **Sales stability:** Calculation of the coefficient of variation (CV standard deviation) of sales (e.g., *Moderate, Variable, Stable*)
- **Retention Rate:** Detection of returning customers (requires providing appropriate customer data)
- **Conversion Rate:** Calculation of conversion (orders to offer views)
- **Long-term Trend (Up to 30 days) and Seasonality:** Comparisons with the averaged weekly pattern

### 🔔 **Automation and Alerts**
- Automated notifications and recommendations ("Secure stock", "Consider a discount")
- Device Flow: Log in fully through the browser, easy generation of a refreshing OAuth key for the Allegro API

## 🛠️ Installation

### 1. **Download and install dependencies**
```bash
git clone <repository-url>
cd AlertIQ-v.001
pip install -r requirements.txt
```

### 2. **Environment variables configuration**
Copy the file with example variables:
```bash
cp env.example .env
```

**Required variables in `.env`:**
```env
# Allegro API
ALLEGRO_CLIENT_ID=your_client_id
ALLEGRO_CLIENT_SECRET=your_client_secret
# Remember to give the app read permissions for orders in the Allegro API!

# Email SMTP for sending reports
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_LOGIN=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com

# Optional - for local mode and a single account:
EMAIL_TO=report_recipient@example.com
```

### 3. **(Optional) Multi-user / Production Mode using Supabase**
If you want to support multiple accounts, add extra variables to `.env`:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_database_key (can be anon)
```

Create the `users` table in Supabase (SQL):
```sql
create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  email text not null,
  active boolean not null default true,
  allegro_token_json jsonb,
  refresh_token text,
  expires_at bigint
);
```
If the script fetches rows from the `users` table – each instance will be covered by the data retrieval system and emails will be sent to the given client. If Supabase fails or is not configured – the System immediately falls back to the **built-in mode**, loading the `allegro_tokens.json` file to the variables with `EMAIL_TO`!

## 🚀 Usage

### **A) Access Key Generation / Authorization**
In the first step after configuring the API, trigger key generation.
```bash
python src/get_token.py
```
*The system will provide a link or prompt you to type a short key in the Allegro browser console window.*
You can also save the tokens directly to a specific Supabase entry:
```bash
python src/get_token.py --user-email marian@example.com
# or: python src/get_token.py --user-id a1b2c3d4...
```

### **B) Running Reports**
```bash
python src/main.py
```
Immediately after connecting the data, the program will fetch yesterday's traffic, perform analysis, and finish by sending an email to the clients. You can trigger the script automatically using a System CRON.

## 🔧 Project Structure

```
AlertIQ-v.001/
├── src/
│   ├── main.py          # Main engine - handles data fetching, analysis, and mailing logic
│   ├── get_token.py     # Allegro API authorization (Device Flow) and expiration manager
│   ├── get_orders.py    # REST logic / fetch order/events from Allegro
│   ├── analyzer.py      # Statistical engine, dict operations, HTML email generation
│   ├── db.py            # Supabase client logic for Multi-user support
│   ├── test_data.py     # Environment mock data and test-data extension
│   └── mailer.py        # SMTP bridge for sending files/emails
├── .env                 # Variables file - do not commit! (API, SMTP tweaks)
├── requirements.txt     # Library dependencies
└── env.example          # Template for your .env file
```
## 🔮 Planned / Upcoming Features
- [ ] Integrated web dashboard for user administration
- [ ] Optional report delivery as converted graphics or SMS Alerts
- [ ] Deeper integration with Allegro Ads queries
- [ ] Export to Excel/PDF (Available as an email attachment on demand)