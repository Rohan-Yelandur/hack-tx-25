# 🏗️ Architecture Overview

This document provides a detailed overview of the Math Explanation Backend architecture, design patterns, and implementation details.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  (Frontend, Mobile App, API Consumers)                          │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP/JSON
┌─────────────────────▼───────────────────────────────────────────┐
│                      Flask API Layer                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Routes (API Endpoints)                                   │  │
│  │  • /api/solve_text    • /api/solve_pdf                   │  │
│  │  • /health            • /status                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                   Service Layer (Core Logic)                     │
│  ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  │
│  │   Gemini       │  │  Eleven Labs   │  │     Manim       │  │
│  │  Orchestrator  │  │     Audio      │  │     Video       │  │
│  │                │  │   Generator    │  │   Generator     │  │
│  └────────┬───────┘  └───────┬────────┘  └────────┬────────┘  │
│           │                  │                     │            │
│  ┌────────▼──────────────────▼─────────────────────▼────────┐  │
│  │              File Storage Service                         │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│                   External APIs & Tools                          │
│  ┌────────────┐  ┌────────────┐  ┌──────────┐  ┌──────────┐  │
│  │   Gemini   │  │   Eleven   │  │  Manim   │  │  FFmpeg  │  │
│  │    API     │  │  Labs API  │  │  Engine  │  │          │  │
│  └────────────┘  └────────────┘  └──────────┘  └──────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

## Pipeline Flow

### Text Problem Solving Pipeline

```
┌─────────────────┐
│  User submits   │
│  text problem   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  1. Problem Analysis                    │
│  Gemini: Identify concepts, difficulty  │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  2. Solution Generation                 │
│  Gemini: Step-by-step solution          │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  3. Teaching Script Creation            │
│  Gemini: Conversational explanation     │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  4. Scene Plan Generation               │
│  Gemini: Visual structure for video     │
└────────┬────────────────────────────────┘
         │
         ├─────────────────────┬───────────────────┐
         │                     │                   │
         ▼                     ▼                   ▼
┌──────────────────┐  ┌─────────────────┐  ┌────────────────┐
│  5a. Audio       │  │  5b. Video      │  │  Return        │
│  Generation      │  │  Generation     │  │  Solution      │
│  (Eleven Labs)   │  │  (Manim)        │  │  Text Only     │
└─────────┬────────┘  └────────┬────────┘  └────────┬───────┘
          │                    │                     │
          ├────────────────────┤                     │
          ▼                    ▼                     │
   ┌──────────────┐    ┌──────────────┐            │
   │  Audio File  │    │  Video File  │            │
   │  + Timestamp │    │  (with audio)│            │
   └──────┬───────┘    └──────┬───────┘            │
          │                    │                     │
          └────────────────────┴─────────────────────┘
                               │
                               ▼
                    ┌───────────────────┐
                    │  Return Complete  │
                    │  Response with    │
                    │  all URLs         │
                    └───────────────────┘
```

### PDF Problem Solving Pipeline

```
┌──────────────┐
│  User uploads│
│  PDF file    │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────┐
│  1. PDF Upload & Storage            │
│  FileStorage: Save to disk          │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  2. PDF Analysis                    │
│  Gemini: Extract problems (OCR-like)│
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  3. For Each Problem                │
│  Run Text Pipeline (steps 1-5)      │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  4. Aggregate Results               │
│  Combine all solutions, audio, video│
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  5. Return Array of Solutions       │
│  Each with its own media files      │
└─────────────────────────────────────┘
```

## Component Details

### 1. Flask API Layer (`app.py`, `routes/`)

**Responsibilities:**
- HTTP request handling
- Input validation
- Response formatting
- Error handling
- CORS management
- Static file serving

**Design Pattern:** Blueprint pattern for modular route organization

**Key Files:**
- `app.py` - Application factory and entry point
- `routes/solve_text.py` - Text problem endpoint
- `routes/solve_pdf.py` - PDF upload endpoint

### 2. Gemini Orchestrator (`services/orchestrator.py`)

**Responsibilities:**
- Problem understanding and analysis
- Solution generation with step-by-step reasoning
- Teaching script creation
- Scene plan generation for videos
- Concept extraction for reusability

**Design Pattern:** Facade pattern - provides simple interface to complex LLM operations

