"""
ReconRadar APOLLO v8.0 QUANTUM — Frontend Module
-------------------------------------------------
Professional Enterprise Design System
Imported by backend.py via: from frontend import HTML_TEMPLATE
Drop-in replacement for the original frontend.py.
Compatible with all WebSocket messages: log / result / status

DESIGN CHANGES:
- Modern glassmorphism aesthetic (replacing cyberpunk)
- Refined color palette with deep navy and coral accents
- Smooth animations and transitions
- Improved readability and accessibility
- Optimized CSS with reduced repaints
- Enhanced responsive layout
"""

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ReconRadar QUANTUM | Enterprise Security Platform</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
/* ═══════════════════════════════════════════
   DESIGN SYSTEM — GLASSMORPHISM ENTERPRISE
═══════════════════════════════════════════ */
:root {
  /* Primary Palette — Deep Navy & Coral */
  --primary-900: #0f172a;
  --primary-800: #1e293b;
  --primary-700: #334155;
  --primary-600: #475569;
  --primary-500: #64748b;
  
  /* Accent — Coral Orange */
  --accent-500: #f97316;
  --accent-400: #fb923c;
  --accent-300: #fdba74;
  --accent-glow: rgba(249, 115, 22, 0.15);
  
  /* Success — Emerald */
  --success-500: #10b981;
  --success-400: #34d399;
  --success-glow: rgba(16, 185, 129, 0.15);
  
  /* Warning — Amber */
  --warning-500: #f59e0b;
  --warning-400: #fbbf24;
  
  /* Danger — Rose */
  --danger-500: #f43f5e;
  --danger-400: #fb7185;
  
  /* Info — Sky Blue */
  --info-500: #0ea5e9;
  --info-400: #38bdf8;
  
  /* Neutral Text */
  --text-100: #f8fafc;
  --text-200: #e2e8f0;
  --text-300: #cbd5e1;
  --text-400: #94a3b8;
  --text-500: #64748b;
  
  /* Glass Effect */
  --glass-bg: rgba(30, 41, 59, 0.7);
  --glass-border: rgba(255, 255, 255, 0.08);
  --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  --backdrop-blur: blur(12px);
  
  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  
  /* Spacing */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  
  /* Transitions */
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
  height: 100%;
  background: linear-gradient(135deg, var(--primary-900) 0%, #0a0f1a 50%, #0d1321 100%);
  color: var(--text-200);
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 1.6;
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Animated Background Gradient */
body::before {
  content: '';
  position: fixed;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at 20% 80%, rgba(249, 115, 22, 0.03) 0%, transparent 50%),
              radial-gradient(circle at 80% 20%, rgba(16, 185, 129, 0.03) 0%, transparent 50%),
              radial-gradient(circle at 40% 40%, rgba(14, 165, 233, 0.02) 0%, transparent 40%);
  animation: bgRotate 30s linear infinite;
  pointer-events: none;
  z-index: 0;
}

@keyframes bgRotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Custom Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { 
  background: var(--primary-600); 
  border-radius: 3px;
  transition: background var(--transition-fast);
}
::-webkit-scrollbar-thumb:hover { background: var(--primary-500); }

/* Selection */
::selection { background: var(--accent-500); color: var(--text-100); }

/* ══════════════════════════════════════════
   APP LAYOUT — Modern Grid
══════════════════════════════════════════ */
#app {
  display: grid;
  grid-template-columns: 280px 1fr 1.8fr;
  height: 100vh;
  gap: 1px;
  position: relative;
  z-index: 1;
}

/* Divider Lines */
#app > * {
  background: transparent;
}

/* ══════════════════════════════════════════
   SIDEBAR — Glass Panel
══════════════════════════════════════════ */
#sidebar {
  background: var(--glass-bg);
  backdrop-filter: var(--backdrop-blur);
  -webkit-backdrop-filter: var(--backdrop-blur);
  border-right: 1px solid var(--glass-border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* Header Section */
.sb-header {
  padding: 24px 20px;
  border-bottom: 1px solid var(--glass-border);
  flex-shrink: 0;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.logo-badge {
  width: 42px;
  height: 42px;
  background: linear-gradient(135deg, var(--accent-500), #ea580c);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  box-shadow: 0 4px 14px var(--accent-glow);
  flex-shrink: 0;
  transition: transform var(--transition-base), box-shadow var(--transition-base);
}

.logo-badge:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--accent-glow);
}

.brand-info h1 {
  font-family: var(--font-sans);
  font-size: 18px;
  font-weight: 700;
  color: var(--text-100);
  letter-spacing: -0.02em;
  margin-bottom: 2px;
}

.brand-info .subtitle {
  font-size: 11px;
  color: var(--text-400);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-weight: 500;
}

.version-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(249, 115, 22, 0.1);
  border: 1px solid rgba(249, 115, 22, 0.2);
  color: var(--accent-400);
  font-size: 10px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 12px;
  margin-top: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Connection Status */
.status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.15);
  border-radius: var(--radius-md);
  margin-top: 14px;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  font-weight: 500;
  color: var(--text-300);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--success-500);
  box-shadow: 0 0 12px var(--success-glow);
  animation: pulse 2s ease-in-out infinite;
}

