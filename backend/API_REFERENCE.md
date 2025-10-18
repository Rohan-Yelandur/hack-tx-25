# 📖 API Reference

Complete reference for the Math Explanation Backend API.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently no authentication required. For production, implement API keys or OAuth.

## Response Format

All endpoints return JSON in the following format:

```json
{
  "success": true,
  "message": "Human-readable message",
  "timestamp": "2025-10-18T12:34:56.789Z",
  "data": { /* Endpoint-specific data */ },
  "error": "Error message (only if success=false)"
}
```

---

## Endpoints

### 1. Health Check

Check if the service is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "success": true,
  "message": "Service is healthy",
  "timestamp": "2025-10-18T12:34:56.789Z",
  "data": {
    "status": "ok"
  }
}
```

**Example:**
```bash
curl http://localhost:5000/health
```

---

### 2. Service Status

Get detailed service status and configuration.

**Endpoint:** `GET /status`

**Response:**
```json
{
  "success": true,
  "message": "Service status",
  "timestamp": "2025-10-18T12:34:56.789Z",
  "data": {
    "status": "running",
    "services": {
      "gemini": "configured",
      "eleven_labs": "configured",
      "manim": "available"
    },
    "storage": {
      "uploads": {
        "count": 5,
        "size_bytes": 1048576
      },
      "audio": {
        "count": 10,
        "size_bytes": 5242880
      },
      "videos": {
        "count": 8,
        "size_bytes": 104857600
      }
    }
  }
}
```

**Example:**
```bash
curl http://localhost:5000/status
```

---

### 3. Solve Text Problem

Solve a text-based math problem and generate explanation materials.

**Endpoint:** `POST /api/solve_text`

**Request Body:**
```json
{
  "problem": "string (required) - The math problem to solve",
  "generate_audio": "boolean (optional, default: true) - Generate audio narration",
  "generate_video": "boolean (optional, default: true) - Generate video animation"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Problem solved successfully",
  "timestamp": "2025-10-18T12:34:56.789Z",
  "data": {
    "problem": "Original problem text",
    "solution": "Step-by-step solution",
    "teaching_script": "Narration script",
    "estimated_duration": 120.5,
    "audio": {
      "url": "/static/audio/narration_abc123.mp3",
      "filename": "narration_abc123.mp3",
      "file_size": 524288,
      "timestamps": [
        {
          "word": "Let's",
          "start_time": 0.0,
          "end_time": 0.4
        }
      ]
    },
    "video": {
      "url": "/static/videos/explanation_abc123.mp4",
      "filename": "explanation_abc123.mp4",
      "file_size": 10485760
    }
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "message": "",
  "timestamp": "2025-10-18T12:34:56.789Z",
  "error": "Problem text cannot be empty"
}
```

**Examples:**

Simple problem (solution only):
```bash
curl -X POST http://localhost:5000/api/solve_text \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Solve for x: 2x + 5 = 13",
    "generate_audio": false,
    "generate_video": false
  }'
```

Full pipeline (audio + video):
```bash
curl -X POST http://localhost:5000/api/solve_text \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Find the derivative of f(x) = x^2 + 3x - 5",
    "generate_audio": true,
    "generate_video": true
  }'
