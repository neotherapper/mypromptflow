/**
 * Universal Time Formatter - YouTube-style relative time display
 * Provides intelligent time formatting for all intelligence system templates
 */

class TimeFormatter {
    constructor() {
        this.now = new Date();
        this.intervals = {
            year: 365 * 24 * 60 * 60 * 1000,
            month: 30 * 24 * 60 * 60 * 1000,
            week: 7 * 24 * 60 * 60 * 1000,
            day: 24 * 60 * 60 * 1000,
            hour: 60 * 60 * 1000,
            minute: 60 * 1000,
            second: 1000
        };
    }

    /**
     * Format timestamp to YouTube-style relative time
     * @param {string|Date} timestamp - ISO timestamp or Date object
     * @returns {string} - Formatted relative time (e.g., "1h 15m ago", "2d ago", "1y 8mo ago")
     */
    formatRelativeTime(timestamp) {
        if (!timestamp || timestamp === 'never' || timestamp === 'error' || timestamp === 'unknown') {
            return timestamp || 'unknown';
        }

        try {
            const date = new Date(timestamp);
            const now = new Date();
            const diff = now.getTime() - date.getTime();

            // Future dates
            if (diff < 0) {
                return 'in the future';
            }

            // Just now (less than 30 seconds)
            if (diff < 30 * 1000) {
                return 'just now';
            }

            // Seconds (30s - 1min)
            if (diff < this.intervals.minute) {
                const seconds = Math.floor(diff / 1000);
                return `${seconds}s ago`;
            }

            // Minutes (1min - 1hour)
            if (diff < this.intervals.hour) {
                const minutes = Math.floor(diff / this.intervals.minute);
                return `${minutes}m ago`;
            }

            // Hours with minutes (1hour - 24hours)
            if (diff < this.intervals.day) {
                const hours = Math.floor(diff / this.intervals.hour);
                const remainingMs = diff - (hours * this.intervals.hour);
                const minutes = Math.floor(remainingMs / this.intervals.minute);
                
                if (hours === 1 && minutes > 0) {
                    return `1h ${minutes}m ago`;
                } else if (hours < 6 && minutes > 0) {
                    return `${hours}h ${minutes}m ago`;
                } else {
                    return `${hours}h ago`;
                }
            }

            // Days (1day - 7days)
            if (diff < this.intervals.week) {
                const days = Math.floor(diff / this.intervals.day);
                return `${days}d ago`;
            }

            // Weeks (1week - 30days)
            if (diff < this.intervals.month) {
                const weeks = Math.floor(diff / this.intervals.week);
                if (weeks === 1) {
                    return '1w ago';
                }
                return `${weeks}w ago`;
            }

            // Months with days (1month - 12months)
            if (diff < this.intervals.year) {
                const months = Math.floor(diff / this.intervals.month);
                const remainingMs = diff - (months * this.intervals.month);
                const days = Math.floor(remainingMs / this.intervals.day);
                
                if (months === 1 && days >= 7) {
                    const weeks = Math.floor(days / 7);
                    return `1mo ${weeks}w ago`;
                } else if (months < 6 && days >= 7) {
                    const weeks = Math.floor(days / 7);
                    return `${months}mo ${weeks}w ago`;
                } else {
                    return `${months}mo ago`;
                }
            }

            // Years with months
            const years = Math.floor(diff / this.intervals.year);
            const remainingMs = diff - (years * this.intervals.year);
            const months = Math.floor(remainingMs / this.intervals.month);
            
            if (years === 1 && months > 0) {
                return `1y ${months}mo ago`;
            } else if (years < 5 && months > 0) {
                return `${years}y ${months}mo ago`;
            } else {
                return `${years}y ago`;
            }

        } catch (error) {
            console.warn('Time formatting error:', error);
            return 'unknown';
        }
    }

    /**
     * Format timestamp for display in headers and titles
     * @param {string|Date} timestamp - ISO timestamp or Date object
     * @returns {string} - Human-readable date and time
     */
    formatDisplayTime(timestamp) {
        if (!timestamp || timestamp === 'never' || timestamp === 'error' || timestamp === 'unknown') {
            return timestamp || 'unknown';
        }

        try {
            const date = new Date(timestamp);
            const options = {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                timeZoneName: 'short'
            };
            return date.toLocaleDateString('en-US', options);
        } catch (error) {
            console.warn('Display time formatting error:', error);
            return 'unknown';
        }
    }

