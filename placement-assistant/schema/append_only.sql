-- TODO (lab 2): make SQLite itself refuse UPDATE and DELETE on message.
CREATE TRIGGER IF NOT EXISTS prevent_message_update
BEFORE UPDATE ON message
BEGIN
    SELECT RAISE(ABORT, 'message table is append-only');
END;

CREATE TRIGGER IF NOT EXISTS prevent_message_delete
BEFORE DELETE ON message
BEGIN
    SELECT RAISE(ABORT, 'message table is append-only');
END;