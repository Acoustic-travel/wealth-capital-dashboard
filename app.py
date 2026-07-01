# import os, json, logging
# from flask import Flask, render_template, jsonify
# from google.oauth2.service_account import Credentials
# import gspread
# from datetime import datetime

# logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
# logger = logging.getLogger(__name__)

# app = Flask(__name__)
# app.config['JSON_SORT_KEYS'] = False

# # ── Config ────────────────────────────────────────────────────────────────────
# SPREADSHEET_ID = "15GG0E-pr6k-uA4DlT0TPys5scwcTgzJfRM8PcKczzqo"

# # Map tab-key → exact sheet name as it appears in your Google Sheet
# SHEETS = {
#     'rpt1': 'rpt1',
#     'rpt2': 'rpt2',
#     'rpt3': 'rpt3',
# }

# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# # ── Auth ──────────────────────────────────────────────────────────────────────
# def get_client():
#     creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
#     if not os.path.exists(creds_path):
#         raise FileNotFoundError('credentials.json not found')
#     creds  = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
#     return gspread.authorize(creds)

# # ── Data fetch ────────────────────────────────────────────────────────────────
# def fetch_sheet(tab_key):
#     """Fetch all rows from a sheet tab, return list-of-dicts."""
#     sheet_name = SHEETS.get(tab_key)
#     if not sheet_name:
#         return []
#     try:
#         client      = get_client()
#         spreadsheet = client.open_by_key(SPREADSHEET_ID)
#         ws          = spreadsheet.worksheet(sheet_name)
#         records     = ws.get_all_records()      # uses row-1 as headers
#         logger.info('Fetched %d rows from %s', len(records), sheet_name)
#         return records
#     except gspread.exceptions.WorksheetNotFound:
#         logger.warning('Sheet "%s" not found – trying by index', sheet_name)
#         # Fallback: try by position (rpt1=0, rpt2=1, rpt3=2)
#         idx = list(SHEETS.keys()).index(tab_key)
#         try:
#             ws      = client.open_by_key(SPREADSHEET_ID).get_worksheet(idx)
#             records = ws.get_all_records()
#             logger.info('Fetched %d rows from worksheet index %d', len(records), idx)
#             return records
#         except Exception as e2:
#             logger.error('Fallback fetch failed: %s', e2)
#             return get_demo(tab_key)
#     except Exception as e:
#         logger.error('fetch_sheet(%s) error: %s', tab_key, e)
#         return get_demo(tab_key)

