# YouTube API Implementation Guide

## Overview

The YouTube Dynamic Search system (`youtube-dynamic-search.py`) currently uses mock data for demonstration. This guide explains how to implement real YouTube API integration.

## API Options

### 1. YouTube Data API v3 (Recommended)

**Pros:**
- Official Google API
- Comprehensive data access
- Well-documented
- Reliable and stable

**Cons:**
- Requires API key and quota management
- Rate limiting (10,000 units/day free tier)
- May require billing for higher usage

**Implementation:**
```python
import googleapiclient.discovery

def _search_youtube_api(self, search_term: str, published_after: datetime) -> List[Dict[str, Any]]:
    """Search YouTube API v3"""
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
    
    # Search for videos
    search_response = youtube.search().list(
        q=search_term,
        part="snippet",
        type="video",
        publishedAfter=published_after.isoformat(),
        maxResults=25,
        order="relevance",
        videoDuration="medium",  # 4-20 minutes
        videoDefinition="any",
        videoCaption="any"
    ).execute()
    
    # Get video details (statistics, content details)
    video_ids = [item["id"]["videoId"] for item in search_response["items"]]
    
    videos_response = youtube.videos().list(
        part="statistics,contentDetails",
        id=",".join(video_ids)
    ).execute()
    
    # Combine search and video data
    results = []
    for search_item, video_item in zip(search_response["items"], videos_response["items"]):
        result = {
            "id": search_item["id"],
            "snippet": search_item["snippet"],
            "statistics": video_item["statistics"],
            "contentDetails": video_item["contentDetails"]
        }
        results.append(result)
    
    return results
```

**Setup Requirements:**
1. Create Google Cloud Project
2. Enable YouTube Data API v3
3. Create API key
4. Set environment variable: `YOUTUBE_API_KEY`

### 2. Invidious API (Alternative)

**Pros:**
- No API key required
- Privacy-focused
- Multiple public instances

**Cons:**
- Less reliable than official API
- Limited instances availability
- Potential rate limiting

**Implementation:**
```python
import requests

def _search_youtube_api(self, search_term: str, published_after: datetime) -> List[Dict[str, Any]]:
    """Search using Invidious API"""
    invidious_instance = "https://vid.puffyan.us"  # or other instance
    
    params = {
        "q": search_term,
        "type": "video",
        "sort_by": "relevance",
        "date": "month",  # last month
        "duration": "medium",
        "page": 1
    }
    
    response = requests.get(f"{invidious_instance}/api/v1/search", params=params)
    response.raise_for_status()
    
    search_results = response.json()
    
    # Convert to YouTube Data API format
    results = []
    for item in search_results:
        result = {
            "id": {"videoId": item["videoId"]},
            "snippet": {
                "title": item["title"],
                "channelTitle": item["author"],
                "channelId": item["authorId"],
                "publishedAt": datetime.fromtimestamp(item["published"]).isoformat() + "Z",
                "description": item["description"],
                "thumbnails": {
                    "medium": {"url": item["videoThumbnails"][2]["url"]}
                }
            },
            "statistics": {
                "viewCount": str(item["viewCount"]),
                "likeCount": "0",  # Not available in Invidious
                "commentCount": "0"
            },
            "contentDetails": {
                "duration": f"PT{item['lengthSeconds']}S"
            }
        }
        results.append(result)
    
    return results
```

### 3. Web Scraping (Last Resort)

**Use only if API options are not viable**

**Implementation considerations:**
- Use rotating user agents
- Implement proper delays
- Handle JavaScript-rendered content
- Respect robots.txt
- Monitor for anti-bot measures

## Implementation Steps

### Step 1: Choose API Method

Update `youtube-dynamic-search.py` to replace the mock implementation:

```python
# Replace the mock implementation in _search_youtube_api method
def _search_youtube_api(self, search_term: str, published_after: datetime) -> List[Dict[str, Any]]:
    """Search YouTube API (replace with actual implementation)"""
    
    # Remove this warning and mock data
    # logger.warning("Using mock YouTube search - replace with actual API implementation")
    
    # Implement your chosen API method here
    if os.getenv("YOUTUBE_API_KEY"):
        return self._search_youtube_data_api(search_term, published_after)
    else:
        return self._search_invidious_api(search_term, published_after)
```

### Step 2: Add Configuration

Update `youtube-search-config.json`:

```json
{
  "api_settings": {
    "preferred_method": "youtube_data_api",
    "fallback_method": "invidious_api",
    "api_key_env_var": "YOUTUBE_API_KEY",
    "invidious_instances": [
      "https://vid.puffyan.us",
      "https://invidious.snopyta.org",
      "https://yewtu.be"
    ]
  },
  "search_terms": {
    // existing search terms
  },
  // rest of configuration
}
```

### Step 3: Add Dependencies

Add to requirements file or install:

```bash
# For YouTube Data API v3
pip install google-api-python-client

# For HTTP requests (Invidious)
pip install requests

# For web scraping (if needed)
pip install beautifulsoup4 selenium
```

### Step 4: Environment Setup

Create `.env` file:

```bash
# YouTube Data API v3
YOUTUBE_API_KEY=your_api_key_here

# Rate limiting
YOUTUBE_REQUESTS_PER_DAY=10000
YOUTUBE_REQUESTS_PER_MINUTE=100
```

### Step 5: Error Handling

Implement robust error handling:

```python
def _search_with_fallback(self, search_term: str, published_after: datetime) -> List[Dict[str, Any]]:
    """Search with fallback methods"""
    
    methods = [
        ("YouTube Data API", self._search_youtube_data_api),
        ("Invidious API", self._search_invidious_api)
    ]
    
    for method_name, method_func in methods:
        try:
            logger.info(f"Trying {method_name} for: {search_term}")
            results = method_func(search_term, published_after)
            logger.info(f"✅ {method_name} succeeded: {len(results)} results")
            return results
            
        except Exception as e:
            logger.warning(f"❌ {method_name} failed: {str(e)}")
            continue
    
    logger.error(f"All API methods failed for: {search_term}")
    return []
```

## Rate Limiting Best Practices

### YouTube Data API v3 Quotas

- Search costs 100 units per request
- Video details cost 1 unit per video
- Daily quota: 10,000 units (free tier)
- Plan accordingly: ~90 searches per day

### Implementation

```python
class QuotaManager:
    def __init__(self, daily_limit: int = 10000):
        self.daily_limit = daily_limit
        self.current_usage = self._load_current_usage()
    
    def can_make_request(self, cost: int) -> bool:
        return self.current_usage + cost <= self.daily_limit
    
    def record_usage(self, cost: int):
        self.current_usage += cost
        self._save_current_usage()
```

## Testing

Test the implementation with:

```bash
# Test with API key
export YOUTUBE_API_KEY="your_key"
python3 youtube-dynamic-search.py

# Test fallback without API key
unset YOUTUBE_API_KEY
python3 youtube-dynamic-search.py
```

## Monitoring

Add monitoring for:
- API quota usage
- Error rates by method
- Search result quality
- Response times

## Security Considerations

1. Store API keys securely
2. Rotate keys regularly
3. Monitor for unauthorized usage
4. Implement IP whitelisting if possible
5. Use HTTPS for all requests

## Next Steps

1. Choose your preferred API method
2. Set up credentials and environment
3. Replace mock implementation
4. Test with real data
5. Monitor performance and adjust rate limiting
6. Consider implementing caching for frequently searched terms