-- DROP TABLE IF EXISTS user;

-- Create user table
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create record table
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER NOT NULL,
    workoutTime TEXT DEFAULT (datetime('now', 'localtime')),
    pose TEXT NOT NULL,
    workoutDuration REAL NOT NULL,
    status TEXT,
    counts TEXT,
    FOREIGN KEY (userid) REFERENCES user(id)
);
