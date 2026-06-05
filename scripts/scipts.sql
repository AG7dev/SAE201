-- A transformer en script python plus tard
CREATE TABLE IF NOT EXISTS user_table(
	username VARCHAR(64) PRIMARY KEY,
    password VARCHAR(64) NOT NULL,
    permissions VARCHAR(64) DEFAULT NULL
	);