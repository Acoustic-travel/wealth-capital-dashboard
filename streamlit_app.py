
# import os
# from datetime import datetime

# import pandas as pd
# import streamlit as st
# import gspread
# import plotly.graph_objects as go
# from google.oauth2.service_account import Credentials

# try:
#     from streamlit_autorefresh import st_autorefresh
#     HAS_AUTOREFRESH = True
# except ImportError:
#     HAS_AUTOREFRESH = False

# # ── Config ────────────────────────────────────────────────────────────────
# st.set_page_config(page_title="Wealth Capital - Live Dashboard", page_icon="📈", layout="wide")

# SPREADSHEET_ID = "15GG0E-pr6k-uA4DlT0TPys5scwcTgzJfRM8PcKczzqo"
# SHEETS = {"RPT 1": "rpt1", "RPT 2": "rpt2", "RPT 3": "rpt3"}
# SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# SHOW_COLS = ["Symbol", "Date", "LTP", "Open", "High", "Low",
#              "Prev Close", "% Price", "High 52", "20SMA", "Range", "Range %"]

# if HAS_AUTOREFRESH:
#     st_autorefresh(interval=30_000, key="wc_autorefresh")


# # ── Google Sheets access ─────────────────────────────────────────────────
# @st.cache_resource(show_spinner=False)
# def get_client():
#     """Streamlit secrets first (Cloud), local credentials.json as fallback (dev only)."""
#     if "gcp_service_account" in st.secrets:
#         creds = Credentials.from_service_account_info(dict(st.secrets["gcp_service_account"]), scopes=SCOPES)
#     else:
#         creds_path = os.path.join(os.path.dirname(__file__), "credentials.json")
#         if not os.path.exists(creds_path):
#             st.error("No Google credentials found. Add `credentials.json` locally, "
#                       "or set `[gcp_service_account]` in Streamlit Cloud → Settings → Secrets.")
#             st.stop()
#         creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
#     return gspread.authorize(creds)


# @st.cache_data(ttl=30, show_spinner="Fetching live data...")
# def fetch_sheet(sheet_name: str) -> pd.DataFrame:
#     try:
#         client = get_client()
#         sh = client.open_by_key(SPREADSHEET_ID)
#         try:
#             ws = sh.worksheet(sheet_name)
#         except gspread.exceptions.WorksheetNotFound:
#             ws = sh.get_worksheet(list(SHEETS.values()).index(sheet_name))

#         values = ws.get_all_values()
#         if not values:
#             return pd.DataFrame()
#         headers, rows = values[0], values[1:]
#         rows = [r + [""] * (len(headers) - len(r)) for r in rows]
#         return pd.DataFrame(rows, columns=headers)
#     except Exception as e:
#         st.error(f"Error fetching '{sheet_name}': {e}")
#         return pd.DataFrame()


# # ── Helpers ───────────────────────────────────────────────────────────────
# def to_float(val, default=0.0):
#     try:
#         return float(str(val).replace(",", "").replace("%", "").strip())
#     except (ValueError, TypeError):
#         return default


# def get_signal(row) -> str:
#     r = to_float(row.get("Range %", 0))
#     return "BUY" if -1 <= r <= 1 else "HOLD"


# def show_candlestick_dialog(row: pd.Series, key_suffix: str):
#     @st.dialog("Stock Chart")
#     def _dialog():
#         symbol = row.get("Symbol", "-")
#         st.subheader(symbol)

#         o, h, l, c, pc = (to_float(row.get("Open")), to_float(row.get("High")),
#                            to_float(row.get("Low")), to_float(row.get("LTP")),
#                            to_float(row.get("Prev Close")))