.status-dot.offline {
  background: var(--danger-500);
  box-shadow: 0 0 12px rgba(244, 63, 94, 0.3);
  animation: blink 1.5s step-end infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.95); }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.timer-display {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  color: var(--warning-500);
  background: rgba(245, 158, 11, 0.08);
  padding: 4px 10px;
  border-radius: var(--radius-sm);
  border: 1px solid rgba(245, 158, 11, 0.15);
}

/* Sidebar Content */
.sb-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

/* Section Styling */
.section {
  margin-bottom: 20px;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--text-400);
  margin-bottom: 12px;
  padding-left: 4px;
}

.section-label i {
  font-size: 10px;
  color: var(--accent-400);
}

.section-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(to right, var(--glass-border), transparent);
}

/* Input Groups */
.input-group {
  position: relative;
  margin-bottom: 12px;
}

.input-group:last-child {
  margin-bottom: 0;
}

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-400);
  font-size: 12px;
  pointer-events: none;
  transition: color var(--transition-fast);
}

.input-field {
  width: 100%;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  padding: 11px 14px 11px 40px;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-100);
  outline: none;
  transition: all var(--transition-fast);
}

.input-field::placeholder {
  color: var(--text-500);
  font-size: 11px;
}

.input-field:focus {
  border-color: var(--accent-500);
  box-shadow: 0 0 0 3px var(--accent-glow);
  background: rgba(15, 23, 42, 0.8);
}

.input-field:focus + .input-icon,
.input-group:focus-within .input-icon {
  color: var(--accent-400);
}

.input-field:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

textarea.input-field {
  min-height: 70px;
  resize: vertical;
  line-height: 1.7;
  color: var(--accent-400);
}

select.input-field {
  appearance: none;
  cursor: pointer;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 36px;
}

/* Module Grid */
.modules-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.module-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  user-select: none;
}

.module-item:hover {
  background: rgba(15, 23, 42, 0.6);
  border-color: var(--primary-600);
}

.module-item input[type="checkbox"] {
  accent-color: var(--accent-500);
  width: 14px;
  height: 14px;
  cursor: pointer;
  flex-shrink: 0;
}

.module-item span {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-300);
  transition: color var(--transition-fast);
}

.module-item:has(input:checked) {
  background: rgba(249, 115, 22, 0.08);
  border-color: rgba(249, 115, 22, 0.3);
}

.module-item:has(input:checked) span {
  color: var(--accent-400);
  font-weight: 600;
}

.module-item.full-width {
  grid-column: 1 / -1;
}

/* Button Group */
.button-row {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 18px;
  font-family: var(--font-sans);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.02em;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: all var(--transition-base);
  text-transform: uppercase;
}

.btn-primary {
  flex: 1;
  background: linear-gradient(135deg, var(--accent-500), #ea580c);
  color: white;
  box-shadow: 0 4px 14px var(--accent-glow);
  position: relative;
  overflow: hidden;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.btn-primary:hover:not(:disabled)::before {
  left: 100%;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--accent-glow);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn-primary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-danger {
  padding: 12px 16px;
  background: rgba(244, 63, 94, 0.08);
  border: 1px solid rgba(244, 63, 94, 0.2);
  color: var(--danger-400);
}

.btn-danger:hover:not(:disabled) {
  background: rgba(244, 63, 94, 0.15);
  border-color: rgba(244, 63, 94, 0.3);
  box-shadow: 0 4px 14px rgba(244, 63, 94, 0.15);
}

.btn-danger:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* Footer */
.sb-footer {
  padding: 14px 20px;
  border-top: 1px solid var(--glass-border);
  flex-shrink: 0;
}

.footer-text {
  font-size: 10px;
  color: var(--text-500);
  line-height: 1.6;
}

.footer-text a {
  color: var(--info-400);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.footer-text a:hover {
  color: var(--accent-400);
  text-decoration: underline;
}

.disclaimer {
  font-size: 9px;
  color: var(--text-500);
  margin-top: 6px;
  opacity: 0.6;
  font-style: italic;
}

/* ══════════════════════════════════════════
   TERMINAL PANEL — Center Column
══════════════════════════════════════════ */
#terminal-panel {
  display: flex;
  flex-direction: column;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: var(--backdrop-blur);
  -webkit-backdrop-filter: var(--backdrop-blur);
  border-right: 1px solid var(--glass-border);
  overflow: hidden;
  position: relative;
}

/* Panel Header */
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  background: rgba(30, 41, 59, 0.5);
  border-bottom: 1px solid var(--glass-border);
  flex-shrink: 0;
}

.panel-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--text-300);
}

