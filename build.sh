@"
#!/usr/bin/env bash
# Build script for Render.com

echo "🚀 Starting build process..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Apply database migrations
echo "🗄 Applying database migrations..."
python manage.py migrate

echo "✅ Build completed successfully!"
"@ | Out-File -FilePath build.sh -Encoding UTF8