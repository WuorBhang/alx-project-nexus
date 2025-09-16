#!/bin/bash

# Start PostgreSQL service
echo "Starting PostgreSQL service..."
sudo service postgresql start

# Create database and user
echo "Creating database and user..."
sudo -u postgres psql << EOF
CREATE DATABASE voting_system;
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE voting_system TO postgres;
EOF

echo "Database setup completed."