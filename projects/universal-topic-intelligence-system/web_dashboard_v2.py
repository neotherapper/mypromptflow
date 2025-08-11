#!/usr/bin/env python3
"""
Enhanced FastAPI Web Dashboard for Universal Topic Intelligence System
Features modern UI/UX design with improved usability and search functionality
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime, timedelta
import json
from pathlib import Path
import asyncio
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

# Import our system components
from agents.queen_agent import QueenAgent
from storage import StorageManager

app = FastAPI(title="Universal Topic Intelligence System v2")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models for API responses
class Stats(BaseModel):
    total_items: int
    priority_distribution: Dict[str, int]
    top_sources: List[Dict[str, Any]]
    items_24h: int
    english_percentage: float
    items_this_week: int

class ContentItemResponse(BaseModel):
    items: List[Dict[str, Any]]
    total: int
    page: int
    per_page: int
    total_pages: int
    filters_applied: Dict[str, Any]

class MonitoringResult(BaseModel):
    success: bool
    items_collected: int
    topics_monitored: List[str]
    error: Optional[str] = None

class SearchResult(BaseModel):
    items: List[Dict[str, Any]]
    total_matches: int
    search_query: str
    search_time_ms: int

# Database helper
def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('topic_intelligence.db')
    conn.row_factory = sqlite3.Row
    return conn

# Enhanced HTML Dashboard with Modern UI
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Topic Intelligence System</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        /* Modern CSS Reset and Variables */
        *, *::before, *::after {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            /* Color System */
            --primary-50: #f0f9ff;
            --primary-100: #e0f2fe;
            --primary-500: #0ea5e9;
            --primary-600: #0284c7;
            --primary-700: #0369a1;
            
            --gray-50: #f9fafb;
            --gray-100: #f3f4f6;
            --gray-200: #e5e7eb;
            --gray-300: #d1d5db;
            --gray-400: #9ca3af;
            --gray-500: #6b7280;
            --gray-600: #4b5563;
            --gray-700: #374151;
            --gray-800: #1f2937;
            --gray-900: #111827;
            
            --success-50: #f0fdf4;
            --success-500: #22c55e;
            --warning-50: #fffbeb;
            --warning-500: #f59e0b;
            --error-50: #fef2f2;
            --error-500: #ef4444;
            
            /* Typography */
            --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            --font-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
            
            /* Spacing */
            --space-1: 0.25rem;
            --space-2: 0.5rem;
            --space-3: 0.75rem;
            --space-4: 1rem;
            --space-5: 1.25rem;
            --space-6: 1.5rem;
            --space-8: 2rem;
            --space-12: 3rem;
            
            /* Shadows */
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
            
            /* Borders */
            --border-radius-sm: 0.375rem;
            --border-radius-md: 0.5rem;
            --border-radius-lg: 0.75rem;
            --border-radius-xl: 1rem;
        }
        
        body {
            font-family: var(--font-sans);
            background-color: var(--gray-50);
            color: var(--gray-900);
            line-height: 1.6;
        }
        
        /* Layout System */
        .app-container {
            display: flex;
            min-height: 100vh;
        }
        
        /* Sidebar Navigation */
        .sidebar {
            width: 280px;
            background: white;
            border-right: 1px solid var(--gray-200);
            display: flex;
            flex-direction: column;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            z-index: 10;
        }
        
        .sidebar-header {
            padding: var(--space-6);
            border-bottom: 1px solid var(--gray-200);
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-600);
            display: flex;
            align-items: center;
            gap: var(--space-3);
        }
        
        .logo i {
            font-size: 1.75rem;
        }
        
        .sidebar-nav {
            flex: 1;
            padding: var(--space-4);
        }
        
        .nav-section {
            margin-bottom: var(--space-6);
        }
        
        .nav-section-title {
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--gray-500);
            margin-bottom: var(--space-3);
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            gap: var(--space-3);
            padding: var(--space-3) var(--space-4);
            border-radius: var(--border-radius-md);
            cursor: pointer;
            transition: all 0.2s;
            margin-bottom: var(--space-1);
        }
        
        .nav-item:hover {
            background-color: var(--gray-100);
        }
        
        .nav-item.active {
            background-color: var(--primary-50);
            color: var(--primary-700);
            font-weight: 500;
        }
        
        .nav-item i {
            width: 20px;
            text-align: center;
        }
        
        /* Main Content Area */
        .main-content {
            flex: 1;
            margin-left: 280px;
            display: flex;
            flex-direction: column;
        }
        
        /* Header */
        .header {
            background: white;
            border-bottom: 1px solid var(--gray-200);
            padding: var(--space-4) var(--space-6);
            display: flex;
            align-items: center;
            gap: var(--space-4);
            position: sticky;
            top: 0;
            z-index: 5;
        }
        
        /* Search Bar */
        .search-container {
            flex: 1;
            max-width: 500px;
            position: relative;
        }
        
        .search-input {
            width: 100%;
            padding: var(--space-3) var(--space-4);
            padding-left: var(--space-12);
            border: 2px solid var(--gray-200);
            border-radius: var(--border-radius-lg);
            font-size: 1rem;
            transition: all 0.2s;
            background: var(--gray-50);
        }
        
        .search-input:focus {
            outline: none;
            border-color: var(--primary-500);
            background: white;
            box-shadow: 0 0 0 3px rgb(14 165 233 / 0.1);
        }
        
        .search-icon {
            position: absolute;
            left: var(--space-4);
            top: 50%;
            transform: translateY(-50%);
            color: var(--gray-400);
        }
        
        /* Action Buttons */
        .header-actions {
            display: flex;
            align-items: center;
            gap: var(--space-3);
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            gap: var(--space-2);
            padding: var(--space-3) var(--space-4);
            border-radius: var(--border-radius-md);
            font-size: 0.875rem;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.2s;
            cursor: pointer;
            border: none;
            white-space: nowrap;
        }
        
        .btn-primary {
            background-color: var(--primary-600);
            color: white;
        }
        
        .btn-primary:hover {
            background-color: var(--primary-700);
            box-shadow: var(--shadow-md);
        }
        
        .btn-secondary {
            background-color: white;
            color: var(--gray-700);
            border: 1px solid var(--gray-300);
        }
        
        .btn-secondary:hover {
            background-color: var(--gray-50);
        }
        
        /* Content Area */
        .content {
            flex: 1;
            padding: var(--space-6);
        }
        
        /* Stats Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: var(--space-6);
            margin-bottom: var(--space-8);
        }
        
        .stat-card {
            background: white;
            padding: var(--space-6);
            border-radius: var(--border-radius-lg);
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--gray-200);
            transition: all 0.2s;
        }
        
        .stat-card:hover {
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }
        
        .stat-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: var(--space-4);
        }
        
        .stat-title {
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--gray-600);
        }
        
        .stat-icon {
            width: 40px;
            height: 40px;
            border-radius: var(--border-radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
        }
        
        .stat-icon.blue {
            background: var(--primary-50);
            color: var(--primary-600);
        }
        
        .stat-icon.green {
            background: var(--success-50);
            color: var(--success-500);
        }
        
        .stat-icon.yellow {
            background: var(--warning-50);
            color: var(--warning-500);
        }
        
        .stat-icon.red {
            background: var(--error-50);
            color: var(--error-500);
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--gray-900);
            margin-bottom: var(--space-1);
        }
        
        .stat-change {
            font-size: 0.75rem;
            font-weight: 500;
        }
        
        .stat-change.positive {
            color: var(--success-500);
        }
        
        .stat-change.negative {
            color: var(--error-500);
        }
        
        /* Filter Panel */
        .filter-panel {
            background: white;
            padding: var(--space-6);
            border-radius: var(--border-radius-lg);
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--gray-200);
            margin-bottom: var(--space-6);
        }
        
        .filter-header {
            display: flex;
            align-items: center;
            justify-content: between;
            margin-bottom: var(--space-4);
        }
        
        .filter-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--gray-900);
            display: flex;
            align-items: center;
            gap: var(--space-2);
        }
        
        .filter-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: var(--space-4);
        }
        
        .filter-group {
            display: flex;
            flex-direction: column;
            gap: var(--space-2);
        }
        
        .filter-label {
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--gray-700);
        }
        
        .filter-select, .filter-input {
            padding: var(--space-3) var(--space-4);
            border: 2px solid var(--gray-200);
            border-radius: var(--border-radius-md);
            font-size: 0.875rem;
            transition: all 0.2s;
        }
        
        .filter-select:focus, .filter-input:focus {
            outline: none;
            border-color: var(--primary-500);
            box-shadow: 0 0 0 3px rgb(14 165 233 / 0.1);
        }
        
        /* Active Filters */
        .active-filters {
            display: flex;
            flex-wrap: wrap;
            gap: var(--space-2);
            margin-top: var(--space-4);
        }
        
        .filter-tag {
            display: inline-flex;
            align-items: center;
            gap: var(--space-2);
            padding: var(--space-1) var(--space-3);
            background: var(--primary-50);
            color: var(--primary-700);
            border-radius: var(--border-radius-md);
            font-size: 0.75rem;
            font-weight: 500;
        }
        
        .filter-tag button {
            background: none;
            border: none;
            color: var(--primary-600);
            cursor: pointer;
            padding: 0;
            margin-left: var(--space-1);
        }
        
        /* Content List */
        .content-section {
            background: white;
            border-radius: var(--border-radius-lg);
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--gray-200);
        }
        
        .content-header {
            padding: var(--space-6);
            border-bottom: 1px solid var(--gray-200);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .content-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--gray-900);
        }
        
        .content-list {
            divide-y divide-gray-200;
        }
        
        .content-item {
            padding: var(--space-6);
            transition: all 0.2s;
            border-bottom: 1px solid var(--gray-100);
        }
        
        .content-item:hover {
            background-color: var(--gray-50);
        }
        
        .content-item:last-child {
            border-bottom: none;
        }
        
        .item-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: var(--space-3);
        }
        
        .item-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--gray-900);
            line-height: 1.5;
            margin-bottom: var(--space-2);
        }
        
        .item-title a {
            color: inherit;
            text-decoration: none;
            transition: color 0.2s;
        }
        
        .item-title a:hover {
            color: var(--primary-600);
        }
        
        .item-meta {
            display: flex;
            align-items: center;
            gap: var(--space-4);
            flex-wrap: wrap;
            font-size: 0.875rem;
            color: var(--gray-500);
        }
        
        .item-meta-item {
            display: flex;
            align-items: center;
            gap: var(--space-1);
        }
        
        .priority-badge {
            display: inline-flex;
            align-items: center;
            padding: var(--space-1) var(--space-2);
            border-radius: var(--border-radius-sm);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .priority-critical {
            background: var(--error-50);
            color: var(--error-700);
        }
        
        .priority-high {
            background: var(--warning-50);
            color: var(--warning-700);
        }
        
        .priority-medium {
            background: var(--primary-50);
            color: var(--primary-700);
        }
        
        .priority-low {
            background: var(--gray-100);
            color: var(--gray-600);
        }
        
        .topic-tags {
            display: flex;
            flex-wrap: wrap;
            gap: var(--space-2);
            margin-top: var(--space-3);
        }
        
        .topic-tag {
            padding: var(--space-1) var(--space-2);
            background: var(--gray-100);
            color: var(--gray-700);
            border-radius: var(--border-radius-sm);
            font-size: 0.75rem;
            font-weight: 500;
        }
        
        /* Loading States */
        .loading {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: var(--space-12);
            color: var(--gray-500);
        }
        
        .spinner {
            width: 24px;
            height: 24px;
            border: 3px solid var(--gray-200);
            border-top: 3px solid var(--primary-500);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: var(--space-3);
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: var(--space-12);
            color: var(--gray-500);
        }
        
        .empty-state i {
            font-size: 3rem;
            margin-bottom: var(--space-4);
            color: var(--gray-300);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .sidebar {
                transform: translateX(-100%);
                transition: transform 0.3s;
            }
            
            .sidebar.open {
                transform: translateX(0);
            }
            
            .main-content {
                margin-left: 0;
            }
            
            .header {
                padding: var(--space-4);
            }
            
            .search-container {
                max-width: none;
            }
            
            .content {
                padding: var(--space-4);
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
                gap: var(--space-4);
            }
            
            .filter-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Accessibility */
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }
        
        /* Focus styles */
        *:focus {
            outline: 2px solid var(--primary-500);
            outline-offset: 2px;
        }
        
        .btn:focus, .nav-item:focus {
            outline-offset: -2px;
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Sidebar Navigation -->
        <aside class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <div class="logo">
                    <i class="fas fa-brain"></i>
                    <span>Intelligence Hub</span>
                </div>
            </div>
            
            <nav class="sidebar-nav">
                <div class="nav-section">
                    <div class="nav-section-title">Overview</div>
                    <div class="nav-item active" data-view="dashboard">
                        <i class="fas fa-chart-line"></i>
                        <span>Dashboard</span>
                    </div>
                    <div class="nav-item" data-view="search">
                        <i class="fas fa-search"></i>
                        <span>Search</span>
                    </div>
                </div>
                
                <div class="nav-section">
                    <div class="nav-section-title">Content</div>
                    <div class="nav-item" data-view="all-content">
                        <i class="fas fa-list"></i>
                        <span>All Items</span>
                    </div>
                    <div class="nav-item" data-view="high-priority">
                        <i class="fas fa-exclamation-triangle"></i>
                        <span>High Priority</span>
                    </div>
                    <div class="nav-item" data-view="recent">
                        <i class="fas fa-clock"></i>
                        <span>Recent</span>
                    </div>
                </div>
                
                <div class="nav-section">
                    <div class="nav-section-title">Topics</div>
                    <div class="nav-item" data-topic="claude-ai">
                        <i class="fas fa-robot"></i>
                        <span>Claude AI</span>
                    </div>
                    <div class="nav-item" data-topic="react">
                        <i class="fab fa-react"></i>
                        <span>React</span>
                    </div>
                    <div class="nav-item" data-topic="typescript">
                        <i class="fas fa-code"></i>
                        <span>TypeScript</span>
                    </div>
                    <div class="nav-item" data-topic="mcp">
                        <i class="fas fa-plug"></i>
                        <span>MCP Servers</span>
                    </div>
                </div>
                
                <div class="nav-section">
                    <div class="nav-section-title">System</div>
                    <div class="nav-item" data-view="monitoring">
                        <i class="fas fa-cog"></i>
                        <span>Monitoring</span>
                    </div>
                </div>
            </nav>
        </aside>
        
        <!-- Main Content -->
        <main class="main-content">
            <!-- Header -->
            <header class="header">
                <div class="search-container">
                    <div class="search-icon">
                        <i class="fas fa-search"></i>
                    </div>
                    <input 
                        type="text" 
                        class="search-input" 
                        id="globalSearch"
                        placeholder="Search across all intelligence..."
                        autocomplete="off"
                    >
                </div>
                
                <div class="header-actions">
                    <button class="btn btn-secondary" id="refreshBtn">
                        <i class="fas fa-sync-alt"></i>
                        <span>Refresh</span>
                    </button>
                    <button class="btn btn-primary" id="monitorBtn">
                        <i class="fas fa-play"></i>
                        <span>Run Monitoring</span>
                    </button>
                </div>
            </header>
            
            <!-- Content Area -->
            <div class="content" id="mainContent">
                <!-- Dashboard View (Default) -->
                <div id="dashboardView">
                    <!-- Stats Grid -->
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-header">
                                <div class="stat-title">Total Items</div>
                                <div class="stat-icon blue">
                                    <i class="fas fa-database"></i>
                                </div>
                            </div>
                            <div class="stat-value" id="totalItems">-</div>
                            <div class="stat-change positive" id="totalItemsChange">+0 this week</div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-header">
                                <div class="stat-title">English Content</div>
                                <div class="stat-icon green">
                                    <i class="fas fa-language"></i>
                                </div>
                            </div>
                            <div class="stat-value" id="englishPercentage">-%</div>
                            <div class="stat-change positive" id="englishChange">Filtered quality</div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-header">
                                <div class="stat-title">High Priority</div>
                                <div class="stat-icon yellow">
                                    <i class="fas fa-exclamation-triangle"></i>
                                </div>
                            </div>
                            <div class="stat-value" id="highPriority">-</div>
                            <div class="stat-change" id="priorityChange">Requires attention</div>
                        </div>
                        
                        <div class="stat-card">
                            <div class="stat-header">
                                <div class="stat-title">Last 24 Hours</div>
                                <div class="stat-icon blue">
                                    <i class="fas fa-clock"></i>
                                </div>
                            </div>
                            <div class="stat-value" id="items24h">-</div>
                            <div class="stat-change" id="recentChange">Recent activity</div>
                        </div>
                    </div>
                    
                    <!-- Filter Panel -->
                    <div class="filter-panel">
                        <div class="filter-header">
                            <div class="filter-title">
                                <i class="fas fa-filter"></i>
                                Content Filters
                            </div>
                        </div>
                        
                        <div class="filter-grid">
                            <div class="filter-group">
                                <label class="filter-label">Topic</label>
                                <select class="filter-select" id="topicFilter">
                                    <option value="">All Topics</option>
                                    <option value="claude-ai">Claude AI</option>
                                    <option value="react">React</option>
                                    <option value="typescript">TypeScript</option>
                                    <option value="mcp">MCP Servers</option>
                                    <option value="ai">AI Applications</option>
                                </select>
                            </div>
                            
                            <div class="filter-group">
                                <label class="filter-label">Priority</label>
                                <select class="filter-select" id="priorityFilter">
                                    <option value="">All Priorities</option>
                                    <option value="critical">Critical Only</option>
                                    <option value="high">High Priority</option>
                                    <option value="medium">Medium Priority</option>
                                    <option value="low">Low Priority</option>
                                </select>
                            </div>
                            
                            <div class="filter-group">
                                <label class="filter-label">Source</label>
                                <select class="filter-select" id="sourceFilter">
                                    <option value="">All Sources</option>
                                </select>
                            </div>
                            
                            <div class="filter-group">
                                <label class="filter-label">Time Range</label>
                                <select class="filter-select" id="timeFilter">
                                    <option value="">All Time</option>
                                    <option value="today">Today</option>
                                    <option value="week">This Week</option>
                                    <option value="month">This Month</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="active-filters" id="activeFilters"></div>
                    </div>
                    
                    <!-- Content List -->
                    <div class="content-section">
                        <div class="content-header">
                            <div class="content-title" id="contentTitle">Latest Intelligence Feed</div>
                            <div class="header-actions">
                                <button class="btn btn-secondary" id="viewToggle">
                                    <i class="fas fa-th-list"></i>
                                    <span>List View</span>
                                </button>
                            </div>
                        </div>
                        
                        <div class="content-list" id="contentList">
                            <div class="loading">
                                <div class="spinner"></div>
                                Loading intelligence...
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
    
    <script>
        // Application State
        const state = {
            currentView: 'dashboard',
            currentFilters: {},
            currentPage: 1,
            searchQuery: '',
            isLoading: false
        };
        
        // API Base URL
        const API_BASE = window.location.origin;
        
        // Initialize Application
        document.addEventListener('DOMContentLoaded', function() {
            initializeApp();
        });
        
        function initializeApp() {
            setupEventListeners();
            loadDashboardData();
        }
        
        function setupEventListeners() {
            // Navigation
            document.querySelectorAll('.nav-item').forEach(item => {
                item.addEventListener('click', handleNavigation);
            });
            
            // Search
            const searchInput = document.getElementById('globalSearch');
            searchInput.addEventListener('input', debounce(handleGlobalSearch, 300));
            searchInput.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    handleGlobalSearch();
                }
            });
            
            // Filters
            document.querySelectorAll('.filter-select').forEach(select => {
                select.addEventListener('change', handleFilterChange);
            });
            
            // Action buttons
            document.getElementById('refreshBtn').addEventListener('click', refreshData);
            document.getElementById('monitorBtn').addEventListener('click', triggerMonitoring);
        }
        
        function handleNavigation(e) {
            const item = e.currentTarget;
            const view = item.dataset.view;
            const topic = item.dataset.topic;
            
            // Update active navigation
            document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            if (view) {
                state.currentView = view;
                loadViewContent(view);
            } else if (topic) {
                state.currentView = 'topic';
                state.currentFilters = { topic };
                loadFilteredContent();
            }
        }
        
        async function loadDashboardData() {
            try {
                await Promise.all([
                    loadStats(),
                    loadContent(),
                    loadSources()
                ]);
            } catch (error) {
                console.error('Error loading dashboard data:', error);
            }
        }
        
        async function loadStats() {
            try {
                const response = await fetch(`${API_BASE}/api/stats`);
                const data = await response.json();
                
                updateStatsDisplay(data);
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        function updateStatsDisplay(data) {
            document.getElementById('totalItems').textContent = data.total_items.toLocaleString();
            document.getElementById('englishPercentage').textContent = `${data.english_percentage.toFixed(1)}%`;
            document.getElementById('items24h').textContent = data.items_24h.toLocaleString();
            
            const highPriority = (data.priority_distribution.critical || 0) + 
                               (data.priority_distribution.high || 0);
            document.getElementById('highPriority').textContent = highPriority.toLocaleString();
            
            // Update change indicators
            document.getElementById('totalItemsChange').textContent = `+${data.items_this_week || 0} this week`;
            document.getElementById('englishChange').textContent = 'Language filtered';
            document.getElementById('priorityChange').textContent = highPriority > 0 ? 'Requires attention' : 'All clear';
            document.getElementById('recentChange').textContent = data.items_24h > 0 ? 'Active monitoring' : 'Quiet period';
        }
        
        async function loadContent(filters = {}, page = 1) {
            if (state.isLoading) return;
            
            state.isLoading = true;
            showContentLoading();
            
            try {
                const params = new URLSearchParams({
                    page: page,
                    per_page: 20,
                    ...filters
                });
                
                const response = await fetch(`${API_BASE}/api/items?${params}`);
                const data = await response.json();
                
                displayContent(data);
                updateContentTitle(data, filters);
                
            } catch (error) {
                console.error('Error loading content:', error);
                showContentError(error);
            } finally {
                state.isLoading = false;
            }
        }
        
        function displayContent(data) {
            const contentList = document.getElementById('contentList');
            
            if (data.items.length === 0) {
                contentList.innerHTML = `
                    <div class="empty-state">
                        <i class="fas fa-inbox"></i>
                        <h3>No content found</h3>
                        <p>Try adjusting your filters or search terms</p>
                    </div>
                `;
                return;
            }
            
            const itemsHtml = data.items.map(item => {
                const publishedDate = item.published_date ? 
                    new Date(item.published_date).toLocaleDateString() : 
                    'Unknown date';
                    
                const topics = Array.isArray(item.topics) ? item.topics : 
                    (item.topics ? JSON.parse(item.topics) : []);
                    
                const score = ((item.priority_score || 0) * 100).toFixed(0);
                
                return `
                    <div class="content-item">
                        <div class="item-header">
                            <div>
                                <div class="item-title">
                                    ${item.url ? `<a href="${item.url}" target="_blank">${item.title}</a>` : item.title}
                                </div>
                                <div class="item-meta">
                                    <div class="item-meta-item">
                                        <span class="priority-badge priority-${item.priority_level}">${item.priority_level}</span>
                                    </div>
                                    <div class="item-meta-item">
                                        <i class="fas fa-calendar"></i>
                                        <span>${publishedDate}</span>
                                    </div>
                                    <div class="item-meta-item">
                                        <i class="fas fa-rss"></i>
                                        <span>${item.source_id}</span>
                                    </div>
                                    <div class="item-meta-item">
                                        <i class="fas fa-star"></i>
                                        <span>Score: ${score}%</span>
                                    </div>
                                    <div class="item-meta-item">
                                        <i class="fas fa-language"></i>
                                        <span>${item.detected_language || 'en'}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        ${topics.length > 0 ? `
                            <div class="topic-tags">
                                ${topics.map(topic => `<span class="topic-tag">${topic}</span>`).join('')}
                            </div>
                        ` : ''}
                    </div>
                `;
            }).join('');
            
            contentList.innerHTML = itemsHtml;
        }
        
        function showContentLoading() {
            document.getElementById('contentList').innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    Loading content...
                </div>
            `;
        }
        
        function showContentError(error) {
            document.getElementById('contentList').innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h3>Error loading content</h3>
                    <p>${error.message || 'Please try again'}</p>
                </div>
            `;
        }
        
        function updateContentTitle(data, filters) {
            let title = 'Latest Intelligence Feed';
            
            if (filters.topic) {
                title = `${filters.topic.toUpperCase()} Intelligence`;
            } else if (filters.priority) {
                title = `${filters.priority.toUpperCase()} Priority Items`;
            } else if (state.searchQuery) {
                title = `Search Results: "${state.searchQuery}"`;
            }
            
            title += ` (${data.total.toLocaleString()} items)`;
            document.getElementById('contentTitle').textContent = title;
        }
        
        async function loadSources() {
            try {
                // Get unique sources from the content to populate source filter
                const response = await fetch(`${API_BASE}/api/items?per_page=1000`);
                const data = await response.json();
                
                const sources = [...new Set(data.items.map(item => item.source_id))].sort();
                const sourceFilter = document.getElementById('sourceFilter');
                
                sources.forEach(source => {
                    const option = document.createElement('option');
                    option.value = source;
                    option.textContent = source.replace(/_/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase());
                    sourceFilter.appendChild(option);
                });
                
            } catch (error) {
                console.error('Error loading sources:', error);
            }
        }
        
        function handleFilterChange(e) {
            const filterType = e.target.id.replace('Filter', '');
            const value = e.target.value;
            
            if (value) {
                state.currentFilters[filterType] = value;
            } else {
                delete state.currentFilters[filterType];
            }
            
            updateActiveFilters();
            loadContent(state.currentFilters, 1);
        }
        
        function updateActiveFilters() {
            const activeFiltersContainer = document.getElementById('activeFilters');
            const filters = Object.entries(state.currentFilters);
            
            if (filters.length === 0) {
                activeFiltersContainer.innerHTML = '';
                return;
            }
            
            const filtersHtml = filters.map(([key, value]) => `
                <div class="filter-tag">
                    <span>${key}: ${value}</span>
                    <button onclick="removeFilter('${key}')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `).join('');
            
            activeFiltersContainer.innerHTML = filtersHtml;
        }
        
        function removeFilter(filterKey) {
            delete state.currentFilters[filterKey];
            
            // Update the corresponding select element
            const selectElement = document.getElementById(filterKey + 'Filter');
            if (selectElement) {
                selectElement.value = '';
            }
            
            updateActiveFilters();
            loadContent(state.currentFilters, 1);
        }
        
        async function handleGlobalSearch() {
            const query = document.getElementById('globalSearch').value.trim();
            
            if (!query) {
                // If search is cleared, reload normal content
                state.searchQuery = '';
                loadContent(state.currentFilters, 1);
                return;
            }
            
            state.searchQuery = query;
            
            try {
                const response = await fetch(`${API_BASE}/api/search?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                
                displayContent(data);
                updateContentTitle(data, { search: query });
                
            } catch (error) {
                console.error('Error performing search:', error);
                showContentError(error);
            }
        }
        
        async function refreshData() {
            const refreshBtn = document.getElementById('refreshBtn');
            const icon = refreshBtn.querySelector('i');
            
            // Show loading state
            icon.classList.add('fa-spin');
            refreshBtn.disabled = true;
            
            try {
                await loadDashboardData();
            } finally {
                // Reset button state
                icon.classList.remove('fa-spin');
                refreshBtn.disabled = false;
            }
        }
        
        async function triggerMonitoring() {
            const monitorBtn = document.getElementById('monitorBtn');
            const icon = monitorBtn.querySelector('i');
            const text = monitorBtn.querySelector('span');
            
            // Show loading state
            icon.className = 'fas fa-spinner fa-spin';
            text.textContent = 'Monitoring...';
            monitorBtn.disabled = true;
            
            try {
                const response = await fetch(`${API_BASE}/api/monitor/claude-ai`, {
                    method: 'POST'
                });
                const result = await response.json();
                
                if (result.success) {
                    // Show success notification
                    showNotification(`✅ Monitoring complete! Collected ${result.items_collected} new items`, 'success');
                    
                    // Refresh the data
                    setTimeout(() => loadDashboardData(), 1000);
                } else {
                    showNotification(`❌ Monitoring failed: ${result.error}`, 'error');
                }
                
            } catch (error) {
                showNotification(`❌ Error: ${error.message}`, 'error');
            } finally {
                // Reset button state
                icon.className = 'fas fa-play';
                text.textContent = 'Run Monitoring';
                monitorBtn.disabled = false;
            }
        }
        
        function showNotification(message, type = 'info') {
            // Create notification element
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 16px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                z-index: 1000;
                max-width: 400px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                animation: slideIn 0.3s ease-out;
                background: ${type === 'success' ? '#059669' : type === 'error' ? '#DC2626' : '#0EA5E9'};
            `;
            notification.textContent = message;
            
            document.body.appendChild(notification);
            
            // Auto remove after 5 seconds
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease-in';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }, 5000);
        }
        
        // Add CSS animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
        
        // Utility function for debouncing
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the enhanced dashboard"""
    return DASHBOARD_HTML

