// // Global variables
// let currentSheet = 'rpt1';
// let allData = {};
// let chartInstances = {
//     price: null,
//     gainers: null
// };

// // Initialize dashboard on page load
// document.addEventListener('DOMContentLoaded', function() {
//     console.log('Dashboard initialized');
//     loadDashboard();
    
//     // Auto-refresh data every 30 seconds
//     setInterval(refreshAllData, 50000);
    
//     // Setup search and sort
//     document.getElementById('searchInput').addEventListener('input', filterTable);
//     document.getElementById('sortSelect').addEventListener('change', sortTable);
// });

// // Load initial dashboard
// async function loadDashboard() {
//     try {
//         await loadAllData();
//         updateDashboard();
//         updateCharts();
//     } catch (error) {
//         console.error('Error loading dashboard:', error);
//         showError('Failed to load dashboard data');
//     }
// }

// // Fetch all data from API
// async function loadAllData() {
//     try {
//         const response = await fetch('/api/all-data');
//         const result = await response.json();
//         allData = result.data;
//         updateLastUpdateTime();
//         return result;
//     } catch (error) {
//         console.error('Error fetching all data:', error);
//         throw error;
//     }
// }

// // Update dashboard with current sheet data
// function updateDashboard() {
//     const data = allData[currentSheet] || [];
    
//     // Update sheet title
//     document.getElementById('sheetTitle').textContent = currentSheet.toUpperCase();
    
//     // Update table
//     updateTable(data);
    
//     // Update statistics
//     updateStatistics(data);
// }

// // Update statistics cards
// function updateStatistics(data) {
//     if (!data || data.length === 0) {
//         return;
//     }
    
//     document.getElementById('totalSymbols').textContent = data.length;
    
//     let priceChanges = [];
//     let gainers = 0;
//     let losers = 0;
    
//     data.forEach(item => {
//         const priceChange = parseFloat(item['% Price'] || 0);
//         if (!isNaN(priceChange)) {
//             priceChanges.push(priceChange);
//             if (priceChange > 0) gainers++;
//             else if (priceChange < 0) losers++;
//         }
//     });
    
//     // Calculate average
//     const avgChange = priceChanges.length > 0
//         ? (priceChanges.reduce((a, b) => a + b, 0) / priceChanges.length).toFixed(2)
//         : 0;
    
//     document.getElementById('avgChange').textContent = avgChange + '%';
//     document.getElementById('gainers').textContent = gainers;
//     document.getElementById('losers').textContent = losers;
// }

// // Update data table
// function updateTable(data) {
//     const tbody = document.getElementById('tableBody');
    
//     if (!data || data.length === 0) {
//         tbody.innerHTML = '<tr><td colspan="13" class="loading">No data available</td></tr>';
//         return;
//     }
    
//     tbody.innerHTML = data.map((item, index) => {
//         const priceChange = parseFloat(item['% Price'] || 0);
//         const statusClass = priceChange > 0 ? 'status-up' : priceChange < 0 ? 'status-down' : 'status-neutral';
//         const statusColor = priceChange > 0 ? 'success-row' : priceChange < 0 ? 'danger-row' : '';
        
//         return `
//             <tr class="${statusColor}" onclick="showDetails('${item.Symbol}', ${index})">
//                 <td><strong>${item.Symbol || '-'}</strong></td>
//                 <td>${item.Date || '-'}</td>
//                 <td>${item.LTP || '-'}</td>
//                 <td>${item.Open || '-'}</td>
//                 <td>${item.High || '-'}</td>
//                 <td>${item.Low || '-'}</td>
//                 <td>${item['Prev Close'] || '-'}</td>
//                 <td class="highlight ${statusClass}">${item['% Price'] || '-'}</td>
//                 <td>${item['High 52'] || '-'}</td>
//                 <td>${item['20SMA'] || '-'}</td>
//                 <td>${item.Range || '-'}</td>
//                 <td>${item['Range %'] || '-'}</td>
//                 <td><button class="action-btn" onclick="event.stopPropagation(); viewDetails('${item.Symbol}')">View</button></td>
//             </tr>
//         `;
//     }).join('');
// }

// // Filter table by search
// function filterTable() {
//     const searchTerm = document.getElementById('searchInput').value.toLowerCase();
//     const rows = document.querySelectorAll('#tableBody tr');
    