.panel-title i {
  color: var(--success-500);
  font-size: 10px;
}

.live-indicator {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--success-500);
  animation: livePulse 2s ease-in-out infinite;
}

@keyframes livePulse {
  0%, 100% { 
    box-shadow: 0 0 8px var(--success-glow), 0 0 16px rgba(16, 185, 129, 0.3);
    opacity: 1; 
  }
  50% { 
    box-shadow: none; 
    opacity: 0.4; 
  }
}

.panel-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-btn {
  background: transparent;
  border: 1px solid var(--glass-border);
  color: var(--text-400);
  font-family: var(--font-sans);
  font-size: 10px;
  font-weight: 500;
  padding: 5px 10px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.panel-btn:hover {
  border-color: var(--primary-600);
  color: var(--text-200);
  background: rgba(255, 255, 255, 0.03);
}

.window-controls {
  display: flex;
  gap: 6px;
  margin-left: 12px;
}

.window-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  opacity: 0.5;
}

.window-dot.red { background: #ef4444; }
.window-dot.yellow { background: #eab308; }
.window-dot.green { background: #22c55e; }

/* Terminal Body */
#terminal {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
  font-family: var(--font-mono);
  font-size: 12px;
  line-height: 1.8;
  color: var(--text-200);
  word-break: break-word;
  white-space: pre-wrap;
}

/* Log Line Styles */
.log-line {
  display: block;
  padding: 2px 0;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateX(-4px); }
  to { opacity: 1; transform: translateX(0); }
}

.log-line::before {
  content: '› ';
  color: var(--text-500);
  font-size: 10px;
  margin-right: 4px;
}

.log-error { color: var(--danger-400) !important; }
.log-warning { color: var(--warning-500) !important; }
.log-system { color: var(--text-400) !important; opacity: 0.7; }
.log-system::before { content: '⚙ '; }
.log-critical { color: var(--info-400) !important; }
.log-success { color: var(--success-400) !important; font-weight: 600; }
.log-phase {
  color: var(--accent-400) !important;
  font-weight: 700;
  padding: 6px 0 4px;
  margin-top: 8px;
  border-top: 1px dashed var(--glass-border);
  padding-top: 12px;
}

.log-phase::before { content: '▸ '; }

.blinking-cursor {
  display: inline-block;
  width: 8px;
  height: 16px;
  background: var(--accent-500);
  animation: cursorBlink 1s step-end infinite;
  vertical-align: middle;
  margin-left: 2px;
}

@keyframes cursorBlink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* Stats Bar */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border-top: 1px solid var(--glass-border);
  flex-shrink: 0;
  background: rgba(30, 41, 59, 0.3);
}

.stat-item {
  padding: 14px 12px;
  text-align: center;
  border-right: 1px solid var(--glass-border);
  transition: background var(--transition-fast);
}

.stat-item:last-child {
  border-right: none;
}

.stat-item:hover {
  background: rgba(255, 255, 255, 0.02);
}

.stat-value {
  display: block;
  font-family: var(--font-mono);
  font-size: 22px;
  font-weight: 700;
  color: var(--accent-400);
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.stat-value.danger { color: var(--danger-400); }
.stat-value.info { color: var(--info-400); }
.stat-value.success { color: var(--success-400); }

.stat-label {
  font-size: 9px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--text-500);
  margin-top: 4px;
}

/* Progress Bar */
.progress-container {
  height: 3px;
  background: var(--primary-700);
  position: relative;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--accent-500), var(--accent-400));
  width: 0%;
  transition: width 0.3s ease-out;
  box-shadow: 0 0 10px var(--accent-glow);
}

.progress-bar.active {
  animation: progressGlow 2s ease-in-out infinite;
}

@keyframes progressGlow {
  0%, 100% { box-shadow: 0 0 10px var(--accent-glow); }
  50% { box-shadow: 0 0 20px var(--accent-glow), 0 0 30px rgba(249, 115, 22, 0.3); }
}

/* ══════════════════════════════════════════
   RESULTS PANEL — Right Column
══════════════════════════════════════════ */
#results-panel {
  display: flex;
  flex-direction: column;
  background: rgba(15, 23, 42, 0.3);
  backdrop-filter: var(--backdrop-blur);
  -webkit-backdrop-filter: var(--backdrop-blur);
  overflow: hidden;
}

