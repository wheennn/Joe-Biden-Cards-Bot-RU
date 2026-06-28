CREATE TABLE
    IF NOT EXISTS users (
        -- v0.1:
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        total_cards INTEGER DEFAULT 0,
        last_card_time FLOAT DEFAULT 0,
        -- v0.1.1:
        unlocked_cards INTEGER DEFAULT 0,
        xp INTEGER DEFAULT 0,
        -- v0.1.2:
        fpacks INTEGER DEFAULT 0,
        -- v0.1.3:
        collected_gift INTEGER DEFAULT 0,
        purchased_special_action INTEGER DEFAULT 0,
        spacks INTEGER DEFAULT 0,
        total_progress INTEGER DEFAULT 0,
        pack_stage INTEGER DEFAULT 1,
        fpack_unlocked_cards INTEGER DEFAULT 0,
        fpack_progress INTEGER DEFAULT 0,
        spack_unlocked_cards INTEGER DEFAULT 0,
        spack_progress INTEGER DEFAULT 0,
        exclusive_unlocked_cards INTEGER DEFAULT 0
    );

CREATE TABLE
    IF NOT EXISTS user_cards (
        user_id INTEGER NOT NULL,
        card_id INTEGER NOT NULL,
        count INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (user_id, card_id)
    );

CREATE TABLE
    IF NOT EXISTS card_stats (
        -- v0.1:
        total_count INTEGER NOT NULL DEFAULT 0,
        card_id INTEGER PRIMARY KEY,
        -- v0.1.1:
        first_unlocked TEXT
    );

CREATE TABLE
    IF NOT EXISTS reminder_spam (
        -- v0.1.2:
        reminder_cd INTEGER DEFAULT 0,
        reminder_2 INTEGER DEFAULT 0,
        reminder_8 INTEGER DEFAULT 0,
        reminder_24 INTEGER DEFAULT 0,
        user_id INTEGER PRIMARY KEY
    );

CREATE TABLE
    IF NOT EXISTS season_info (
        -- v0.1.2:
        current_season INTEGER DEFAULT 1,
        season INTEGER PRIMARY KEY,
        rewards TEXT,
        winner TEXT
    );

CREATE TABLE
    IF NOT EXISTS global_rewards (
        -- v0.1.3:
        reward_name TEXT NOT NULL,
        reward_indicator INTEGER NOT NULL,
        reward_xp INTEGER NOT NULL,
        reward_stage INTEGER NOT NULL,
        status INTEGER DEFAULT 0 NOT NULL,
        id INTEGER DEFAULT 1 NOT NULL,
        CONSTRAINT status_check CHECK (status IN (0, 1)),
        CONSTRAINT stage_check CHECK (reward_stage IN (1, 2, 3, 4, 5)),
        UNIQUE (id, reward_name, reward_stage)
    );

CREATE TABLE
    IF NOT EXISTS settings (
        -- v0.1.3:
        user_id INTEGER PRIMARY KEY,
        openings_per_time INTEGER DEFAULT 1,
        showing_prefixes INTEGER DEFAULT 1,
        -- v0.1.4:
        showing_my_profile INTEGER DEFAULT 1
    );

COMMIT