**Key Methods:**
```python
analyze_problem(problem_text) -> Dict
generate_solution(problem_text) -> Dict
create_teaching_script(problem_text, solution_text) -> Dict
generate_scene_plan(script) -> Dict
process_problem(problem_text) -> Dict  # Main orchestration
```

**Prompting Strategy:**
- Structured prompts in `utils/prompts.py`
- Separate prompts for each task
- Contextual information passed between stages
- LaTeX support for mathematical notation

### 3. Audio Generator (`services/audio_generator.py`)

**Responsibilities:**
- Text-to-speech conversion
- Timestamp generation for sync
- Audio file management
- Voice settings configuration

**Design Pattern:** Service pattern with configuration injection

**Key Features:**
- High-quality voice synthesis
- Character/word-level timestamps
- Configurable voice parameters (stability, similarity)
- Approximate timestamp fallback

**API Integration:**
```python
generate_audio(script, output_filename) -> Dict
generate_audio_with_timestamps(script, output_filename) -> Dict
```

### 4. Video Generator (`services/video_generator.py`)

**Responsibilities:**
- Dynamic Manim script generation
- Video rendering
- Audio-video synchronization
- Scene creation based on teaching plan

**Design Pattern:** Template Method pattern for video generation

**Key Features:**
- Dynamic scene generation
- LaTeX expression rendering
- Equation animations
- Audio synchronization via FFmpeg
- Quality configuration

**Process:**
1. Parse scene plan
2. Extract math expressions
3. Generate Manim Python script
4. Render video with Manim
5. Merge with audio using FFmpeg

### 5. File Storage (`services/file_storage.py`)

**Responsibilities:**
- File upload handling
- Unique filename generation
- URL generation for static files
- File cleanup (age-based)
- Storage statistics

**Design Pattern:** Repository pattern for file operations

**Directory Structure:**
```
static/
├── audio/       # Generated audio files
├── videos/      # Generated video files
└── uploads/     # Uploaded PDFs
```

## Data Flow

### Request Flow

1. **Client Request** → Flask route handler
2. **Route Handler** → Validates input
3. **Route Handler** → Calls appropriate service(s)
4. **Service** → Performs business logic
5. **Service** → Returns result
6. **Route Handler** → Formats response
7. **Route Handler** → Returns JSON to client

### File Flow

1. **Generation** → Service creates file
2. **Storage** → File saved to appropriate directory
3. **URL Generation** → FileStorage creates accessible URL
4. **Response** → URL included in API response
5. **Client Access** → Direct download via static URL
6. **Cleanup** → Old files removed after retention period

## Design Patterns Used

### 1. Application Factory Pattern
- `create_app()` function
- Enables multiple app instances
- Facilitates testing

### 2. Blueprint Pattern
- Modular route organization
- `/api` prefix for all API routes
- Separate blueprints per feature

### 3. Service Layer Pattern
- Business logic separated from routes
- Services are independent and testable
- Clear separation of concerns

### 4. Factory Functions
- `get_orchestrator()`
- `get_audio_generator()`
- `get_video_generator()`
- `get_file_storage()`
- Enables dependency injection

### 5. Configuration Object Pattern
- Centralized configuration in `Config` class
- Environment-based configuration
- Validation on startup

### 6. Template Method Pattern
- Video generation pipeline
- Extensible for different video styles

## Error Handling Strategy

### Three-Tier Error Handling

1. **Input Validation**
   - Validate at route level
   - Return 400 errors with clear messages
   - Use helper functions for common validations

2. **Service-Level Exceptions**
   - Services raise exceptions on failure
   - Include context in error messages
   - Log errors with stack traces

3. **Global Error Handlers**
   - Catch all exceptions in app.py
   - Return consistent error format
   - Log unexpected errors

### Error Response Format

```json
{
  "success": false,
  "message": "",
  "timestamp": "2025-10-18T12:34:56.789Z",
  "error": "Detailed error message"
}
```

## Logging Strategy

### Log Levels

- **INFO**: Normal operations, pipeline progress
- **WARNING**: Recoverable issues, missing optional features
- **ERROR**: Failures, exceptions, API errors

### Log Format

```
YYYY-MM-DD HH:MM:SS - module_name - LEVEL - message
```

### Key Logging Points

1. Service initialization
2. API calls (start/end)
3. File operations
4. Pipeline stages
5. Errors and exceptions

## Configuration Management