@app.get("/api/stats", response_model=Stats)
async def get_stats():
    """Get enhanced system statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Total items
        cursor.execute("SELECT COUNT(*) as count FROM content_items")
        total_items = cursor.fetchone()['count']
        
        # Items by priority
        cursor.execute("""
            SELECT priority_level, COUNT(*) as count 
            FROM content_items 
            GROUP BY priority_level
        """)
        priority_dist = {row['priority_level']: row['count'] for row in cursor.fetchall()}
        
        # Top sources
        cursor.execute("""
            SELECT source_id, COUNT(*) as count 
            FROM content_items 
            GROUP BY source_id 
            ORDER BY count DESC 
            LIMIT 5
        """)
        top_sources = [{'source': row['source_id'], 'count': row['count']} for row in cursor.fetchall()]
        
        # Recent activity (last 24 hours)
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM content_items 
            WHERE collected_date > datetime('now', '-24 hours')
        """)
        recent_count = cursor.fetchone()['count']
        
        # Weekly activity
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM content_items 
            WHERE collected_date > datetime('now', '-7 days')
        """)
        weekly_count = cursor.fetchone()['count']
        
        # Language statistics
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN is_english = 1 THEN 1 ELSE 0 END) as english_items,
                COUNT(*) as total_items
            FROM content_items 
            WHERE detected_language IS NOT NULL
        """)
        lang_stats = cursor.fetchone()
        english_percentage = (lang_stats['english_items'] / lang_stats['total_items'] * 100) if lang_stats['total_items'] > 0 else 0
        
        return Stats(
            total_items=total_items,
            priority_distribution=priority_dist,
            top_sources=top_sources,
            items_24h=recent_count,
            english_percentage=english_percentage,
            items_this_week=weekly_count
        )
    finally:
        conn.close()

