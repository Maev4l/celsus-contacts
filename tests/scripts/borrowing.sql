CREATE TABLE IF NOT EXISTS "borrowing"
(
    user_id VARCHAR(36) NOT NULL,
    lending_id VARCHAR(36) NOT NULL,
    contact_id VARCHAR(36) NOT NULL,
    book_id VARCHAR(36) NOT NULL
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

-- test delete: contact with id 1004 cannot be deleted
INSERT INTO "borrowing" ("lending_id", "user_id", "contact_id", "book_id") VALUES ('1', 'user4', '1004', 'book-id-1');

-- test return book
INSERT INTO "borrowing" ("lending_id", "user_id", "contact_id", "book_id") VALUES ('2', 'user6', '1006', 'book-id-2');