import React from 'react';

const BACKEND = 'http://127.0.0.1:8000';

const CHART_LABELS = {
    'histogram.png': '📊 Distribution Histogram',
    'heatmap.png':   '🌡️ Correlation Heatmap',
    'bar.png':       '📈 Category Distribution',
    'trend.png':     '📉 Trend Over Rows',
};

function Charts({ data, onReset }) {
    const { summary, charts, predictions, report_url } = data;

    const rows  = summary?.shape?.[0] ?? '—';
    const cols  = summary?.shape?.[1] ?? '—';
    const missing = summary?.missing
        ? Object.values(summary.missing).reduce((a, b) => a + b, 0)
        : 0;
    const numCols = summary?.columns?.length ?? 0;

    const predEntries = predictions && !predictions.message
        ? Object.entries(predictions)
        : [];

    return (
        <div className="dashboard-container">
            {/* ── Header ── */}
            <div className="dashboard-header">
                <h2>Analysis Results</h2>
                <div className="actions">
                    {report_url && (
                        <a
                            href={`${BACKEND}${report_url}`}
                            download
                            className="btn btn-primary"
                            target="_blank"
                            rel="noreferrer"
                            id="download-report-btn"
                        >
                            📄 Download PDF
                        </a>
                    )}
                    <button onClick={onReset} className="btn btn-secondary" id="analyze-another-btn">
                        ↺ Analyze Another
                    </button>
                </div>
            </div>

            {/* ── Stats Bar ── */}
            <div className="stats-bar">
                <div className="stat-card">
                    <div className="stat-icon blue">📋</div>
                    <div>
                        <div className="stat-label">Rows</div>
                        <div className="stat-value">{rows.toLocaleString?.() ?? rows}</div>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon purple">🗂️</div>
                    <div>
                        <div className="stat-label">Columns</div>
                        <div className="stat-value">{numCols}</div>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon cyan">🔍</div>
                    <div>
                        <div className="stat-label">Missing Vals</div>
                        <div className="stat-value">{missing}</div>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon amber">📈</div>
                    <div>
                        <div className="stat-label">Charts</div>
                        <div className="stat-value">{charts?.length ?? 0}</div>
                    </div>
                </div>
            </div>

            {/* ── Info Grid ── */}
            <div className="dashboard-grid">
                {/* Summary Card */}
                <div className="card">
                    <div className="card-header">
                        <span className="card-icon">📋</span>
                        <h3>Dataset Overview</h3>
                    </div>
                    <div className="summary-row">
                        <span className="label">Shape</span>
                        <span className="value">{rows} × {cols}</span>
                    </div>
                    <div className="summary-row">
                        <span className="label">Total Cells</span>
                        <span className="value">{(rows * cols).toLocaleString?.() ?? '—'}</span>
                    </div>
                    <div className="summary-row">
                        <span className="label">Missing Values</span>
                        <span className="value" style={{ color: missing > 0 ? '#F59E0B' : '#10B981' }}>
                            {missing > 0 ? `⚠️ ${missing}` : '✅ None'}
                        </span>
                    </div>
                    <div className="column-tags">
                        {summary?.columns?.map(col => (
                            <span key={col} className="tag">{col}</span>
                        ))}
                    </div>
                </div>

                {/* Predictions Card */}
                <div className="card">
                    <div className="card-header">
                        <span className="card-icon">🤖</span>
                        <h3>Trend Predictions</h3>
                    </div>
                    {predEntries.length > 0 ? (
                        <ul className="prediction-list">
                            {predEntries.map(([col, pred]) => (
                                <li key={col} className="prediction-item">
                                    <span className="col-name">{col}</span>
                                    {typeof pred === 'object' ? (
                                        <div style={{ textAlign: 'right' }}>
                                            <div className={`trend-badge ${pred.trend}`}>
                                                {pred.trend === 'up' ? '↑' : '↓'}
                                                {pred.next_predicted.toFixed(2)}
                                            </div>
                                        </div>
                                    ) : (
                                        <span className="insufficient">{pred}</span>
                                    )}
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="insufficient" style={{ padding: '1rem 0' }}>
                            {predictions?.message || 'No numeric columns for prediction.'}
                        </p>
                    )}
                </div>
            </div>

            {/* ── Charts ── */}
            <div className="charts-section">
                <div className="section-title">
                    <span>📊 Generated Charts</span>
                    <span className="line" />
                    <span style={{ color: 'var(--text-3)', fontSize: '0.8rem', whiteSpace: 'nowrap' }}>
                        {charts?.length ?? 0} chart{charts?.length !== 1 ? 's' : ''}
                    </span>
                </div>
                <div className="charts-grid">
                    {charts && charts.length > 0 ? (
                        charts.map((chart, idx) => (
                            <div key={idx} className="chart-card">
                                <div className="chart-card-label">
                                    {CHART_LABELS[chart] ?? `Chart ${idx + 1}`}
                                </div>
                                <img
                                    src={`${BACKEND}/static/${chart}`}
                                    alt={CHART_LABELS[chart] ?? `Chart ${idx + 1}`}
                                    loading="lazy"
                                />
                            </div>
                        ))
                    ) : (
                        <div className="no-charts">
                            📭 No charts were generated for this dataset.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Charts;
