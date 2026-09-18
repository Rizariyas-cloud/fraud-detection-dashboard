COLORS = {
    "bg": "#0A0E1A",
    "card": "#111827",
    "border": "#1F2937",
    "red": "#EF4444",
    "green": "#10B981",
    "blue": "#3B82F6",
    "yellow": "#F59E0B",
    "text": "#F9FAFB",
    "subtext": "#9CA3AF",
    "grid": "#1F2937"
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; }

.stApp { background-color: #0A0E1A !important; }

section[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid #1F2937 !important;
}

section[data-testid="stSidebar"] * { color: #F9FAFB !important; }

.block-container {
    padding: 1rem 2rem !important;
    max-width: 100% !important;
}

div[data-testid="metric-container"] {
    background: #111827 !important;
    border: 1px solid #1F2937 !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
}

div[data-testid="metric-container"] label {
    color: #9CA3AF !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #F9FAFB !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

.stButton > button {
    background: #3B82F6 !important;
    color: #F9FAFB !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: #2563EB !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(59,130,246,0.4) !important;
}

.metric-card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 0.5rem;
}

.metric-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    border-radius: 12px 0 0 12px;
}

.metric-card.blue::before { background: #3B82F6; }
.metric-card.red::before { background: #EF4444; }
.metric-card.green::before { background: #10B981; }
.metric-card.yellow::before { background: #F59E0B; }

.metric-label {
    color: #9CA3AF;
    font-size: 0.72rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
}

.metric-value {
    color: #F9FAFB;
    font-size: 1.9rem;
    font-weight: 700;
    line-height: 1.1;
}

.metric-value.red { color: #EF4444; }
.metric-value.green { color: #10B981; }
.metric-value.blue { color: #3B82F6; }

.metric-sub {
    color: #9CA3AF;
    font-size: 0.75rem;
    margin-top: 0.3rem;
}

.section-title {
    color: #F9FAFB;
    font-size: 1rem;
    font-weight: 600;
    margin: 1.2rem 0 0.8rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1F2937;
}

.alert-banner {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    color: #EF4444;
    font-weight: 500;
    margin-bottom: 1rem;
}

.header-wrap {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem 0 1.2rem 0;
    border-bottom: 1px solid #1F2937;
    margin-bottom: 1.5rem;
}

.brand-name {
    font-size: 1.8rem;
    font-weight: 700;
    color: #F9FAFB;
    text-shadow: 0 0 20px rgba(59,130,246,0.5);
    letter-spacing: -0.02em;
}

.brand-sub {
    color: #9CA3AF;
    font-size: 0.85rem;
    margin-top: 2px;
}

.live-wrap {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #10B981;
    font-size: 0.8rem;
    font-weight: 500;
}

.pulse {
    width: 8px; height: 8px;
    background: #10B981;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%   { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); }
    70%  { box-shadow: 0 0 0 8px rgba(16,185,129,0); }
    100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
}

.status-fraud {
    background: rgba(239,68,68,0.15);
    color: #EF4444;
    border: 1px solid rgba(239,68,68,0.3);
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}

.status-clear {
    background: rgba(16,185,129,0.15);
    color: #10B981;
    border: 1px solid rgba(16,185,129,0.3);
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}

.status-review {
    background: rgba(245,158,11,0.15);
    color: #F59E0B;
    border: 1px solid rgba(245,158,11,0.3);
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0A0E1A; }
::-webkit-scrollbar-thumb { background: #1F2937; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #374151; }
</style>
"""

def get_css():
    return CSS

def get_colors():
    return COLORS