#         fig = go.Figure(go.Candlestick(
#             x=[row.get("Date", "-")], open=[o], high=[h], low=[l], close=[c],
#             increasing_line_color="#10b981", decreasing_line_color="#ef4444",
#         ))
#         if pc:
#             fig.add_hline(y=pc, line_dash="dot", line_color="#6b7280", annotation_text="Prev Close")
#         fig.update_layout(height=350, margin=dict(l=10, r=10, t=20, b=10),
#                            xaxis_rangeslider_visible=False, showlegend=False)
#         st.plotly_chart(fig, use_container_width=True, key=f"candle_{key_suffix}")

#         c1, c2 = st.columns(2)
#         c1.write(f"**LTP:** {row.get('LTP','-')}  \n**Open:** {row.get('Open','-')}  \n"
#                  f"**High:** {row.get('High','-')}  \n**Low:** {row.get('Low','-')}")
#         c2.write(f"**Prev Close:** {row.get('Prev Close','-')}  \n**% Change:** {row.get('% Price','-')}  \n"
#                  f"**20SMA:** {row.get('20SMA','-')}  \n**Range %:** {row.get('Range %','-')}")

#         signal = get_signal(row)
#         st.markdown(f"**Signal:** {'🟢 BUY' if signal == 'BUY' else '⚪ HOLD'}")

#         if row.get("URL"):
#             st.link_button("🔗 External Chart", row["URL"], key=f"link_{key_suffix}")

#     _dialog()


# # ── Per-tab dashboard ─────────────────────────────────────────────────────
# def render_dashboard(sheet_key: str):
#     df = fetch_sheet(sheet_key)
#     if df.empty:
#         st.warning("No data available — check the Google Sheet connection.")
#         return

#     df["_pct"] = df["% Price"].apply(to_float) if "% Price" in df.columns else 0.0
#     df["Signal"] = df.apply(get_signal, axis=1)

#     c1, c2, c3, c4 = st.columns(4)
#     c1.metric("Total Symbols", len(df))
#     c2.metric("Average Change", f"{round(df['_pct'].mean(), 2) if len(df) else 0}%")
#     c3.metric("Buy", int((df["Signal"] == "BUY").sum()))
#     c4.metric("Hold", int((df["Signal"] == "HOLD").sum()))

#     fc1, fc2, fc3 = st.columns([2, 1, 1])
#     search = fc1.text_input("Search", key=f"search_{sheet_key}", placeholder="Search symbol...", label_visibility="collapsed")
#     sort_choice = fc2.selectbox("Sort", ["Sort by...", "Symbol (A-Z)", "LTP (High→Low)", "LTP (Low→High)"],
#                                  key=f"sort_{sheet_key}", label_visibility="collapsed")
#     range_choice = fc3.selectbox("Range", ["All Range %", "-1 to +1", "-3 to +3", "-5 to +5", "-7 to +7", "-10 to +10"],
#                                   key=f"range_{sheet_key}", label_visibility="collapsed")

#     view = df.copy()
#     if search:
#         view = view[view["Symbol"].astype(str).str.lower().str.contains(search.lower(), na=False)]
#     if range_choice != "All Range %":
#         limit = float(range_choice.split("to")[0].replace("+", "").replace("-", "").strip())
#         view = view[view["Range %"].apply(to_float).between(-limit, limit)]
#     if sort_choice == "Symbol (A-Z)":
#         view = view.sort_values("Symbol")
#     elif sort_choice == "LTP (High→Low)":
#         view = view.sort_values("LTP", key=lambda s: s.apply(to_float), ascending=False)
#     elif sort_choice == "LTP (Low→High)":
#         view = view.sort_values("LTP", key=lambda s: s.apply(to_float), ascending=True)

#     view = view.reset_index(drop=True)
#     cols = [c for c in SHOW_COLS if c in view.columns]
#     table_df = view[cols + ["Signal"]].copy()
#     table_df["Signal"] = table_df["Signal"].map({"BUY": "🟢 BUY", "HOLD": "⚪ HOLD"})

