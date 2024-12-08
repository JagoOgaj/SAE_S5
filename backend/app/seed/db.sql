DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS conversation_messages CASCADE;
DROP TABLE IF EXISTS conversation_images CASCADE;
DROP TABLE IF EXISTS token_block_list CASCADE;

CREATE TYPE role_enum AS ENUM ('ADMIN', 'USER');

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name role_enum NOT NULL UNIQUE
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL
);

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TYPE message_type_enum AS ENUM ('USER', 'AI');

CREATE TABLE conversation_messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    message_type message_type_enum NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE TABLE conversation_images (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    image_data BYTEA NOT NULL,       
    image_size INTEGER NOT NULL CHECK (image_size > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE TABLE token_block_list (
    id SERIAL PRIMARY KEY,                                       
    jti VARCHAR NOT NULL UNIQUE,                                 
    token_type VARCHAR NOT NULL,                                 
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE, 
    revoked_at TIMESTAMP,                                        
    expires TIMESTAMP NOT NULL                                  
);

CREATE INDEX idx_conversations_user_id ON conversations (user_id);  
CREATE UNIQUE INDEX roles_name_lower_idx ON roles (LOWER(name));

INSERT INTO roles (name) VALUES 
    ('ADMIN'), 
    ('USER');