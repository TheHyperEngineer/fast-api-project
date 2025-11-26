# Run dev uvicorn with environment set for local Mongo
$env:MONGO_URI = 'mongodb://localhost:27017'
$env:MONGO_DB = 'test'
$env:MONGO_COLLECTION = 'medical'
python -m uvicorn app.main:app --reload --port 8005 --log-level debug