#     st.caption("Click a row to see its candlestick chart")
#     event = st.dataframe(
#         table_df, use_container_width=True, hide_index=True,
#         on_select="rerun", selection_mode="single-row", key=f"table_{sheet_key}",
#     )

#     if event and event.selection and event.selection.get("rows"):
#         idx = event.selection["rows"][0]
#         show_candlestick_dialog(view.iloc[idx], key_suffix=f"{sheet_key}_{idx}")


# # ── Header ────────────────────────────────────────────────────────────────
# h1, h2 = st.columns([3, 1])
# with h1:
#     st.title(" Wealth Capital")
#     st.caption("Trading · Investment · Growth")
# with h2:
#     st.write("")
#     st.caption(f"● Live — updated {datetime.now().strftime('%H:%M:%S')}")
#     if st.button("🔄 Refresh now"):
#         fetch_sheet.clear()
#         st.rerun()

# # ── Tabs ──────────────────────────────────────────────────────────────────
# tabs = st.tabs(list(SHEETS.keys()))
# for label, tab in zip(SHEETS.keys(), tabs):
#     with tab:
#         render_dashboard(SHEETS[label])

# st.caption(f"© {datetime.now().year} Wealth Capital. All rights reserved.")






"""
Wealth Capital — Live Stock Dashboard (Streamlit)
Simple, fast version: live Google Sheet data, search/sort/filter,
click a symbol to open its live chart on GoCharting.
"""

import os
from datetime import datetime

import pandas as pd
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

try:
    from streamlit_autorefresh import st_autorefresh
    HAS_AUTOREFRESH = True
except ImportError:
    HAS_AUTOREFRESH = False

# ── Config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Wealth Capital - Live Dashboard", page_icon="📈", layout="wide")

SPREADSHEET_ID = "15GG0E-pr6k-uA4DlT0TPys5scwcTgzJfRM8PcKczzqo"
SHEETS = {"RPT 1": "rpt1", "RPT 2": "rpt2", "RPT 3": "rpt3"}
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

SHOW_COLS = ["Symbol", "Date", "LTP", "Open", "High", "Low",
             "Prev Close", "% Price", "High 52", "20SMA", "Range", "Range %"]

if HAS_AUTOREFRESH:
    st_autorefresh(interval=30_000, key="wc_autorefresh")


# ── Google Sheets access ─────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_client():
    """Streamlit secrets first (Cloud), local credentials.json as fallback (dev only)."""
    if "gcp_service_account" in st.secrets:
        creds = Credentials.from_service_account_info(dict(st.secrets["gcp_service_account"]), scopes=SCOPES)
    else:
        creds_path = os.path.join(os.path.dirname(__file__), "credentials.json")
        if not os.path.exists(creds_path):
            st.error("No Google credentials found. Add `credentials.json` locally, "
                      "or set `[gcp_service_account]` in Streamlit Cloud → Settings → Secrets.")
            st.stop()
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    return gspread.authorize(creds)


@st.cache_data(ttl=30, show_spinner="Fetching live data...")
def fetch_sheet(sheet_name: str) -> pd.DataFrame:
    try:
        client = get_client()
        sh = client.open_by_key(SPREADSHEET_ID)
        try:
            ws = sh.worksheet(sheet_name)
        except gspread.exceptions.WorksheetNotFound:
            ws = sh.get_worksheet(list(SHEETS.values()).index(sheet_name))

        values = ws.get_all_values()
        if not values:
            return pd.DataFrame()
        headers, rows = values[0], values[1:]
        rows = [r + [""] * (len(headers) - len(r)) for r in rows]
        return pd.DataFrame(rows, columns=headers)
    except Exception as e:
        st.error(f"Error fetching '{sheet_name}': {e}")
        return pd.DataFrame()


# ── Helpers ───────────────────────────────────────────────────────────────
def to_float(val, default=0.0):
    try:
        return float(str(val).replace(",", "").replace("%", "").strip())
    except (ValueError, TypeError):
        return default


