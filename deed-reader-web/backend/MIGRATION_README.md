# Flask to FastAPI Migration Guide

## Overview
We are migrating Deed Reader Pro from Flask to FastAPI to gain:
- **Async Support**: Better performance for I/O operations
- **Auto Documentation**: Built-in Swagger/ReDoc API docs
- **Type Safety**: Pydantic models for request/response validation
- **Better Performance**: Faster request handling with Starlette/Uvicorn

## Migration Status

### ✅ Completed
- [x] FastAPI application structure (`main.py`)
- [x] Document upload/processing endpoints
- [x] Dual-server migration script
- [x] Async file operations

### 🔄 In Progress
- [ ] Analysis routes migration
- [ ] Chat routes migration
- [ ] Plotting routes migration

### 📋 TODO
- [ ] Frontend API client updates
- [ ] Database migration to PostgreSQL
- [ ] WebSocket support for real-time updates
- [ ] Complete test coverage

## Running the Migration

### Option 1: Run Both Servers (Recommended During Migration)
```bash
cd deed-reader-web/backend
python run_migration.py
```
- Flask: http://localhost:5000 (legacy)
- FastAPI: http://localhost:8000 (new)
- API Docs: http://localhost:8000/api/docs

### Option 2: Run Only FastAPI
```bash
cd deed-reader-web/backend
uvicorn main:app --reload --port 8000
```

### Option 3: Run Only Flask (Legacy)
```bash
cd deed-reader-web/backend
python app.py
```

## API Endpoint Mapping

| Feature | Flask (Legacy) | FastAPI (New) | Status |
|---------|---------------|---------------|---------|
| Upload Document | POST `/api/documents/upload` | POST `/api/documents/upload` | ✅ Migrated |
| Process Text | POST `/api/documents/text` | POST `/api/documents/text` | ✅ Migrated |
| Validate Document | POST `/api/documents/validate` | POST `/api/documents/validate` | ✅ Migrated |
| Get Formats | - | GET `/api/documents/supported-formats` | ✅ New |
| Delete Document | - | DELETE `/api/documents/{upload_id}` | ✅ New |
| Analyze Document | POST `/api/analysis/analyze` | POST `/api/analysis/analyze` | 🔄 Pending |
| Chat | POST `/api/chat/ask` | POST `/api/chat/ask` | 🔄 Pending |
| Plot | POST `/api/plotting/plot` | POST `/api/plotting/plot` | 🔄 Pending |

## Testing the New Endpoints

### 1. Test Document Upload (FastAPI)
```bash
# Upload a PDF
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "accept: application/json" \
  -F "file=@test_deed.pdf"

# Upload a text file
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "accept: application/json" \
  -F "file=@test_deed.txt"
```

### 2. Test Text Processing
```bash
curl -X POST "http://localhost:8000/api/documents/text" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Beginning at a point on the North line of Main Street..."
  }'
```

### 3. Test Document Validation
```bash
curl -X POST "http://localhost:8000/api/documents/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This deed made this day between John Doe, Grantor..."
  }'
```

### 4. View API Documentation
Open in browser: http://localhost:8000/api/docs

## Key Differences for Developers

### 1. Async Functions
```python
# Flask (old)
@app.route('/upload', methods=['POST'])
def upload():
    file.save(path)
    
# FastAPI (new)
@router.post('/upload')
async def upload():
    async with aiofiles.open(path, 'wb') as f:
        await f.write(contents)
```

### 2. Request Validation
```python
# Flask (old)
data = request.get_json()
if not data or 'text' not in data:
    return jsonify({'error': 'No text'}), 400

# FastAPI (new)
class TextRequest(BaseModel):
    text: str = Field(..., min_length=10)

async def process(request: TextRequest):
    # Validation automatic!
```

### 3. Response Models
```python
# Flask (old)
return jsonify({
    'success': True,
    'message': 'Done'
})

# FastAPI (new)
class Response(BaseModel):
    success: bool
    message: str

@router.post('/endpoint', response_model=Response)
async def endpoint() -> Response:
    return Response(success=True, message="Done")
```

## Frontend Migration

To migrate frontend code to use FastAPI endpoints:

1. **Update Base URL** (during migration):
   ```javascript
   // Old
   const API_BASE = 'http://localhost:5000/api'
   
   // New (gradual migration)
   const FLASK_API = 'http://localhost:5000/api'
   const FASTAPI_API = 'http://localhost:8000/api'
   
   // Use FASTAPI_API for migrated endpoints
   ```

2. **Update Error Handling**:
   FastAPI returns more structured error responses with better validation messages.

3. **Use TypeScript Types**:
   Generate TypeScript types from FastAPI's OpenAPI schema for better type safety.

## Deployment Considerations

1. **Reverse Proxy Configuration**:
   ```nginx
   # Route to different backends based on readiness
   location /api/documents {
       proxy_pass http://localhost:8000;  # FastAPI
   }
   
   location /api/analysis {
       proxy_pass http://localhost:5000;  # Flask (until migrated)
   }
   ```

2. **Environment Variables**:
   Both Flask and FastAPI use the same `.env` file

3. **Performance Monitoring**:
   FastAPI includes built-in performance metrics in response headers

## Rollback Plan

If issues arise with FastAPI endpoints:
1. Frontend can immediately switch back to Flask endpoints
2. Both servers can run indefinitely during migration
3. No data migration required - both use same file storage

## Next Steps

1. Complete migration of remaining routes
2. Update frontend to use new endpoints
3. Add comprehensive tests
4. Performance benchmarking
5. Deprecate Flask application

## Questions?

- Check API docs: http://localhost:8000/api/docs
- Review type definitions in Pydantic models
- Test endpoints with Swagger UI 