SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PDF_PATH="$SCRIPT_DIR/../assets/sample.pdf"
API_URL="http://localhost:8080"

# Health check
echo "--------------------------------"
echo "Testing Health check endpoint"
curl -X GET "$API_URL/health_check"
echo
echo "--------------------------------"

# Ingest
echo "Testing Ingest endpoint"
curl -X POST "$API_URL/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "application/pdf",
    "data": "$(base64 -i $PDF_PATH | tr -d '\n')"
  }'
echo "--------------------------------"

# Retrieve
echo "Testing Retrieve endpoint"
curl -X POST "$API_URL/retrieve" \
  -H "Content-Type: application/json" \
  -d '{
    "query_texts": [
      "What is machine learning?",
      "Explain vector databases"
    ]
  }'
echo "--------------------------------"

# Summarize
echo "Testing Summarize endpoint"
curl -X POST "$API_URL/summarize" \
  -H "Content-Type: application/json" \
  -d "{
    \"content_type\": \"application/pdf\",
    \"data\": \"$(base64 -i $PDF_PATH | tr -d '\n')\"
  }"
echo "--------------------------------"
