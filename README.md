# Celebrity Khobor

## Streamlit Cloud setup

The app needs an Ollama server reachable from Streamlit Cloud. Ollama running on
your personal computer at `localhost` is not reachable by the deployed app.

1. Deploy an Ollama server behind a publicly reachable HTTPS endpoint. Ensure
   the `llama3.2` model is available on that server.
2. In Streamlit Cloud, open the app's **Settings > Secrets** and add:

   ```toml
   OLLAMA_BASE_URL = "https://your-ollama-host.example"
   OLLAMA_MODEL = "llama3.2"
   ```

3. If the endpoint is protected by a reverse proxy that expects a bearer token,
   add `OLLAMA_API_KEY = "your-token"` to Secrets. The app sends it as an
   `Authorization: Bearer` header. Keep the endpoint on HTTPS and never commit
   real tokens to the repository.