//     rows.forEach(row => {
//         const symbol = row.querySelector('td')?.textContent.toLowerCase() || '';
//         if (symbol.includes(searchTerm)) {
//             row.classList.remove('hidden');
//         } else {
//             row.classList.add('hidden');
//         }
//     });
// }

// // Sort table
// function sortTable() {
//     const sortValue = document.getElementById('sortSelect').value;
//     const data = allData[currentSheet] || [];
//     let sortedData = [...data];
    
//     switch(sortValue) {
//         case 'symbol':
//             sortedData.sort((a, b) => (a.Symbol || '').localeCompare(b.Symbol || ''));
//             break;
//         case 'price-high':
//             sortedData.sort((a, b) => parseFloat(b.LTP || 0) - parseFloat(a.LTP || 0));
//             break;
//         case 'price-low':
//             sortedData.sort((a, b) => parseFloat(a.LTP || 0) - parseFloat(b.LTP || 0));
//             break;
//         case 'change-high':
//             sortedData.sort((a, b) => parseFloat(b['% Price'] || 0) - parseFloat(a['% Price'] || 0));
//             break;
//         case 'change-low':
//             sortedData.sort((a, b) => parseFloat(a['% Price'] || 0) - parseFloat(b['% Price'] || 0));
//             break;
//     }
    
//     updateTable(sortedData);
// }

// // Update charts
// function updateCharts() {
//     const data = allData[currentSheet] || [];
//     updatePriceChart(data);
//     updateGainersChart(data);
// }

// // Price change distribution chart
// function updatePriceChart(data) {
//     const ctx = document.getElementById('priceChart').getContext('2d');
    
//     const priceChanges = data
//         .map(item => ({
//             symbol: item.Symbol,
//             change: parseFloat(item['% Price'] || 0)
//         }))
//         .sort((a, b) => b.change - a.change)
//         .slice(0, 10); // Top 10
    
//     if (chartInstances.price) {
//         chartInstances.price.destroy();
//     }
    
//     chartInstances.price = new Chart(ctx, {
//         type: 'bar',
//         data: {
//             labels: priceChanges.map(item => item.symbol),
//             datasets: [{
//                 label: 'Price Change %',
//                 data: priceChanges.map(item => item.change),
//                 backgroundColor: priceChanges.map(item => 
//                     item.change > 0 ? 'rgba(16, 185, 129, 0.7)' : 'rgba(239, 68, 68, 0.7)'
//                 ),
//                 borderRadius: 6,
//                 borderSkipped: false
//             }]
//         },
//         options: {
//             responsive: true,
//             maintainAspectRatio: false,
//             plugins: {
//                 legend: {
//                     display: false
//                 }
//             },
//             scales: {
//                 y: {
//                     beginAtZero: true,
//                     grid: {
//                         color: 'rgba(0, 0, 0, 0.05)'
//                     }
//                 },
//                 x: {
//                     grid: {
//                         display: false
//                     }
//                 }
//             }
//         }
//     });
// }

// // Gainers vs Losers pie chart
// function updateGainersChart(data) {
//     const ctx = document.getElementById('gainersChart').getContext('2d');
    
//     let gainers = 0, losers = 0, neutral = 0;
    
//     data.forEach(item => {
//         const change = parseFloat(item['% Price'] || 0);
//         if (change > 0) gainers++;
//         else if (change < 0) losers++;
//         else neutral++;
//     });
    
//     if (chartInstances.gainers) {
//         chartInstances.gainers.destroy();
//     }
    
//     chartInstances.gainers = new Chart(ctx, {
//         type: 'doughnut',
//         data: {
//             labels: ['Gainers', 'Losers', 'Neutral'],
//             datasets: [{
//                 data: [gainers, losers, neutral],
//                 backgroundColor: [
//                     'rgba(16, 185, 129, 0.8)',
//                     'rgba(239, 68, 68, 0.8)',
//                     'rgba(107, 114, 128, 0.8)'
//                 ],
//                 borderColor: [
//                     'rgba(16, 185, 129, 1)',
//                     'rgba(239, 68, 68, 1)',
//                     'rgba(107, 114, 128, 1)'
//                 ],
//                 borderWidth: 2
//             }]
//         },
//         options: {
//             responsive: true,
//             maintainAspectRatio: false,
//             plugins: {
//                 legend: {
//                     position: 'bottom'
//                 }
//             }
//         }
//     });
// }

// // Switch between sheets
// function switchTab(sheet) {
//     currentSheet = sheet;
    
