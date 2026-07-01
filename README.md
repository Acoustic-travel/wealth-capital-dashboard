# 📊 SER Fin 2026 - Live Stock Dashboard

A beautiful, real-time stock market dashboard built with Python Flask, HTML5, CSS3, and JavaScript. Displays live data from Google Sheets with auto-updating charts and statistics.

![Dashboard Preview](#)

## ✨ Features

### Core Features
- 📊 **Live Data Updates** - Auto-refreshes every 30 seconds
- 📈 **Interactive Charts** - Price distribution and gainers/losers visualization
- 🔄 **Multiple Sheets** - Switch between RPT1, RPT2, RPT3 seamlessly
- 🔍 **Advanced Search** - Filter symbols in real-time
- 📑 **Smart Sorting** - Sort by symbol, price, or percentage change
- 📱 **Fully Responsive** - Works on desktop, tablet, and mobile devices
- 🎨 **Beautiful UI** - Modern gradient design with smooth animations
- 🚀 **Fast Performance** - Optimized for speed and efficiency

### Dashboard Components
1. **Header** - Live status indicator and last update time
2. **Navigation Tabs** - Easy sheet switching
3. **Statistics Cards** - Total symbols, average change, gainers/losers count
4. **Charts Section** - Visual data representation
5. **Data Table** - Comprehensive stock information
6. **Search & Filter** - Quick symbol lookup
7. **Detail Modal** - Click any row for detailed information

## 🚀 Quick Start

### For Linux/Mac Users:
```bash
# Make script executable
chmod +x start.sh

# Run the script
./start.sh
```

### For Windows Users:
```bash
# Double-click start.bat
# OR run in command prompt:
start.bat
```

### Manual Setup:
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Then open your browser and navigate to: **http://localhost:5000**

## 📋 Project Structure

```
ser-dashboard/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── SETUP_GUIDE.md        # Detailed setup instructions
├── README.md             # This file
├── .env.example          # Environment variables example
├── start.sh              # Quick start for Linux/Mac
├── start.bat             # Quick start for Windows
├── templates/
│   └── dashboard.html    # Main HTML template
└── static/
    ├── style.css         # Styling
    └── script.js         # Interactive functionality
```

## 🔧 Configuration

### Google Sheets Integration

The dashboard is pre-configured with:
- **Spreadsheet ID**: `15GG0E-pr6k-uA4DlT0TPys5scwcTgzJfRM8PcKczzqo`
- **Sheets**: RPT1, RPT2, RPT3

#### To use with your own Google Sheet:

1. **Get your Spreadsheet ID**
   - Open your Google Sheet
   - The ID is in the URL: `https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit`

2. **Update in app.py**
   ```python
   SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"
   ```

3. **Add your sheet names**
   ```python
   SHEETS = {
       'your_sheet_1': 0,
       'your_sheet_2': 1,
       'your_sheet_3': 2,
   }
   ```

### Setting Up Google Sheets API

#### Method 1: Using Service Account (Recommended)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Sheets API
4. Create Service Account:
   - Credentials → Create Service Account
   - Fill details and create
5. Create JSON Key:
   - Go to Service Account
   - Keys → Add Key → Create new key → JSON
   - Download and save as `credentials.json` in project root
6. Share your Google Sheet with the service account email

#### Method 2: Using OAuth2

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials
3. Download JSON and save as `token.json`

#### Method 3: No Authentication (Public Sheet)

If your Google Sheet is publicly shared, no credentials needed!

## 📊 Data Format

Your Google Sheet should have the following columns:
- Symbol
- Date
- LTP (Last Traded Price)
- Open
- High
- Low
- Prev Close
- % Price (Percentage change)
- High 52
- 20SMA (20-day Simple Moving Average)
- Range
- Range %
- URL (Optional - link to chart)

## 🌐 API Endpoints

```
GET  /                      - Main dashboard
GET  /api/data/<sheet>      - Get data from specific sheet
GET  /api/all-data          - Get all sheets data
GET  /api/statistics/<sheet> - Get statistics
```

## 🎯 Usage

1. **View Dashboard**
   - Open http://localhost:5000
   - Data loads automatically

2. **Switch Sheets**
   - Click RPT1, RPT2, or RPT3 tabs
   - Data updates instantly

3. **Search Symbols**
   - Type in search box
   - Results filter in real-time

4. **Sort Data**
   - Select sort option
   - Table reorders instantly

5. **View Details**
   - Click any row
   - Detailed modal appears

6. **Refresh Data**
   - Click 🔄 Refresh button
   - Auto-refreshes every 30 seconds

## ⚙️ Customization

### Change Refresh Interval
Edit `static/script.js`:
```javascript
setInterval(refreshAllData, 30000); // 30 seconds
```

### Customize Colors
Edit `static/style.css`:
```css
:root {
    --primary-color: #1e40af;
    --success-color: #10b981;
    --danger-color: #ef4444;
    /* ... more colors ... */
}
```

### Change Font
Edit `static/style.css`:
```css
body {
    font-family: 'Your Font Name', sans-serif;
}
```

### Add More Charts
Edit `static/script.js`:
```javascript
function updateCustomChart(data) {
    // Your chart code here
}
```

## 🐳 Docker Deployment

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t ser-dashboard .
docker run -p 5000:5000 ser-dashboard
```

## 🚀 Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Heroku
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Using AWS, Azure, or Google Cloud
Follow their Flask deployment guides with the provided files.

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Linux/Mac - Find and kill process
lsof -i :5000
kill -9 <PID>

# Windows - Use different port in app.py
app.run(port=5001)
```

### No Data Showing
- Check browser console (F12)
- Verify Google credentials
- Ensure sheet names match configuration
- Check Google Sheet sharing permissions

### Slow Performance
- Reduce refresh interval in script.js
- Optimize Google Sheets (remove unused rows)
- Use pagination for large datasets

### CORS Issues
- Ensure Flask app is serving both frontend and backend
- Check browser console for CORS errors
- No additional configuration needed for same-origin requests

## 📈 Performance Tips

1. **Limit Data Rows** - Archive old data
2. **Optimize Sheet** - Remove unnecessary columns
3. **Cache Results** - Add Redis for caching
4. **Database** - Use SQLite for better performance
5. **Compression** - Enable gzip compression

## 🔒 Security Considerations

1. **Never commit credentials.json** - Add to .gitignore
2. **Use environment variables** - For sensitive data
3. **HTTPS in production** - Use SSL/TLS
4. **Rate limiting** - Protect API endpoints
5. **Input validation** - Validate all user inputs

## 📝 License

This project is open source. Feel free to use and modify as needed.

## 🤝 Contributing

Contributions welcome! Please feel free to submit pull requests.

## 📞 Support

For issues and questions:
1. Check SETUP_GUIDE.md
2. Review browser console errors
3. Verify all files are in correct locations
4. Ensure Python packages are installed

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Chart.js](https://www.chartjs.org/)
- [CSS Grid](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)

## 🙏 Credits

Built with:
- Python Flask - Backend framework
- Google Sheets API - Data source
- Chart.js - Charting library
- CSS Grid - Responsive layout
- JavaScript - Interactivity

---

**SER Fin 2026 Dashboard** | Live Stock Market Data Visualization
Last Updated: June 2026
