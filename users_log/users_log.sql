CREATE table USERS (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    geo TEXT
);

CREATE table LOG (
    user_id INTEGER NOT NULL REFERENCES USERS(user_id),
    time TEXT NOT NULL,
    bet REAL,
    win REAL
);