//     // Update active tab
//     document.querySelectorAll('.tab-btn').forEach(btn => {
//         btn.classList.remove('active');
//     });
//     event.target.classList.add('active');
    
//     // Update dashboard
//     updateDashboard();
//     updateCharts();
    
//     // Reset search and sort
//     document.getElementById('searchInput').value = '';
//     document.getElementById('sortSelect').value = '';
// }

// // Show detailed view modal
// function showDetails(symbol, index) {
//     const data = allData[currentSheet] || [];
//     if (index < data.length) {
//         viewDetails(symbol);
//     }
// }

// function viewDetails(symbol) {
//     const data = allData[currentSheet] || [];
//     const item = data.find(d => d.Symbol === symbol);
    
//     if (!item) return;
    
//     const modal = document.getElementById('detailModal');
//     const modalTitle = document.getElementById('modalTitle');
//     const modalBody = document.getElementById('modalBody');
    
//     modalTitle.textContent = `${symbol} - Details`;
    
//     const priceChange = parseFloat(item['% Price'] || 0);
//     const statusClass = priceChange > 0 ? 'status-up' : priceChange < 0 ? 'status-down' : '';
    
//     modalBody.innerHTML = `
//         <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
//             <div><strong>Symbol:</strong> ${item.Symbol}</div>
//             <div><strong>Date:</strong> ${item.Date}</div>
//             <div><strong>LTP:</strong> ${item.LTP}</div>
//             <div><strong>Open:</strong> ${item.Open}</div>
//             <div><strong>High:</strong> ${item.High}</div>
//             <div><strong>Low:</strong> ${item.Low}</div>
//             <div><strong>Prev Close:</strong> ${item['Prev Close']}</div>
//             <div><strong>% Change:</strong> <span class="${statusClass}">${item['% Price']}</span></div>
//             <div><strong>High 52:</strong> ${item['High 52']}</div>
//             <div><strong>20SMA:</strong> ${item['20SMA']}</div>
//             <div><strong>Range:</strong> ${item.Range}</div>
//             <div><strong>Range %:</strong> ${item['Range %']}</div>
//         </div>
//         ${item.URL ? `<p style="margin-top: 20px;"><a href="${item.URL}" target="_blank" class="action-btn">View Chart</a></p>` : ''}
//     `;
    
//     modal.classList.add('show');
// }

// function closeModal() {
//     document.getElementById('detailModal').classList.remove('show');
// }

// // Close modal when clicking outside
// window.onclick = function(event) {
//     const modal = document.getElementById('detailModal');
//     if (event.target === modal) {
//         modal.classList.remove('show');
//     }
// }

// // Refresh all data
// async function refreshAllData() {
//     try {
//         await loadAllData();
//         updateDashboard();
//         updateCharts();
//         showSuccess('Data refreshed');
//     } catch (error) {
//         console.error('Error refreshing data:', error);
//         showError('Failed to refresh data');
//     }
// }

// // Update last update time
// function updateLastUpdateTime() {
//     const now = new Date();
//     const timeString = now.toLocaleTimeString();
//     document.getElementById('lastUpdate').textContent = `Last updated: ${timeString}`;
// }

// // Show success message
// function showSuccess(message) {
//     const toast = createToast(message, 'success');
//     document.body.appendChild(toast);
//     setTimeout(() => toast.remove(), 3000);
// }

// // Show error message
// function showError(message) {
//     const toast = createToast(message, 'error');
//     document.body.appendChild(toast);
//     setTimeout(() => toast.remove(), 5000);
// }

// // Create toast notification
// function createToast(message, type) {
//     const toast = document.createElement('div');
//     toast.className = `toast toast-${type}`;
//     toast.textContent = message;
//     toast.style.cssText = `
//         position: fixed;
//         top: 20px;
//         right: 20px;
//         padding: 15px 20px;
//         background: ${type === 'success' ? '#10b981' : '#ef4444'};
//         color: white;
//         border-radius: 6px;
//         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
//         z-index: 9999;
//         animation: slideIn 0.3s ease;
//     `;
//     return toast;
// }

// // Add action button styling
// const style = document.createElement('style');
// style.textContent = `
//     .action-btn {
//         padding: 5px 10px;
//         background: #3b82f6;
//         color: white;
//         border: none;
//         border-radius: 4px;
//         cursor: pointer;
//         font-size: 12px;
//         transition: all 0.3s ease;
//     }
    