# # ── Demo fallback ─────────────────────────────────────────────────────────────
# # def get_demo(tab_key):
# #     """Return sample data so the UI is never empty during dev/auth issues."""
# #     demo = {
# #         'rpt1': [
# #             {'Symbol':'ABCAPITAL','Date':'24/06/2026','LTP':'396','Open':'383.75','High':'396.5','Low':'381.85','Prev Close':'383.75','% Price':'3.19','High 52':'396.5','20SMA':'361.2','Range':'20.6','Range %':'5.7','URL':'https://charting.nsesindia.com/?symbol=ABCAPITAL-EQ'},
# #             {'Symbol':'ACTSTECH','Date':'24/06/2026','LTP':'42.7','Open':'42.7','High':'42.7','Low':'40.67','Prev Close':'40.67','% Price':'4.99','High 52':'42.7','20SMA':'36.3','Range':'6.4','Range %':'7.6','URL':'https://charting.nsesindia.com/?symbol=ACTSTECH-EQ'},
# #             {'Symbol':'AETHER','Date':'24/06/2026','LTP':'1358','Open':'1253.5','High':'1370.6','Low':'1232.9','Prev Close':'1244.2','% Price':'9.15','High 52':'1370.6','20SMA':'1141.1','Range':'91.8','Range %':'8.0','URL':'https://charting.nsesindia.com/?symbol=AETHER-EQ'},
# #             {'Symbol':'AKUMS','Date':'24/06/2026','LTP':'614','Open':'624.9','High':'639','Low':'611.6','Prev Close':'619.15','% Price':'-0.83','High 52':'639','20SMA':'570.8','Range':'40.8','Range %':'7.1','URL':'https://charting.nsesindia.com/?symbol=AKUMS-EQ'},
# #             {'Symbol':'AMBIKCO','Date':'24/06/2026','LTP':'1776.9','Open':'1660.7','High':'1816.3','Low':'1656.1','Prev Close':'1660.5','% Price':'7.01','High 52':'1816.3','20SMA':'1645.0','Range':'11.1','Range %':'0.7','URL':'https://charting.nsesindia.com/?symbol=AMBIKCO-EQ'},
# #         ],
# #         'rpt2': [
# #             {'Symbol':'APARINDS','Date':'24/06/2026','LTP':'16620','Open':'16654','High':'17157','Low':'16569','Prev Close':'16654','% Price':'-0.2','High 52':'17157','20SMA':'14413.0','Range':'2156.0','Range %':'15.0','URL':'https://charting.nsesindia.com/?symbol=APARINDS-EQ'},
# #             {'Symbol':'ARVIND','Date':'24/06/2026','LTP':'559','Open':'521.95','High':'561.5','Low':'516.7','Prev Close':'521.55','% Price':'7.18','High 52':'561.5','20SMA':'496.0','Range':'20.7','Range %':'4.2','URL':'https://charting.nsesindia.com/?symbol=ARVIND-EQ'},
# #         ],
# #         'rpt3': [
# #             {'Symbol':'AUROPHARMA','Date':'24/06/2026','LTP':'1531.4','Open':'1540.3','High':'1550.9','Low':'1525.2','Prev Close':'1534.2','% Price':'-0.18','High 52':'1550.9','20SMA':'1452.1','Range':'73.1','Range %':'5.0','URL':'https://charting.nsesindia.com/?symbol=AUROPHARMA-EQ'},
# #             {'Symbol':'AXISHCETF','Date':'24/06/2026','LTP':'162.4','Open':'166.19','High':'166.19','Low':'158.2','Prev Close':'162.14','% Price':'0.16','High 52':'166.19','20SMA':'158.0','Range':'0.2','Range %':'0.1','URL':'https://charting.nsesindia.com/?symbol=AXISHCETF-EQ'},
# #         ],
# #     }
# #     logger.warning('Using DEMO DATA for %s', tab_key)
# #     return demo.get(tab_key, [])

# # ── Routes ────────────────────────────────────────────────────────────────────
# @app.route('/')
# def index():
#     return render_template('dashboard.html')

# @app.route('/api/data/<tab>')
# def get_data(tab):
#     if tab not in SHEETS:
#         return jsonify({'error': 'Unknown sheet'}), 400
#     data = fetch_sheet(tab)
#     return jsonify({'sheet': tab, 'data': data, 'count': len(data),
#                     'timestamp': datetime.now().isoformat()})

# @app.route('/api/all-data')
# def get_all_data():
#     result = {tab: fetch_sheet(tab) for tab in SHEETS}
#     return jsonify({'data': result, 'timestamp': datetime.now().isoformat()})

# @app.route('/api/statistics/<tab>')
# def get_stats(tab):
#     if tab not in SHEETS:
#         return jsonify({'error': 'Unknown sheet'}), 400
#     data    = fetch_sheet(tab)
#     changes = []
#     for row in data:
#         try: changes.append(float(row.get('% Price', 0)))
#         except: pass
#     stats = {
#         'total':   len(data),
#         'gainers': sum(1 for x in changes if x > 0),
#         'losers':  sum(1 for x in changes if x < 0),
#         'avg':     round(sum(changes)/len(changes), 2) if changes else 0,
#         'max':     round(max(changes), 2) if changes else 0,
#         'min':     round(min(changes), 2) if changes else 0,
#     }
#     return jsonify(stats)

# if __name__ == '__main__':
#     print('\n' + '='*55)
#     print('  SER Fin 2026 · Live Dashboard')
#     print('='*55)
#     print(f'  Sheet ID : {SPREADSHEET_ID}')
#     print(f'  Creds    : {"✓ Found" if os.path.exists("credentials.json") else "✗ MISSING"}')
#     print('  URL      : http://localhost:5000')
#     print('='*55 + '\n')
#     app.run(debug=True, host='0.0.0.0', port=5000)






