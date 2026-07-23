
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

try:
    from streamlit_autorefresh import st_autorefresh
    HAS_AUTOREFRESH = True
except ImportError:
    HAS_AUTOREFRESH = False


st.set_page_config(page_title="Wealth Capital - Live Dashboard", page_icon=" ", layout="wide")

SPREADSHEET_ID = "15GG0E-pr6k-uA4DlT0TPys5scwcTgzJfRM8PcKczzqo"
SHEETS = {"RPT 1": "rpt1", "RPT 2": "rpt2", "RPT 3": "rpt3"}
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
IST = ZoneInfo("Asia/Kolkata")

# Columns we add ourselves for calculations — never shown in the table
INTERNAL_COLS = {"_pct"}

if HAS_AUTOREFRESH:
    st_autorefresh(interval=60_000, key="wc_autorefresh")



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


@st.cache_resource(show_spinner=False)
def get_worksheets():
    """Open the spreadsheet and list its worksheets ONCE per app lifetime.
    This is the expensive part (2 API calls) — caching it here means normal
    refreshes only cost 1 API call per tab (get_all_values), not 4+."""
    client = get_client()
    sh = client.open_by_key(SPREADSHEET_ID)
    return sh.worksheets()


@st.cache_data(ttl=60, show_spinner="Fetching live data...")
def fetch_sheet(sheet_name: str) -> pd.DataFrame:
    try:
        worksheets = get_worksheets()
        idx = list(SHEETS.values()).index(sheet_name)
        ws = worksheets[idx]  # fetch by position — matches Rpt1/Rpt2/Rpt3 regardless of exact name/case

        values = ws.get_all_values()
        if not values:
            return pd.DataFrame()
        headers, rows = values[0], values[1:]
        headers = [h.strip() for h in headers]
        rows = [r + [""] * (len(headers) - len(r)) for r in rows]
        return pd.DataFrame(rows, columns=headers)
    except gspread.exceptions.APIError as e:
        if "429" in str(e) or "Quota exceeded" in str(e):
            st.error(
                "Google Sheets API rate limit hit (too many reads per minute). "
                "This clears itself within a minute — try Refresh again shortly. "
                "If it keeps happening, close extra open tabs of this app, since each one polls independently."
            )
        else:
            st.error(f"Error fetching '{sheet_name}': {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching '{sheet_name}': {e}")
        return pd.DataFrame()



def to_float(val, default=0.0):
    try:
        return float(str(val).replace(",", "").replace("%", "").strip())
    except (ValueError, TypeError):
        return default


# def get_signal(row) -> str:
#     """BUY when Range % is between -1 and +1. If Range % can't be read
#     (e.g. the sheet's own formula returned #N/A), show HOLD rather than
#     silently guessing BUY."""
#     r = to_float(row.get("Range %"), default=None)
#     if r is None:
#         return "HOLD"
#     return "BUY" if -1 <= r <= 1 else "HOLD"


def chart_url(symbol: str) -> str:
    return f"https://gocharting.com/terminal?ticker=NSE:{symbol}"


def render_dashboard(sheet_key: str):
    df = fetch_sheet(sheet_key)
    if df.empty:
        st.warning("No data available — check the Google Sheet connection.")
        return

    df["_pct"] = df["% Price"].apply(to_float) if "% Price" in df.columns else 0.0
    
    c1, c2 = st.columns(2)
    c1.metric("Total Symbols", len(df))
    c2.metric(
        "Average Change",
        f"{round(df['_pct'].mean(), 2) if len(df) else 0}%"
    )

    fc1, fc2, fc3 = st.columns([2, 1, 1])
    search = fc1.text_input("Search", key=f"search_{sheet_key}", placeholder="Search symbol...", label_visibility="collapsed")
    sort_choice = fc2.selectbox("Sort", ["Sort by...", "Symbol (A-Z)", "LTP (High→Low)", "LTP (Low→High)"],
                                 key=f"sort_{sheet_key}", label_visibility="collapsed")
    range_choice = fc3.selectbox("Range", ["All Range %", "-1 to +1", "-3 to +3", "-5 to +5", "-7 to +7", "-10 to +10"],
                                  key=f"range_{sheet_key}", label_visibility="collapsed")

    view = df.copy()
    if search and "Symbol" in view.columns:
        view = view[view["Symbol"].astype(str).str.lower().str.contains(search.lower(), na=False)]
    if range_choice != "All Range %" and "Range %" in view.columns:
        limit = float(range_choice.split("to")[0].replace("+", "").replace("-", "").strip())
        view = view[view["Range %"].apply(to_float).between(-limit, limit)]
    if sort_choice == "Symbol (A-Z)" and "Symbol" in view.columns:
        view = view.sort_values("Symbol")
    elif sort_choice == "LTP (High→Low)" and "LTP" in view.columns:
        view = view.sort_values("LTP", key=lambda s: s.apply(to_float), ascending=False)
    elif sort_choice == "LTP (Low→High)" and "LTP" in view.columns:
        view = view.sort_values("LTP", key=lambda s: s.apply(to_float), ascending=True)

    view = view.reset_index(drop=True)

    # Show every real column from the sheet, in the sheet's own order — this
    # is what makes Rpt1/Rpt2/Rpt3 each display their own actual columns
    # (Prev. High Date, Buy, Sell, SL, PDate vs Date, etc.) automatically.
    # The raw 'url' column itself is hidden — it's only used internally to
    # power the clickable Symbol link below.
    url_col = next((c for c in df.columns if c.lower() == "url"), None)
    sheet_cols = [c for c in df.columns if c not in INTERNAL_COLS and c != url_col]
    table_df = view[sheet_cols].copy()
    # table_df["Signal"] = view["Signal"].map({"BUY": "🟢 BUY", "HOLD": "⚪ HOLD"})

    # Prefer the sheet's own pre-built url column for the Symbol link if present,
    # otherwise construct it from the symbol name.
    if url_col and "Symbol" in table_df.columns:
        sheet_urls = view[url_col].astype(str)
        fallback_urls = view["Symbol"].apply(chart_url)
        table_df["Symbol"] = sheet_urls.where(sheet_urls.str.startswith("http"), fallback_urls)
    elif "Symbol" in table_df.columns:
        table_df["Symbol"] = view["Symbol"].apply(chart_url)

    # Cosmetic only: tidy up the sheet's own error strings for display
    table_df = table_df.replace({"#N/A": "–", "#REF!": "–", "#DIV/0!": "–"})

    column_config = {}
    if "Symbol" in table_df.columns:
        column_config["Symbol"] = st.column_config.LinkColumn("Symbol", display_text=r"ticker=NSE:(.*)")

    st.caption("Click a symbol to open its live chart on GoCharting")
    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        key=f"table_{sheet_key}",
        column_config=column_config,
    )



h1, h2 = st.columns([3, 1])
with h1:
    st.title(" Wealth Capital")
    st.caption("Trading · Investment · Growth")
with h2:
    st.write("")
    st.caption(f"● Live — updated {datetime.now(IST).strftime('%H:%M:%S')} IST")
    if st.button("🔄 Refresh now"):
        fetch_sheet.clear()
        st.rerun()


tabs = st.tabs(list(SHEETS.keys()))
for label, tab in zip(SHEETS.keys(), tabs):
    with tab:
        render_dashboard(SHEETS[label])

st.markdown(
    f"<p style='text-align:center;color:gray;font-size:0.85rem;margin-top:1rem;'>"
    f"© {datetime.now(IST).year} Wealth Capital. All rights reserved.</p>",
    unsafe_allow_html=True,
)
