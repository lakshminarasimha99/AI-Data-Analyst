import React, { useState, useRef } from 'react';
import axios from 'axios';

function Upload({ onUploadSuccess }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [dragOver, setDragOver] = useState(false);
    const inputRef = useRef(null);

    const selectFile = (f) => {
        if (f && f.name.endsWith('.csv')) {
            setFile(f);
            setError(null);
        } else if (f) {
            setError('Only .csv files are supported.');
        }
    };

    const handleFileChange = (e) => {
        if (e.target.files.length > 0) selectFile(e.target.files[0]);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setDragOver(false);
        const dropped = e.dataTransfer.files[0];
        selectFile(dropped);
    };

    const handleDragOver = (e) => { e.preventDefault(); setDragOver(true); };
    const handleDragLeave = () => setDragOver(false);

    const uploadFile = async () => {
        if (!file) { setError('Please select a file first.'); return; }
        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await axios.post('http://127.0.0.1:8000/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            onUploadSuccess(res.data);
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || 'Upload failed. Is the backend running?');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-container">
            <div
                className={`upload-card ${dragOver ? 'drag-over' : ''}`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onClick={() => !loading && inputRef.current?.click()}
            >
                <div className="upload-icon-wrap">
                    {loading ? '⏳' : dragOver ? '📂' : '📊'}
                </div>

                <h2>{loading ? 'Analyzing your data…' : 'Upload Dataset'}</h2>
                <p>
                    {loading
                        ? 'Running ML models & generating charts'
                        : 'Drag & drop a CSV file here, or click to browse'}
                </p>

                {/* File chip */}
                {file && !loading && (
                    <div className="file-chip">
                        <span>📄</span>
                        {file.name}
                        <span style={{ color: 'rgba(255,255,255,0.4)', cursor: 'pointer' }}
                            onClick={(e) => { e.stopPropagation(); setFile(null); }}>
                            ✕
                        </span>
                    </div>
                )}

                <input
                    ref={inputRef}
                    type="file"
                    id="file-upload"
                    accept=".csv"
                    onChange={handleFileChange}
                    className="file-input"
                    onClick={(e) => e.stopPropagation()}
                />

                {!file && !loading && (
                    <label
                        htmlFor="file-upload"
                        className="file-label"
                        onClick={(e) => e.stopPropagation()}
                    >
                        📁 Choose CSV File
                    </label>
                )}

                {error && (
                    <div className="error-message">
                        <span>⚠️</span> {error}
                    </div>
                )}

                <button
                    className="upload-button"
                    onClick={(e) => { e.stopPropagation(); uploadFile(); }}
                    disabled={!file || loading}
                >
                    {loading ? (
                        <><span className="spinner" /> Analyzing...</>
                    ) : (
                        '🚀 Analyze Data'
                    )}
                </button>

                {loading && (
                    <div className="progress-bar-wrap">
                        <div className="progress-bar-fill" />
                    </div>
                )}

                {!loading && (
                    <p className="upload-hint">Supports CSV files · Max recommended 50 MB</p>
                )}
            </div>
        </div>
    );
}

export default Upload;