.results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  background: rgba(30, 41, 59, 0.5);
  border-bottom: 1px solid var(--glass-border);
  flex-shrink: 0;
}

.results-title {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--text-300);
  display: flex;
  align-items: center;
  gap: 10px;
}

.results-title i {
  color: var(--info-400);
}

.results-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: transparent;
  border: 1px solid var(--glass-border);
  color: var(--text-400);
  font-size: 16px;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  border-color: var(--primary-600);
  color: var(--text-200);
  background: rgba(255, 255, 255, 0.03);
}

.action-btn.primary:hover {
  border-color: var(--info-500);
  color: var(--info-400);
  background: rgba(14, 165, 233, 0.1);
}

/* Results Content */
#results-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
}

.result-card {
  background: rgba(30, 41, 59, 0.4);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  margin-bottom: 12px;
  transition: all var(--transition-base);
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from { 
    opacity: 0; 
    transform: translateY(10px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

.result-card:hover {
  background: rgba(30, 41, 59, 0.6);
  border-color: var(--primary-600);
  transform: translateX(2px);
}

.result-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.result-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.result-icon.subdomain { 
  background: rgba(249, 115, 22, 0.15); 
  color: var(--accent-400);
}

.result-icon.port { 
  background: rgba(16, 185, 129, 0.15); 
  color: var(--success-400);
}

.result-icon.vuln { 
  background: rgba(244, 63, 94, 0.15); 
  color: var(--danger-400);
}

.result-icon.info { 
  background: rgba(14, 165, 233, 0.15); 
  color: var(--info-400);
}

.result-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-100);
  flex: 1;
}

.result-meta {
  font-size: 10px;
  color: var(--text-500);
  font-family: var(--font-mono);
}

.result-body {
  font-size: 12px;
  color: var(--text-300);
  line-height: 1.7;
  padding-left: 42px;
}

.result-tag {
  display: inline-block;
  font-size: 9px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 2px 8px;
  border-radius: 10px;
  margin-left: 8px;
}

.result-tag.high {
  background: rgba(244, 63, 94, 0.15);
  color: var(--danger-400);
}

.result-tag.medium {
  background: rgba(245, 158, 11, 0.15);
  color: var(--warning-500);
}

.result-tag.low {
  background: rgba(16, 185, 129, 0.15);
  color: var(--success-400);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-500);
  text-align: center;
  padding: 40px 20px;
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.3;
}

.empty-state p {
  font-size: 13px;
  max-width: 280px;
  line-height: 1.6;
}

/* Responsive Adjustments */
@media (max-width: 1400px) {
  #app {
    grid-template-columns: 260px 1fr 1.5fr;
  }
}

@media (max-width: 1200px) {
  #app {
    grid-template-columns: 240px 1fr;
  }
  
  #results-panel {
    display: none;
  }
}

@media (max-width: 768px) {
  #app {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
  }
  
  #sidebar {
    border-right: none;
    border-bottom: 1px solid var(--glass-border);
    max-height: 40vh;
  }
}

