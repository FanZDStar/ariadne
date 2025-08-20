module.exports = {
  apps: [{
    name: 'ariadne-backend',
    cwd: '/www/wwwroot/ariadne-backend',
    script: 'venv/bin/python',
    args: '-m uvicorn app.main:app --host 0.0.0.0 --port 8000',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true,
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
  }]
}