    /**
     * Format timestamp for metric displays
     * @param {string|Date} timestamp - ISO timestamp or Date object
     * @returns {string} - Concise time format for metrics
     */
    formatMetricTime(timestamp) {
        if (!timestamp || timestamp === 'never' || timestamp === 'error' || timestamp === 'unknown') {
            return timestamp || 'unknown';
        }

        try {
            const date = new Date(timestamp);
            const now = new Date();
            const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
            const yesterday = new Date(today.getTime() - 24 * 60 * 60 * 1000);
            const dateOnly = new Date(date.getFullYear(), date.getMonth(), date.getDate());

            if (dateOnly.getTime() === today.getTime()) {
                return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
            } else if (dateOnly.getTime() === yesterday.getTime()) {
                return 'Yesterday';
            } else {
                return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            }
        } catch (error) {
            console.warn('Metric time formatting error:', error);
            return 'unknown';
        }
    }

    /**
     * Auto-update all timestamps on the page
     * Call this method to refresh all time displays
     */
    updateAllTimestamps() {
        // Update relative time elements
        document.querySelectorAll('[data-timestamp]').forEach(element => {
            const timestamp = element.getAttribute('data-timestamp');
            const format = element.getAttribute('data-format') || 'relative';
            
            switch (format) {
                case 'relative':
                    element.textContent = this.formatRelativeTime(timestamp);
                    break;
                case 'display':
                    element.textContent = this.formatDisplayTime(timestamp);
                    break;
                case 'metric':
                    element.textContent = this.formatMetricTime(timestamp);
                    break;
            }
        });

        // Update content age elements
        document.querySelectorAll('.content-age').forEach(element => {
            const timestamp = element.getAttribute('data-timestamp');
            if (timestamp) {
                element.textContent = this.formatRelativeTime(timestamp);
            }
        });

        // Update metric values
        document.querySelectorAll('.metric-value[data-timestamp]').forEach(element => {
            const timestamp = element.getAttribute('data-timestamp');
            element.textContent = this.formatMetricTime(timestamp);
        });

        // Update last updated footer
        const lastUpdated = document.getElementById('last-updated');
        if (lastUpdated) {
            const now = new Date();
            lastUpdated.textContent = `Last updated: ${this.formatRelativeTime(now.toISOString())}`;
        }
    }

    /**
     * Start auto-refresh of timestamps
     * @param {number} interval - Refresh interval in milliseconds (default: 60000 = 1 minute)
     */
    startAutoRefresh(interval = 60000) {
        this.stopAutoRefresh(); // Clear any existing interval
        
        this.refreshInterval = setInterval(() => {
            this.updateAllTimestamps();
        }, interval);
        
        // Initial update
        this.updateAllTimestamps();
    }

    /**
     * Stop auto-refresh of timestamps
     */
    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    /**
     * Calculate freshness score based on content age
     * @param {string|Date} timestamp - Content timestamp
     * @returns {number} - Freshness score from 0 to 1
     */
    calculateFreshness(timestamp) {
        if (!timestamp) return 0;

        try {
            const date = new Date(timestamp);
            const now = new Date();
            const ageInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);

            // Freshness scoring (higher is fresher)
            if (ageInHours < 1) return 1.0;           // Last hour: perfect
            if (ageInHours < 24) return 0.9;         // Last day: excellent
            if (ageInHours < 168) return 0.7;        // Last week: good
            if (ageInHours < 720) return 0.5;        // Last month: okay
            if (ageInHours < 8760) return 0.3;       // Last year: old
            return 0.1;                               // Very old: poor
        } catch (error) {
            return 0;
        }
    }

    /**
     * Get appropriate refresh interval based on content age
     * @param {string|Date} timestamp - Content timestamp
     * @returns {number} - Recommended refresh interval in milliseconds
     */
    getRefreshInterval(timestamp) {
        if (!timestamp) return 300000; // 5 minutes default

        try {
            const date = new Date(timestamp);
            const now = new Date();
            const ageInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);

            if (ageInHours < 1) return 30000;        // 30 seconds for very recent
            if (ageInHours < 24) return 60000;       // 1 minute for recent
            if (ageInHours < 168) return 300000;     // 5 minutes for this week
            return 900000;                            // 15 minutes for older content
        } catch (error) {
            return 300000; // 5 minutes default
        }
    }
}

// Global instance
window.timeFormatter = new TimeFormatter();

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.timeFormatter.startAutoRefresh();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TimeFormatter;
}