```

---

### 4. Solve PDF Problem

Upload a PDF worksheet and generate explanations for contained problems.

**Endpoint:** `POST /api/solve_pdf`

**Request:** Multipart form data

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | File | Yes | PDF file to process |
| `generate_audio` | String | No | "true" or "false" (default: "true") |
| `generate_video` | String | No | "true" or "false" (default: "true") |

**Response:**
```json
{
  "success": true,
  "message": "PDF processed successfully with 2 problem(s)",
  "timestamp": "2025-10-18T12:34:56.789Z",
  "data": {
    "pdf_filename": "worksheet.pdf",
    "problems_count": 2,
    "problems": [
      {
        "problem_number": 1,
        "problem_text": "Extracted problem text",
        "solution": "Step-by-step solution",
        "teaching_script": "Narration script",
        "estimated_duration": 90.0,
        "audio": {
          "url": "/static/audio/narration_xyz789.mp3",
          "filename": "narration_xyz789.mp3",
          "file_size": 393216,
          "timestamps": []
        },
        "video": {
          "url": "/static/videos/explanation_xyz789.mp4",
          "filename": "explanation_xyz789.mp4",
          "file_size": 8388608
        }
      }
    ]
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/solve_pdf \
  -F "file=@worksheet.pdf" \
  -F "generate_audio=true" \
  -F "generate_video=true"
```

---

### 5. Manual Cleanup

Manually trigger cleanup of old files.

**Endpoint:** `POST /api/cleanup`

**Response:**
```json
{
  "success": true,
  "message": "Cleanup completed",
  "timestamp": "2025-10-18T12:34:56.789Z",
  "data": {
    "uploads_deleted": 3,
    "audio_deleted": 5,
    "videos_deleted": 4
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/cleanup
```

---

### 6. Check Text Service Status

Check if the text solving service is available.

**Endpoint:** `GET /api/solve_text/status`

**Response:**
```json
{
  "success": true,
  "message": "Text solving service is available",
  "timestamp": "2025-10-18T12:34:56.789Z",
  "data": {
    "status": "ready"
  }
}
```

---

### 7. Check PDF Service Status

Check if the PDF solving service is available.

**Endpoint:** `GET /api/solve_pdf/status`

**Response:**
```json
{
  "success": true,
  "message": "PDF solving service is available",
  "timestamp": "2025-10-18T12:34:56.789Z",
  "data": {
    "status": "ready"
  }
}
```

---

## Static File Access

Generated files are accessible via static URLs:

### Audio Files
```
GET /static/audio/{filename}
```

Example:
```
http://localhost:5000/static/audio/narration_abc123.mp3
```

### Video Files
```
GET /static/videos/{filename}
```

Example:
```
http://localhost:5000/static/videos/explanation_abc123.mp4
```

---

## Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Invalid input or missing required fields |
| 404 | Not Found | Endpoint or resource not found |
| 500 | Internal Server Error | Server-side error during processing |

---

## Rate Limiting

Currently no rate limiting implemented. For production:
- Implement rate limiting per IP
- Consider API key-based quotas
- Add request queuing for expensive operations

---

## Data Validation

### Problem Text Requirements

- Minimum length: 10 characters
- Maximum length: 10,000 characters
- Cannot be empty or whitespace only

### PDF Requirements

- File extension must be `.pdf`
- Maximum file size: 16 MB (configurable)
- Must be a valid PDF file

---

## Processing Times

Typical processing times (may vary):

| Operation | Time |
|-----------|------|
| Solution generation | 5-15 seconds |
| Audio generation | 10-30 seconds |
| Video generation | 30-120 seconds |
| Full pipeline | 45-165 seconds |

**Note:** Video generation is the slowest step. Use `generate_video=false` for faster responses during development.

---

## Best Practices

### 1. Development Testing

Test without expensive operations:
```json
{
  "problem": "Your problem here",
  "generate_audio": false,
  "generate_video": false
}
```

### 2. Progressive Enhancement

Build features incrementally:
1. Test with solution only
2. Add audio generation
3. Finally, enable video generation

### 3. Error Handling

Always check the `success` field:
```javascript
if (response.success) {
  // Handle success
} else {
  // Handle error using response.error
}
```

### 4. Timeout Configuration

Set appropriate timeouts in your client:
- Solution only: 30 seconds
- With audio: 60 seconds
- Full pipeline: 180 seconds

---

## Example Integration (JavaScript)

```javascript
async function solveProblem(problem) {
  try {
    const response = await fetch('http://localhost:5000/api/solve_text', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        problem: problem,
        generate_audio: true,
        generate_video: true
      }),
      timeout: 180000 // 3 minutes
    });
    
    const result = await response.json();
    
    if (result.success) {
      console.log('Solution:', result.data.solution);
      console.log('Audio URL:', result.data.audio.url);
      console.log('Video URL:', result.data.video.url);
      return result.data;
    } else {
      console.error('Error:', result.error);
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('Request failed:', error);
    throw error;
  }
}

// Usage
solveProblem('What is the derivative of x^2?')
  .then(data => {
    // Use the data
  })
  .catch(error => {
    // Handle error
  });
```

---

## Example Integration (Python)

```python
import requests

def solve_problem(problem, generate_audio=True, generate_video=True):
    """Solve a math problem using the API."""
    url = 'http://localhost:5000/api/solve_text'
    
    payload = {
        'problem': problem,
        'generate_audio': generate_audio,
        'generate_video': generate_video
    }
    
    try:
        response = requests.post(url, json=payload, timeout=180)
        result = response.json()
        
        if result['success']:
            return result['data']
        else:
            raise Exception(result['error'])
            
    except requests.exceptions.Timeout:
        raise Exception('Request timed out')
    except Exception as e:
        raise Exception(f'API error: {str(e)}')

# Usage
try:
    data = solve_problem('What is 2 + 2?')
    print('Solution:', data['solution'])
    print('Audio:', data['audio']['url'])
    print('Video:', data['video']['url'])
except Exception as e:
    print('Error:', str(e))
```

---

## WebSocket Support (Future)

For real-time progress updates, consider implementing WebSocket support:

```javascript
// Planned for future version
const socket = io('http://localhost:5000');

socket.on('progress', (data) => {
  console.log(`Progress: ${data.step} - ${data.percentage}%`);
});
```

---

## Versioning

Current version: **v1.0.0**

API versioning will be implemented as:
```
/api/v1/solve_text
/api/v2/solve_text
```

---

## Support

For issues or questions:
- Check server logs for detailed errors
- Review the setup guide (SETUP.md)
- Verify all environment variables are set
- Test with simple examples first

