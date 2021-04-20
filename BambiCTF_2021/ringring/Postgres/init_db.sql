CREATE SCHEMA IF NOT EXISTS ringring;

CREATE TABLE IF NOT EXISTS ringring.alarms
(
    session_id text,
    alarm_time text,
    alarm_text text
);

CREATE TABLE IF NOT EXISTS ringring.sessions
(
    session_id text,
    started     timestamptz DEFAULT now(),
    is_billable boolean CHECK ( is_billable != is_vip ) DEFAULT TRUE,
    is_vip     boolean DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS session_idx ON ringring.sessions(session_id);
CREATE INDEX IF NOT EXISTS alarms_idx ON ringring.alarms(session_id);
CREATE INDEX IF NOT EXISTS vip_idx ON ringring.sessions(is_vip);