import os, json, logging
from flask import Flask, render_template, jsonify
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# ── Config ────────────────────────────────────────────────────────────────────
SPREADSHEET_ID = "15GG0E-pr6k-uA4DlT0TPys5scwcTgzJfRM8PcKczzqo"

SHEETS = {
    'rpt1': 'rpt1',
    'rpt2': 'rpt2',
    'rpt3': 'rpt3',
}

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# ── Auth ──────────────────────────────────────────────────────────────────────
def get_client():
    creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
    if not os.path.exists(creds_path):
        raise FileNotFoundError('credentials.json not found')
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    return gspread.authorize(creds)

# ── Data fetch ────────────────────────────────────────────────────────────────
def fetch_sheet(tab_key):
    """Fetch all rows from a sheet tab, return list-of-dicts."""
    sheet_name = SHEETS.get(tab_key)
    if not sheet_name:
        return []
    client = None
    try:
        client      = get_client()
        spreadsheet = client.open_by_key(SPREADSHEET_ID)


        ws = spreadsheet.worksheet(sheet_name)

        values = ws.get_all_values()

        if not values:
            return []

        print(f"\nWorksheet : {ws.title}")
        print("Headers :", values[0])

        headers = values[0]

        records = [
            dict(zip(headers, row))
            for row in values[1:]
        ]

        logger.info("Fetched %d rows from %s", len(records), ws.title)

        return records
    except gspread.exceptions.WorksheetNotFound:
        logger.warning('Sheet "%s" not found – trying by index', sheet_name)
        idx = list(SHEETS.keys()).index(tab_key)
        try:
            ws = spreadsheet.get_worksheet(idx)
            values = ws.get_all_values()

            if not values:
                return []

            print(f"\nWorksheet : {ws.title}")
            print("Headers :", values[0])

            headers = values[0]

            records = []

            for row in values[1:]:
                row += [''] * (len(headers) - len(row))
                records.append(dict(zip(headers, row)))

            logger.info("Fetched %d rows from %s", len(records), ws.title)

            return records
        except Exception as e2:
            logger.error('Fallback fetch failed: %s', e2)
            return []
    except Exception as e:
        logger.error('fetch_sheet(%s) error: %s', tab_key, e)
        return []

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/data/<tab>')
def get_data(tab):
    if tab not in SHEETS:
        return jsonify({'error': 'Unknown sheet'}), 400
    data = fetch_sheet(tab)
    return jsonify({'sheet': tab, 'data': data, 'count': len(data),
                    'timestamp': datetime.now().isoformat()})

@app.route('/api/all-data')
def get_all_data():
    result = {tab: fetch_sheet(tab) for tab in SHEETS}
    return jsonify({'data': result, 'timestamp': datetime.now().isoformat()})

@app.route('/api/statistics/<tab>')
def get_stats(tab):
    if tab not in SHEETS:
        return jsonify({'error': 'Unknown sheet'}), 400
    data    = fetch_sheet(tab)
    changes = []
    for row in data:
        try: changes.append(float(row.get('% Price', 0)))
        except: pass
    stats = {
        'total':   len(data),
        'gainers': sum(1 for x in changes if x > 0),
        'losers':  sum(1 for x in changes if x < 0),
        'avg':     round(sum(changes)/len(changes), 2) if changes else 0,
        'max':     round(max(changes), 2) if changes else 0,
        'min':     round(min(changes), 2) if changes else 0,
    }
    return jsonify(stats)

if __name__ == '__main__':
    print('\n' + '='*55)
    print('  Trading Fin 2026 · Live Dashboard')
    print('='*55)
    print(f'  Sheet ID : {SPREADSHEET_ID}')
    print(f'  Creds    : {"✓ Found" if os.path.exists("credentials.json") else "✗ MISSING"}')
    print('  URL      : http://localhost:5000')
    print('='*55 + '\n')
    app.run(debug=True, host='0.0.0.0', port=5000)