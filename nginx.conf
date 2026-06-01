server {
    listen 80;
    server_name sop-review-2026.xyz www.sop-review-2026.xyz;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name sop-review-2026.xyz www.sop-review-2026.xyz;

    ssl_certificate /etc/letsencrypt/live/sop-review-2026.xyz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/sop-review-2026.xyz/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    root /var/www/agent-trap;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /collect {
        proxy_pass http://127.0.0.1:9999;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
