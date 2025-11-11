#cloud-config
package_update: true
packages:
  - docker.io
  - docker-compose-plugin
runcmd:
  - [ sh, -c, "usermod -aG docker ubuntu || true" ]
  - [ sh, -c, "mkdir -p /opt/driver-forecast && chown ubuntu:ubuntu /opt/driver-forecast" ]
  - [ sh, -c, "cat > /etc/systemd/system/driver-forecast.service <<'EOF'
[Unit]
Description=Driver Forecast App
After=docker.service

[Service]
Type=simple
Restart=always
User=ubuntu
WorkingDirectory=/opt/driver-forecast
ExecStart=/usr/bin/docker compose up
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target
EOF" ]
  - [ sh, -c, "systemctl daemon-reload && systemctl enable driver-forecast.service && systemctl start driver-forecast.service || true" ]