//     .action-btn:hover {
//         background: #1e40af;
//         transform: translateY(-1px);
//     }
    
//     .success-row {
//         background: rgba(16, 185, 129, 0.05) !important;
//     }
    
//     .danger-row {
//         background: rgba(239, 68, 68, 0.05) !important;
//     }
// `;
// document.head.appendChild(style);

// console.log('Dashboard script loaded successfully');



// Global variables
let currentSheet = 'rpt1';
let allData = {};
let chartInstances = {
    price: null,
    gainers: null
};

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
    console.log('Dashboard initialized');
    loadDashboard();

    // Auto-refresh every 30 seconds
    setInterval(refreshAllData, 30000);

    document.getElementById('searchInput').addEventListener('input', filterTable);
    document.getElementById('sortSelect').addEventListener('change', sortTable);
});

// ── Load ──────────────────────────────────────────────────────────────────────
async function loadDashboard() {
    try {
        await loadAllData();
        updateDashboard();
        updateCharts();
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showError('Failed to load dashboard data');
    }
}

async function loadAllData() {
    try {
        const response = await fetch('/api/all-data');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const result = await response.json();
        allData = result.data;
        updateLastUpdateTime();
        return result;
    } catch (error) {
        console.error('Error fetching all data:', error);
        throw error;
    }
}

// ── Dashboard update ──────────────────────────────────────────────────────────
function updateDashboard() {
    const data = allData[currentSheet] || [];
    document.getElementById('sheetTitle').textContent = currentSheet.toUpperCase();
    updateTable(data);
    updateStatistics(data);
}

function updateStatistics(data) {
    if (!data || data.length === 0) return;

    document.getElementById('totalSymbols').textContent = data.length;

    let priceChanges = [], gainers = 0, losers = 0;
    data.forEach(item => {
        const pc = parseFloat(item['% Price'] || 0);
        if (!isNaN(pc)) {
            priceChanges.push(pc);
            if (pc > 0) gainers++;
            else if (pc < 0) losers++;
        }
    });

    const avgChange = priceChanges.length
        ? (priceChanges.reduce((a, b) => a + b, 0) / priceChanges.length).toFixed(2)
        : 0;

    document.getElementById('avgChange').textContent = avgChange + '%';
    document.getElementById('gainers').textContent   = gainers;
    document.getElementById('losers').textContent    = losers;
}

// ── Buy / Sell signal helper ───────────────────────────────────────────────────
/**
 * Derives a BUY / SELL / HOLD signal from the row data.
 * Logic (adjustable):
 *   BUY  – price change > 0  AND LTP > 20SMA
 *   SELL – price change < 0  AND LTP < 20SMA
 *   HOLD – everything else
 */
function getSignal(item) {
    const pc  = parseFloat(item['% Price'] || 0);
    const ltp = parseFloat(item['LTP']     || 0);
    const sma = parseFloat(item['20SMA']   || 0);

    // Prefer explicit column from sheet if present
    const sheetSignal = (item['Signal'] || item['signal'] || '').toString().trim().toUpperCase();
    if (['BUY', 'SELL', 'HOLD'].includes(sheetSignal)) return sheetSignal;

    if (pc > 0 && ltp > sma && sma > 0) return 'BUY';
    if (pc < 0 && ltp < sma && sma > 0) return 'SELL';
    return 'HOLD';
}

function signalBadge(signal) {
    const map = {
        BUY:  { cls: 'badge-buy',  label: '▲ BUY'  },
        SELL: { cls: 'badge-sell', label: '▼ SELL' },
        HOLD: { cls: 'badge-hold', label: '— HOLD' },
    };
    const s = map[signal] || map['HOLD'];
    return `<span class="signal-badge ${s.cls}">${s.label}</span>`;
}

