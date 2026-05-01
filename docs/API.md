# API Reference

The Flask API exposes two endpoints.

## `GET /health`

Returns service health.

Response:

```json
{
  "status": "ok"
}
```

## `POST /scrape`

Scrapes public TikTok hashtag pages and returns video metadata.

Request:

```json
{
  "hashtag": "funny",
  "limit": 5
}
```

Fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `hashtag` | string | no | Hashtag to inspect, with or without `#` |
| `limit` | number | no | Maximum videos to return, capped by `MAX_LIMIT` |

Successful response:

```json
[
  {
    "hashtag_searched": "funny",
    "author": "creator",
    "video_link": "https://www.tiktok.com/@creator/video/123",
    "playCount": 100000,
    "diggCount": 12000,
    "commentCount": 300,
    "shareCount": 900,
    "collectCount": 800,
    "hashtags": ["#funny"],
    "description_full": "Example public caption"
  }
]
```

Error response:

```json
{
  "error": "hashtag must contain at least one letter or number"
}
```

## Notes

- TikTok changes its markup often, so scraping selectors may need updates over time.
- Keep limits conservative to reduce blocking and rate-limit issues.
- The API returns public metadata only and does not download videos.
