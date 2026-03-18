import React, { useState } from 'react';
import Upload from './Upload';
import Charts from './Charts';
import './index.css';

function App() {
    const [data, setData] = useState(null);

    return (
        <div className="app-container">
            <header className="app-header">
                <div className="header-badge">
                    <span className="dot" />
                    Powered by FastAPI · Pandas · Scikit-Learn
                </div>
                <h1>AI Data Analyst</h1>
                <p>
                    Upload any CSV dataset and instantly get AI-generated charts,
                    statistical insights, trend predictions, and a downloadable PDF report.
                </p>
            </header>

            <main className="app-main">
                {!data ? (
                    <Upload onUploadSuccess={(res) => setData(res)} />
                ) : (
                    <Charts data={data} onReset={() => setData(null)} />
                )}
            </main>
        </div>
    );
}

export default App;