@app.get("/api/items", response_model=ContentItemResponse)
async def get_items(
    page: int = 1,
    per_page: int = 20,
    topic: str = "",
    priority: str = "",
    source: str = "",
    time_range: str = ""
):
    """Get content items with enhanced filtering"""
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Build query with enhanced filters
        query = "SELECT * FROM content_items WHERE 1=1"
        params = []
        
        if topic:
            query += " AND topics LIKE ?"
            params.append(f'%"{topic}"%')
        
        if priority:
            query += " AND priority_level = ?"
            params.append(priority)
            
        if source:
            query += " AND source_id = ?"
            params.append(source)
            
        if time_range:
            if time_range == "today":
                query += " AND collected_date > datetime('now', '-1 day')"
            elif time_range == "week":
                query += " AND collected_date > datetime('now', '-7 days')"
            elif time_range == "month":
                query += " AND collected_date > datetime('now', '-30 days')"
        
        # Get total count
        count_query = query.replace("*", "COUNT(*) as count")
        cursor.execute(count_query, params)
        total = cursor.fetchone()['count']
        
        # Get items
        query += " ORDER BY collected_date DESC LIMIT ? OFFSET ?"
        params.extend([per_page, offset])
        
        cursor.execute(query, params)
        items = []
        for row in cursor.fetchall():
            item = dict(row)
            # Parse JSON fields
            item['topics'] = json.loads(item['topics']) if item['topics'] else []
            item['metadata'] = json.loads(item['metadata']) if item['metadata'] else {}
            items.append(item)
        
        return ContentItemResponse(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=(total + per_page - 1) // per_page,
            filters_applied={
                "topic": topic,
                "priority": priority,
                "source": source,
                "time_range": time_range
            }
        )
    finally:
        conn.close()

