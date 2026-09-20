.env will eventually contain configuration/secrets that shouldn't be hard-coded into our Python files.


For example, later:
LLM_API_KEY=...
DATABASE_URL=...


Instead of doing this:
api_key = "my-secret-key"


we'll do something conceptually like:
.env
 ↓
Configuration
 ↓
LLM Client


This is important for security.
We'll properly configure this later. For now, we're just establishing the file.