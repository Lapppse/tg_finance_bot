CREATE TABLE IF NOT EXISTS expenses (
	user_id INTEGER NOT NULL,
	money INTEGER NOT NULL,
	desc VARCHAR(50),
	category VARCHAR(25),
	date DATE NOT NULL
)