/* Loading State */
.loading-skeleton {
  background: linear-gradient(
    90deg,
    rgba(255,255,255,0.03) 25%,
    rgba(255,255,255,0.06) 50%,
    rgba(255,255,255,0.03) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-md);
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Focus Visible for Accessibility */
:focus-visible {
  outline: 2px solid var(--accent-500);
  outline-offset: 2px;
}

/* Print Styles */
@media print {
  body {
    background: white;
    color: black;
  }
  
  #sidebar, .panel-header, .stats-bar, .button-row {
    display: none;
  }
  
  #terminal-panel, #results-panel {
    border: none;
  }
}
</style>
</head>
<body>
<div id="app">
  <!-- SIDEBAR -->
  <aside id="sidebar">
    <div class="sb-header">
      <div class="logo-container">
        <div class="logo-badge">
          <i class="fas fa-radar"></i>
        </div>
        <div class="brand-info">
          <h1>ReconRadar</h1>
          <div class="subtitle">Enterprise Security Platform</div>
          <div class="version-pill">
            <i class="fas fa-bolt"></i> v8.0 QUANTUM
          </div>
        </div>
      </div>
      
      <div class="status-bar">
        <div class="status-indicator">
          <span class="status-dot" id="status-dot"></span>
          <span id="connection-text">Connected</span>
        </div>
        <div class="timer-display" id="scan-timer">00:00</div>
      </div>
    </div>
    
    <div class="sb-content">
      <!-- Target Input -->
      <div class="section">
        <div class="section-label">
          <i class="fas fa-crosshairs"></i>
          <span>Target Configuration</span>
        </div>
        
        <div class="input-group">
          <input type="text" id="target-input" class="input-field" placeholder="example.com" autocomplete="off">
          <i class="fas fa-globe input-icon"></i>
        </div>
        
        <div class="input-group">
          <select id="scan-profile" class="input-field">
            <option value="quick">Quick Scan</option>
            <option value="standard" selected>Standard Scan</option>
            <option value="comprehensive">Comprehensive</option>
            <option value="stealth">Stealth Mode</option>
          </select>
          <i class="fas fa-sliders-h input-icon" style="left: auto; right: 14px; transform: none;"></i>
        </div>
      </div>
      
      <!-- Advanced Options -->
      <div class="section">
        <div class="section-label">
          <i class="fas fa-cog"></i>
          <span>Advanced Options</span>
        </div>
        
        <div class="input-group">
          <textarea id="custom-args" class="input-field" placeholder="--rate-limit 100 --timeout 30"></textarea>
          <i class="fas fa-terminal input-icon"></i>
        </div>
        
        <div class="input-group">
          <input type="text" id="api-key" class="input-field" placeholder="API Key (optional)">
          <i class="fas fa-key input-icon"></i>
        </div>
      </div>
      
      <!-- Modules -->
      <div class="section">
        <div class="section-label">
          <i class="fas fa-th-large"></i>
          <span>Reconnaissance Modules</span>
        </div>
        
        <div class="modules-grid">
          <label class="module-item">
            <input type="checkbox" data-module="dns" checked>
            <span>DNS Enumeration</span>
          </label>
          <label class="module-item">
            <input type="checkbox" data-module="whois" checked>
            <span>WHOIS Lookup</span>
          </label>
          <label class="module-item">
            <input type="checkbox" data-module="subdomains" checked>
            <span>Subdomain Scan</span>
          </label>
          <label class="module-item">
            <input type="checkbox" data-module="ports" checked>
            <span>Port Scanning</span>
          </label>
          <label class="module-item">
            <input type="checkbox" data-module="tech" checked>
            <span>Tech Stack</span>
          </label>
          <label class="module-item">
            <input type="checkbox" data-module="screenshots">
            <span>Screenshots</span>
          </label>
          <label class="module-item">
            <input type="checkbox" data-module="cloud">
            <span>Cloud Assets</span>
          </label>
          <label class="module-item">
            <input type="checkbox" data-module="vulns">
            <span>Vulnerability</span>
          </label>
          <label class="module-item full-width">
            <input type="checkbox" data-module="osint" checked>
            <span>OSINT Intelligence</span>
          </label>
          <label class="module-item full-width">
            <input type="checkbox" data-module="hash_cracker">
            <span><i class="fas fa-lock"></i> Hash Cracker</span>
          </label>
        </div>
      </div>
      
      <!-- Hash Cracker Section -->
      <div class="section" id="hash-section" style="display:none;">
        <div class="section-label">
          <i class="fas fa-key"></i>
          <span>Hash Cracker</span>
        </div>
        
        <div class="input-group">
          <input type="text" id="hash-input" class="input-field" placeholder="Enter hash to crack">
          <i class="fas fa-fingerprint input-icon"></i>
        </div>
        
        <div class="input-group">
          <select id="hash-type" class="input-field">
            <option value="auto">Auto-Detect</option>
            <option value="md5">MD5</option>
            <option value="sha1">SHA1</option>
            <option value="sha256">SHA256</option>
            <option value="sha512">SHA512</option>
            <option value="ntlm">NTLM</option>
          </select>
          <i class="fas fa-hashtag input-icon"></i>
        </div>
        
        <div class="button-row">
          <button class="btn btn-primary" id="crack-btn" style="flex:1;">
            <i class="fas fa-bolt"></i> Crack Hash
          </button>
        </div>
      </div>
    </div>
    
    <div class="sb-footer">
      <div class="footer-text">
        <i class="fas fa-shield-alt"></i> 
        Authorized security testing only.
        <br>
        <a href="#"><i class="fas fa-book"></i> Documentation</a>
      </div>
      <div class="disclaimer">
        Always obtain written permission before scanning.
      </div>
    </div>
  </aside>
  
  <!-- TERMINAL PANEL -->
  <main id="terminal-panel">
    <div class="panel-header">
      <div class="panel-title">
        <i class="fas fa-terminal"></i>
        <span>Live Console</span>
        <span class="live-indicator">
          <span class="live-dot"></span>
        </span>
      </div>
      <div class="panel-actions">
        <button class="panel-btn" id="clear-btn">
          <i class="fas fa-trash"></i> Clear
        </button>
        <button class="panel-btn" id="export-btn">
          <i class="fas fa-download"></i> Export
        </button>
        <div class="window-controls">
          <span class="window-dot red"></span>
          <span class="window-dot yellow"></span>
          <span class="window-dot green"></span>
        </div>
      </div>
    </div>
    
    <div class="progress-container">
      <div class="progress-bar" id="progress-bar"></div>
    </div>
    
    <div id="terminal">
      <span class="log-line log-system">ReconRadar QUANTUM v8.0 initialized</span>
      <span class="log-line log-system">Ready for target input...</span>
      <span class="blinking-cursor"></span>
    </div>
    
    <div class="stats-bar">
      <div class="stat-item">
        <span class="stat-value" id="stat-subdomains">0</span>
        <span class="stat-label">Subdomains</span>
      </div>
      <div class="stat-item">
        <span class="stat-value info" id="stat-ports">0</span>
        <span class="stat-label">Open Ports</span>
      </div>
      <div class="stat-item">
        <span class="stat-value danger" id="stat-vulns">0</span>
        <span class="stat-label">Vulnerabilities</span>
      </div>
    </div>
  </main>
  
  <!-- RESULTS PANEL -->
  <aside id="results-panel">
    <div class="results-header">
      <div class="results-title">
        <i class="fas fa-folder-open"></i>
        <span>Findings</span>
      </div>
      <div class="results-actions">
        <button class="action-btn primary" id="refresh-results" title="Refresh">
          <i class="fas fa-sync-alt"></i>
        </button>
        <button class="action-btn" id="filter-results" title="Filter">
          <i class="fas fa-filter"></i>
        </button>
        <button class="action-btn" id="download-report" title="Download Report">
          <i class="fas fa-file-pdf"></i>
        </button>
      </div>
    </div>
    
    <div id="results-content">
      <div class="empty-state">
        <i class="fas fa-inbox"></i>
        <p>No findings yet. Start a scan to discover assets and vulnerabilities.</p>
      </div>
    </div>
  </aside>
