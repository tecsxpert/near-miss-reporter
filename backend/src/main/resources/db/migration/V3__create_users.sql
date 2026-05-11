-- Drop table if it exists to ensure a clean state matching the entity
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Seed an admin user
INSERT INTO users (username, password) VALUES ('admin', 'admin');