def get_signal(row) -> str:
    r = to_float(row.get("Range %", 0))
    return "BUY" if -1 <= r <= 1 else "HOLD"


def chart_url(symbol: str) -> str:
    return f"https://gocharting.com/terminal?ticker=NSE:{symbol}"


# ── Per-tab dashboard ─────────────────────────────────────────────────────
def render_dashboard(sheet_key: str):
    df = fetch_sheet(sheet_key)
    if df.empty:
        st.warning("No data available — check the Google Sheet connection.")
        return

    df["_pct"] = df["% Price"].apply(to_float) if "% Price" in df.columns else 0.0
    df["Signal"] = df.apply(get_signal, axis=1)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Symbols", len(df))
    c2.metric("Average Change", f"{round(df['_pct'].mean(), 2) if len(df) else 0}%")
    c3.metric("Buy", int((df["Signal"] == "BUY").sum()))
    c4.metric("Hold", int((df["Signal"] == "HOLD").sum()))

    fc1, fc2, fc3 = st.columns([2, 1, 1])
    search = fc1.text_input("Search", key=f"search_{sheet_key}", placeholder="Search symbol...", label_visibility="collapsed")
    sort_choice = fc2.selectbox("Sort", ["Sort by...", "Symbol (A-Z)", "LTP (High→Low)", "LTP (Low→High)"],
                                 key=f"sort_{sheet_key}", label_visibility="collapsed")
    range_choice = fc3.selectbox("Range", ["All Range %", "-1 to +1", "-3 to +3", "-5 to +5", "-7 to +7", "-10 to +10"],
                                  key=f"range_{sheet_key}", label_visibility="collapsed")

    view = df.copy()
    if search:
        view = view[view["Symbol"].astype(str).str.lower().str.contains(search.lower(), na=False)]
    if range_choice != "All Range %":
        limit = float(range_choice.split("to")[0].replace("+", "").replace("-", "").strip())
        view = view[view["Range %"].apply(to_float).between(-limit, limit)]
    if sort_choice == "Symbol (A-Z)":
        view = view.sort_values("Symbol")
    elif sort_choice == "LTP (High→Low)":
        view = view.sort_values("LTP", key=lambda s: s.apply(to_float), ascending=False)
    elif sort_choice == "LTP (Low→High)":
        view = view.sort_values("LTP", key=lambda s: s.apply(to_float), ascending=True)

    view = view.reset_index(drop=True)
    cols = [c for c in SHOW_COLS if c in view.columns]
    table_df = view[cols + ["Signal"]].copy()
    table_df["Signal"] = table_df["Signal"].map({"BUY": "🟢 BUY", "HOLD": "⚪ HOLD"})
    table_df["Symbol"] = view["Symbol"].apply(chart_url)

    st.caption("Click a symbol to open its live chart on GoCharting")
    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        key=f"table_{sheet_key}",
        column_config={
            "Symbol": st.column_config.LinkColumn(
                "Symbol", display_text=r"ticker=NSE:(.*)"
            )
        },
    )


# ── Header ────────────────────────────────────────────────────────────────
h1, h2 = st.columns([3, 1])
with h1:
    st.title(" Wealth Capital")
    st.caption("Trading · Investment · Growth")
with h2:
    st.write("")
    st.caption(f"● Live — updated {datetime.now().strftime('%H:%M:%S')}")
    if st.button("🔄 Refresh now"):
        fetch_sheet.clear()
        st.rerun()

# ── Tabs ──────────────────────────────────────────────────────────────────
tabs = st.tabs(list(SHEETS.keys()))
for label, tab in zip(SHEETS.keys(), tabs):
    with tab:
        render_dashboard(SHEETS[label])

st.markdown(
    f"<p style='text-align:center;color:gray;font-size:0.85rem;margin-top:1rem;'>"
    f"© {datetime.now().year} Wealth Capital. All rights reserved.</p>",
    unsafe_allow_html=True,
)