</div>

<script>
// ═══════════════════════════════════════════
// RECONRADAR QUANTUM — CLIENT APPLICATION
// ═══════════════════════════════════════════

(function() {
  'use strict';
  
  // DOM Elements
  const els = {
    app: document.getElementById('app'),
    sidebar: document.getElementById('sidebar'),
    targetInput: document.getElementById('target-input'),
    scanProfile: document.getElementById('scan-profile'),
    customArgs: document.getElementById('custom-args'),
    apiKey: document.getElementById('api-key'),
    scanBtn: document.getElementById('scan-btn'),
    stopBtn: document.getElementById('stop-btn'),
    statusDot: document.getElementById('status-dot'),
    connectionText: document.getElementById('connection-text'),
    scanTimer: document.getElementById('scan-timer'),
    terminal: document.getElementById('terminal'),
    progressBar: document.getElementById('progress-bar'),
    statSubdomains: document.getElementById('stat-subdomains'),
    statPorts: document.getElementById('stat-ports'),
    statVulns: document.getElementById('stat-vulns'),
    resultsContent: document.getElementById('results-content'),
    clearBtn: document.getElementById('clear-btn'),
    exportBtn: document.getElementById('export-btn'),
    hashSection: document.getElementById('hash-section'),
    hashInput: document.getElementById('hash-input'),
    hashType: document.getElementById('hash-type'),
    crackBtn: document.getElementById('crack-btn')
  };
  
  // State
  let ws = null;
  let isConnected = false;
  let isScanning = false;
  let timerInterval = null;
  let scanStartTime = null;
  let stats = { subdomains: 0, ports: 0, vulns: 0 };
  
  // Initialize
  function init() {
    setupEventListeners();
    connectWebSocket();
    updateTimerDisplay();
  }
  
  // Event Listeners
  function setupEventListeners() {
    // Module checkboxes
    document.querySelectorAll('.module-item input[type="checkbox"]').forEach(cb => {
      cb.addEventListener('change', handleModuleToggle);
    });
    
    // Clear button
    if (els.clearBtn) {
      els.clearBtn.addEventListener('click', clearTerminal);
    }
    
    // Export button
    if (els.exportBtn) {
      els.exportBtn.addEventListener('click', exportLogs);
    }
    
    // Enter key on target input
    if (els.targetInput) {
      els.targetInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !isScanning) {
          startScan();
        }
      });
    }
    
    // Hash cracker toggle
    const hashCrackerCb = document.querySelector('input[data-module="hash_cracker"]');
    if (hashCrackerCb && els.hashSection) {
      hashCrackerCb.addEventListener('change', (e) => {
        els.hashSection.style.display = e.target.checked ? 'block' : 'none';
      });
    }
    
    // Crack hash button
    if (els.crackBtn) {
      els.crackBtn.addEventListener('click', crackHash);
    }
  }
  
  // WebSocket Connection
  function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    
    try {
      ws = new WebSocket(wsUrl);
      
      ws.onopen = () => {
        isConnected = true;
        updateConnectionStatus(true);
        logToTerminal('WebSocket connected', 'system');
      };
      
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          handleWebSocketMessage(data);
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e);
        }
      };
      
      ws.onclose = () => {
        isConnected = false;
        updateConnectionStatus(false);
        logToTerminal('WebSocket disconnected. Reconnecting...', 'warning');
        setTimeout(connectWebSocket, 2000);
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        logToTerminal('Connection error', 'error');
      };
    } catch (e) {
      console.error('Failed to create WebSocket:', e);
      updateConnectionStatus(false);
    }
  }
  
  // Handle WebSocket Messages
  function handleWebSocketMessage(data) {
    switch (data.type) {
      case 'status':
        handleStatusUpdate(data);
        break;
      case 'log':
        logToTerminal(data.message, data.level || 'info');
        break;
      case 'result':
        handleResult(data);
        break;
      case 'progress':
        updateProgress(data.progress || 0);
        break;
    }
  }
  
  // Status Updates
  function handleStatusUpdate(data) {
    if (data.scanning !== undefined) {
      isScanning = data.scanning;
      if (isScanning) {
        startTimer();
        els.progressBar?.classList.add('active');
      } else {
        stopTimer();
        els.progressBar?.classList.remove('active');
        updateProgress(100);
        setTimeout(() => updateProgress(0), 500);
      }
    }
    
    if (data.target) {
      logToTerminal(`Target: ${data.target}`, 'phase');
    }
    
    if (data.modules) {
      logToTerminal(`Modules: ${data.modules.join(', ')}`, 'system');
    }
  }
  
  // Result Handling
  function handleResult(data) {
    if (data.category === 'subdomain') {
      stats.subdomains++;
      updateStat('subdomains', stats.subdomains);
    } else if (data.category === 'port') {
      stats.ports++;
      updateStat('ports', stats.ports);
    } else if (data.category === 'vulnerability') {
      stats.vulns++;
      updateStat('vulns', stats.vulns);
    }
    
    addResultCard(data);
  }
  
  // Add Result Card
  function addResultCard(data) {
    if (!els.resultsContent) return;
    
    // Remove empty state if present
    const emptyState = els.resultsContent.querySelector('.empty-state');
    if (emptyState) {
      emptyState.remove();
    }
    
    const card = document.createElement('div');
    card.className = 'result-card';
    
    const iconClass = getIconForCategory(data.category);
    const tagClass = getTagClass(data.severity);
    
    card.innerHTML = `
      <div class="result-header">
        <div class="result-icon ${iconClass}">
          <i class="fas ${getIconForType(data.category)}"></i>
        </div>
        <div>
          <div class="result-title">
            ${escapeHtml(data.title || 'Finding')}
            ${data.severity ? `<span class="result-tag ${tagClass}">${data.severity}</span>` : ''}
          </div>
          <div class="result-meta">${escapeHtml(data.meta || '')}</div>
        </div>
      </div>
      <div class="result-body">${escapeHtml(data.description || data.value || '')}</div>
    `;
    
    els.resultsContent.insertBefore(card, els.resultsContent.firstChild);
  }
  
  // Utility Functions
  function getIconForCategory(category) {
    const icons = {
      subdomain: 'subdomain',
      port: 'port',
      vulnerability: 'vuln',
      tech: 'info',
      whois: 'info',
      dns: 'info',
      osint: 'info'
    };
    return icons[category] || 'info';
  }
  
  function getIconForType(category) {
    const icons = {
      subdomain: 'fa-location-dot',
      port: 'fa-network-wired',
      vulnerability: 'fa-triangle-exclamation',
      tech: 'fa-microchip',
      whois: 'fa-id-card',
      dns: 'fa-server',
      osint: 'fa-globe'
    };
    return icons[category] || 'fa-circle-info';
  }
  
  function getTagClass(severity) {
    const classes = {
      high: 'high',
      critical: 'high',
      medium: 'medium',
      low: 'low',
      info: 'low'
    };
    return classes[severity?.toLowerCase()] || 'low';
  }
  
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
  
  // Terminal Logging
  function logToTerminal(message, level = 'info') {
    if (!els.terminal) return;
    
    // Remove blinking cursor temporarily
    const cursor = els.terminal.querySelector('.blinking-cursor');
    if (cursor) cursor.remove();
    
    const line = document.createElement('span');
    line.className = `log-line log-${level}`;
    line.textContent = message;
    
    els.terminal.appendChild(line);
    els.terminal.scrollTop = els.terminal.scrollHeight;
    
    // Re-add cursor
    const newCursor = document.createElement('span');
    newCursor.className = 'blinking-cursor';
    els.terminal.appendChild(newCursor);
    
    // Limit log lines
    const lines = els.terminal.querySelectorAll('.log-line');
    if (lines.length > 500) {
      lines[0].remove();
    }
  }
  
  function clearTerminal() {
    if (!els.terminal) return;
    
    els.terminal.innerHTML = '';
    const cursor = document.createElement('span');
    cursor.className = 'blinking-cursor';
    els.terminal.appendChild(cursor);
    
    logToTerminal('Terminal cleared', 'system');
  }
  
  function exportLogs() {
    const logs = Array.from(document.querySelectorAll('.log-line'))
      .map(line => line.textContent)
      .join('\n');
    
    const blob = new Blob([logs], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `reconradar-log-${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    
    logToTerminal('Logs exported', 'system');
  }
  
  // Statistics
  function updateStat(type, value) {
    const el = type === 'subdomains' ? els.statSubdomains :
               type === 'ports' ? els.statPorts :
               els.statVulns;
    
    if (el) {
      animateNumber(el, value);
    }
  }
  
  function animateNumber(element, target) {
    const start = parseInt(element.textContent) || 0;
    const increment = Math.ceil((target - start) / 10);
    let current = start;
    
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      element.textContent = current;
    }, 30);
  }
  
  // Progress Bar
  function updateProgress(percent) {
    if (els.progressBar) {
      els.progressBar.style.width = `${Math.min(100, Math.max(0, percent))}%`;
    }
  }
  
  // Timer
  function startTimer() {
    scanStartTime = Date.now();
    if (timerInterval) clearInterval(timerInterval);
    
    timerInterval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - scanStartTime) / 1000);
      updateTimerDisplay(elapsed);
    }, 1000);
  }
  
  function stopTimer() {
    if (timerInterval) {
      clearInterval(timerInterval);
      timerInterval = null;
    }
  }
  
  function updateTimerDisplay(seconds = 0) {
    if (!els.scanTimer) return;
    
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    els.scanTimer.textContent = 
      `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  
  // Connection Status
  function updateConnectionStatus(connected) {
    if (!els.statusDot || !els.connectionText) return;
    
    if (connected) {
      els.statusDot.classList.remove('offline');
      els.connectionText.textContent = 'Connected';
      els.connectionText.style.color = 'var(--success-500)';
    } else {
      els.statusDot.classList.add('offline');
      els.connectionText.textContent = 'Disconnected';
      els.connectionText.style.color = 'var(--danger-500)';
    }
  }
  
  // Module Toggle
  function handleModuleToggle(e) {
    const module = e.target.dataset.module;
    console.log(`Module ${module} ${e.target.checked ? 'enabled' : 'disabled'}`);
  }
  
  // Hash Cracker
  function crackHash() {
    const hash = els.hashInput?.value.trim();
    const hashType = els.hashType?.value || 'auto';
    
    if (!hash) {
      logToTerminal('Please enter a hash to crack', 'warning');
      return;
    }
    
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'crack_hash',
        hash: hash,
        hash_type: hashType
      }));
      
      logToTerminal(`Cracking hash (${hashType})...`, 'phase');
    } else {
      logToTerminal('Not connected to server', 'error');
    }
  }
  
  // Scan Functions
  function startScan() {
    const target = els.targetInput?.value.trim();
    
    if (!target) {
      logToTerminal('Please enter a target domain or IP', 'warning');
      els.targetInput?.focus();
      return;
    }
    
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      logToTerminal('Not connected to server', 'error');
      return;
    }
    
    const modules = [];
    document.querySelectorAll('.module-item input[type="checkbox"]:checked').forEach(cb => {
      if (cb.dataset.module !== 'hash_cracker') {
        modules.push(cb.dataset.module);
      }
    });
    
    const payload = {
      type: 'start_scan',
      target: target,
      profile: els.scanProfile?.value || 'standard',
      modules: modules,
      args: els.customArgs?.value.trim(),
      api_key: els.apiKey?.value.trim()
    };
    
    ws.send(JSON.stringify(payload));
    
    logToTerminal(`Initiating scan on ${target}...`, 'phase');
    logToTerminal(`Profile: ${payload.profile}`, 'system');
    logToTerminal(`Modules: ${modules.join(', ')}`, 'system');
    
    isScanning = true;
    startTimer();
    els.progressBar?.classList.add('active');
  }
  
  function stopScan() {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'stop_scan' }));
      logToTerminal('Stopping scan...', 'warning');
    }
  }
  
  // Initialize Application
  init();
  
  // Expose for debugging
  window.ReconRadar = {
    startScan,
    stopScan,
    clearTerminal,
    exportLogs,
    crackHash,
    stats,
    ws
  };
})();
</script>
</body>
</html>
"""