// ── Table ─────────────────────────────────────────────────────────────────────
function updateTable(data) {
    const tbody = document.getElementById('tableBody');

    if (!data || data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="14" class="loading">No data available – check Google Sheet connection</td></tr>';
        return;
    }

    tbody.innerHTML = data.map((item, index) => {
        const pc          = parseFloat(item['% Price'] || 0);
        const statusClass = pc > 0 ? 'status-up' : pc < 0 ? 'status-down' : 'status-neutral';
        const rowColor    = pc > 0 ? 'success-row' : pc < 0 ? 'danger-row' : '';
        const signal      = getSignal(item);

        return `
            <tr class="${rowColor}" onclick="showDetails('${item.Symbol}', ${index})">
                <td><strong>${item.Symbol || '-'}</strong></td>
                <td>${item.Date || '-'}</td>
                <td>${item.LTP || '-'}</td>
                <td>${item.Open || '-'}</td>
                <td>${item.High || '-'}</td>
                <td>${item.Low || '-'}</td>
                <td>${item['Prev Close'] || '-'}</td>
                <td class="highlight ${statusClass}">${item['% Price'] || '-'}</td>
                <td>${item['High 52'] || '-'}</td>
                <td>${item['20SMA'] || '-'}</td>
                <td>${item.Range || '-'}</td>
                <td>${item['Range %'] || '-'}</td>
                <td>${signalBadge(signal)}</td>
                <td><button class="action-btn" onclick="event.stopPropagation(); viewDetails('${item.Symbol}')">View</button></td>
            </tr>
        `;
    }).join('');
}

// ── Filter / Sort ─────────────────────────────────────────────────────────────
function filterTable() {
    const term = document.getElementById('searchInput').value.toLowerCase();
    document.querySelectorAll('#tableBody tr').forEach(row => {
        const sym = row.querySelector('td')?.textContent.toLowerCase() || '';
        row.classList.toggle('hidden', !sym.includes(term));
    });
}

function sortTable() {
    const val  = document.getElementById('sortSelect').value;
    const data = allData[currentSheet] || [];
    let sorted = [...data];

    switch (val) {
        case 'symbol':      sorted.sort((a, b) => (a.Symbol || '').localeCompare(b.Symbol || '')); break;
        case 'price-high':  sorted.sort((a, b) => parseFloat(b.LTP || 0) - parseFloat(a.LTP || 0)); break;
        case 'price-low':   sorted.sort((a, b) => parseFloat(a.LTP || 0) - parseFloat(b.LTP || 0)); break;
        case 'change-high': sorted.sort((a, b) => parseFloat(b['% Price'] || 0) - parseFloat(a['% Price'] || 0)); break;
        case 'change-low':  sorted.sort((a, b) => parseFloat(a['% Price'] || 0) - parseFloat(b['% Price'] || 0)); break;
    }

    updateTable(sorted);
}

// ── Charts ────────────────────────────────────────────────────────────────────
function updateCharts() {
    const data = allData[currentSheet] || [];
    updatePriceChart(data);
    updateGainersChart(data);
}

function updatePriceChart(data) {
    const ctx = document.getElementById('priceChart').getContext('2d');
    const top = data
        .map(item => ({ symbol: item.Symbol, change: parseFloat(item['% Price'] || 0) }))
        .sort((a, b) => b.change - a.change)
        .slice(0, 10);

    if (chartInstances.price) chartInstances.price.destroy();

    chartInstances.price = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: top.map(i => i.symbol),
            datasets: [{
                label: 'Price Change %',
                data:  top.map(i => i.change),
                backgroundColor: top.map(i =>
                    i.change > 0 ? 'rgba(16, 185, 129, 0.7)' : 'rgba(239, 68, 68, 0.7)'
                ),
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.05)' } },
                x: { grid: { display: false } }
            }
        }
    });
}