### Environment Variables

Loaded from `.env` file via `python-dotenv`:

```python
Config.GEMINI_API_KEY       # Required
Config.ELEVEN_LABS_API_KEY  # Required
Config.DEBUG                # Optional
Config.MANIM_QUALITY        # Optional
```

### Validation

`Config.validate()` called on startup:
- Checks required API keys
- Validates configuration values
- Fails fast with clear error messages

### Directory Initialization

`Config.ensure_directories()` creates required directories:
```python
static/audio/
static/videos/
static/uploads/
```

## Scalability Considerations

### Current Implementation

- **Synchronous processing**: Each request blocks until complete
- **Single-threaded**: One request at a time
- **Local file storage**: Files stored on server disk

### Future Enhancements

1. **Asynchronous Processing**
   - Celery + Redis for background jobs
   - Return job ID immediately
   - Poll for status or use webhooks

2. **Distributed Storage**
   - S3 or cloud storage for files
   - CDN for video/audio delivery
   - Database for metadata

3. **Horizontal Scaling**
   - Stateless application design
   - Load balancer for multiple instances
   - Shared storage or cache

4. **Caching**
   - Cache similar problems
   - Reuse generated content
   - Hash-based deduplication

5. **Rate Limiting**
   - Per-user quotas
   - API key-based limits
   - Request queuing

## Security Considerations

### Current State (Development)

- No authentication
- No rate limiting
- CORS enabled for all origins
- Local file storage

### Production Recommendations

1. **Authentication & Authorization**
   - API key authentication
   - OAuth 2.0 for user access
   - Role-based permissions

2. **Input Sanitization**
   - Already implemented: filename sanitization
   - LaTeX expression validation
   - PDF content scanning

3. **Rate Limiting**
   - Per-user/IP limits
   - Cost-based quotas (video generation is expensive)

4. **File Security**
   - Virus scanning for uploads
   - File type validation
   - Size limits enforced

5. **API Security**
   - HTTPS only in production
   - CORS restricted to known origins
   - Request signing

## Testing Strategy

### Unit Tests (Not Implemented - Hackathon)

Would test:
- Utility functions
- Service methods
- Validation logic

### Integration Tests

Would test:
- API endpoints
- Service integration
- File operations

### Manual Testing

Use `example_usage.py`:
```bash
python example_usage.py
```

## Performance Characteristics

### Typical Processing Times

| Operation | Time | Bottleneck |
|-----------|------|------------|
| Problem Analysis | 2-5s | Gemini API |
| Solution Generation | 3-8s | Gemini API |
| Teaching Script | 5-10s | Gemini API |
| Audio Generation | 5-20s | Eleven Labs API |
| Video Rendering | 30-90s | Manim + CPU |
| **Total** | **45-133s** | Video rendering |

### Optimization Opportunities

1. **Parallel Generation**: Generate audio and video simultaneously
2. **Quality Tradeoffs**: Lower video quality = faster rendering
3. **Caching**: Reuse similar explanations
4. **Precomputation**: Pre-render common problem types

## Extensibility Points

### Adding New Services

1. Create new file in `services/`
2. Implement service class
3. Add factory function
4. Import in `services/__init__.py`

### Adding New Endpoints

1. Create route file in `routes/`
2. Define route with `@api_bp.route()`
3. Import in `routes/__init__.py`

### Customizing Prompts

Edit `utils/prompts.py`:
- Modify existing prompt templates
- Add new prompt templates
- Adjust temperature/parameters

### Adding New Video Styles

Extend `VideoGenerator`:
- Add new scene generation methods
- Create style-specific templates
- Configure via environment variables

## Monitoring & Observability

### Current Implementation

- Console logging
- Basic health check endpoint
- Status endpoint with statistics

### Production Additions

1. **Structured Logging**: JSON logs for parsing
2. **Metrics**: Request counts, response times
3. **Tracing**: Distributed tracing for pipeline
4. **Alerts**: Error rate, processing time anomalies
5. **Dashboards**: Grafana/Kibana for visualization

## Conclusion

This architecture prioritizes:
- **Modularity**: Each component is independent
- **Maintainability**: Clear separation of concerns
- **Extensibility**: Easy to add new features
- **Simplicity**: Straightforward for hackathon context

The system is production-ready with the recommended enhancements for authentication, scaling, and monitoring.