@app.get("/api/search", response_model=SearchResult)
async def search_content(q: str = Query(..., min_length=2)):
    """Search across all content with full-text search"""
    start_time = datetime.now()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Full-text search across title and content
        query = """
            SELECT *, 
                   CASE 
                       WHEN title LIKE ? THEN 10
                       WHEN content LIKE ? THEN 5
                       ELSE 1
                   END as relevance_score
            FROM content_items 
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY relevance_score DESC, collected_date DESC
            LIMIT 100
        """
        
        search_pattern = f"%{q}%"
        cursor.execute(query, [search_pattern] * 4)
        
        items = []
        for row in cursor.fetchall():
            item = dict(row)
            # Parse JSON fields
            item['topics'] = json.loads(item['topics']) if item['topics'] else []
            item['metadata'] = json.loads(item['metadata']) if item['metadata'] else {}
            # Remove relevance_score from response
            item.pop('relevance_score', None)
            items.append(item)
        
        search_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return SearchResult(
            items=items,
            total_matches=len(items),
            search_query=q,
            search_time_ms=search_time_ms
        )
        
    finally:
        conn.close()

@app.get("/api/topics")
async def get_topics():
    """Get monitored topics with enhanced statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT topic_slug, topic_name, priority_level, 
                   items_collected, last_monitored
            FROM topics
            ORDER BY items_collected DESC
        """)
        
        topics = []
        for row in cursor.fetchall():
            topic = dict(row)
            topics.append(topic)
        
        return topics
    finally:
        conn.close()

@app.post("/api/monitor/{topic}", response_model=MonitoringResult)
async def monitor_topic(topic: str):
    """Trigger monitoring for a specific topic with language filtering"""
    try:
        # Run async monitoring
        queen = QueenAgent()
        result = await queen.orchestrate(force_topics=[topic])
        
        return MonitoringResult(
            success=True,
            items_collected=result.total_items_collected,
            topics_monitored=result.topics_monitored
        )
    except Exception as e:
        return MonitoringResult(
            success=False,
            items_collected=0,
            topics_monitored=[],
            error=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting Universal Topic Intelligence System Dashboard v2")
    print("🎨 Enhanced UI/UX with modern design and improved usability")
    print("🌐 Language filtering enabled - English content only")
    print("📍 Open your browser to: http://localhost:5001")
    print("Press Ctrl+C to stop the server\n")
    uvicorn.run(app, host="0.0.0.0", port=5001)