function updateGainersChart(data) {
    const ctx = document.getElementById('gainersChart').getContext('2d');
    let gainers = 0, losers = 0, neutral = 0;

    data.forEach(item => {
        const c = parseFloat(item['% Price'] || 0);
        if (c > 0) gainers++; else if (c < 0) losers++; else neutral++;
    });

    if (chartInstances.gainers) chartInstances.gainers.destroy();

    chartInstances.gainers = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Gainers', 'Losers', 'Neutral'],
            datasets: [{
                data: [gainers, losers, neutral],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(107, 114, 128, 0.8)'
                ],
                borderColor: [
                    'rgba(16, 185, 129, 1)',
                    'rgba(239, 68, 68, 1)',
                    'rgba(107, 114, 128, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

// ── Tab switch ────────────────────────────────────────────────────────────────
function switchTab(sheet, btn) {
    currentSheet = sheet;

    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');

    updateDashboard();
    updateCharts();

    document.getElementById('searchInput').value  = '';
    document.getElementById('sortSelect').value   = '';
}

// ── Modal ─────────────────────────────────────────────────────────────────────
function showDetails(symbol, index) {
    const data = allData[currentSheet] || [];
    if (index < data.length) viewDetails(symbol);
}

function viewDetails(symbol) {
    const data = allData[currentSheet] || [];
    const item = data.find(d => d.Symbol === symbol);
    if (!item) return;

    const signal = getSignal(item);
    const pc     = parseFloat(item['% Price'] || 0);
    const statusClass = pc > 0 ? 'status-up' : pc < 0 ? 'status-down' : '';

    document.getElementById('modalTitle').textContent = `${symbol} – Details`;
    document.getElementById('modalBody').innerHTML = `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:15px;">
            <div><strong>Symbol:</strong> ${item.Symbol}</div>
            <div><strong>Date:</strong> ${item.Date}</div>
            <div><strong>LTP:</strong> ${item.LTP}</div>
            <div><strong>Open:</strong> ${item.Open}</div>
            <div><strong>High:</strong> ${item.High}</div>
            <div><strong>Low:</strong> ${item.Low}</div>
            <div><strong>Prev Close:</strong> ${item['Prev Close']}</div>
            <div><strong>% Change:</strong> <span class="${statusClass}">${item['% Price']}</span></div>
            <div><strong>High 52:</strong> ${item['High 52']}</div>
            <div><strong>20SMA:</strong> ${item['20SMA']}</div>
            <div><strong>Range:</strong> ${item.Range}</div>
            <div><strong>Range %:</strong> ${item['Range %']}</div>
            <div style="grid-column:1/-1"><strong>Signal:</strong> ${signalBadge(signal)}</div>
        </div>
        ${item.URL ? `<p style="margin-top:20px;"><a href="${item.URL}" target="_blank" class="action-btn">📈 View Chart</a></p>` : ''}
    `;

    document.getElementById('detailModal').classList.add('show');
}

function closeModal() {
    document.getElementById('detailModal').classList.remove('show');
}

window.onclick = function (e) {
    const modal = document.getElementById('detailModal');
    if (e.target === modal) modal.classList.remove('show');
};

// ── Refresh ───────────────────────────────────────────────────────────────────
async function refreshAllData() {
    try {
        document.getElementById('status').textContent = '● Refreshing…';
        await loadAllData();
        updateDashboard();
        updateCharts();
        document.getElementById('status').textContent = '● Live';
        showSuccess('Data refreshed from Google Sheets');
    } catch (error) {
        console.error('Refresh error:', error);
        document.getElementById('status').textContent = '● Error';
        showError('Failed to refresh – check server connection');
    }
}

function updateLastUpdateTime() {
    document.getElementById('lastUpdate').textContent =
        'Last updated: ' + new Date().toLocaleTimeString();
}

// ── Toast ─────────────────────────────────────────────────────────────────────
function showSuccess(msg) { appendToast(msg, '#10b981', 3000); }
function showError(msg)   { appendToast(msg, '#ef4444', 5000); }

function appendToast(msg, bg, duration) {
    const t = document.createElement('div');
    t.textContent = msg;
    t.style.cssText = `
        position:fixed;top:20px;right:20px;padding:14px 20px;
        background:${bg};color:#fff;border-radius:8px;
        box-shadow:0 4px 12px rgba(0,0,0,.15);z-index:9999;
        font-size:14px;font-weight:600;animation:slideIn .3s ease;
    `;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), duration);
}

// ── Injected styles ───────────────────────────────────────────────────────────
const _style = document.createElement('style');
_style.textContent = `
    .action-btn {
        padding:5px 12px;background:#3b82f6;color:#fff;
        border:none;border-radius:4px;cursor:pointer;
        font-size:12px;text-decoration:none;transition:all .2s;
    }
    .action-btn:hover { background:#1e40af;transform:translateY(-1px); }

    .success-row { background:rgba(16,185,129,.05) !important; }
    .danger-row  { background:rgba(239,68,68,.05)  !important; }

    /* Signal badges */
    .signal-badge {
        display:inline-block;padding:3px 10px;border-radius:20px;
        font-size:11px;font-weight:700;letter-spacing:.5px;white-space:nowrap;
    }
    .badge-buy  { background:#d1fae5;color:#065f46; }
    .badge-sell { background:#fee2e2;color:#991b1b; }
    .badge-hold { background:#f3f4f6;color:#4b5563; }

    @keyframes slideIn {
        from { transform:translateY(-10px);opacity:0; }
        to   { transform:translateY(0);opacity:1; }
    }
`;
document.head.appendChild(_style);

console.log('Dashboard script loaded ✓');