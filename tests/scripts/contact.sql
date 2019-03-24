CREATE TABLE IF NOT EXISTS "contact"
(
    id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    nickname VARCHAR(100) NOT NULL,
    thumbnail TEXT,
    CONSTRAINT contact_id_key UNIQUE (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

-- for test update
INSERT INTO "contact" ("id", "user_id", "nickname", "thumbnail")VALUES ('1000', 'user1', 'contact-1', 'thumbnail-1');

-- for test get
INSERT INTO "contact" ("id", "user_id", "nickname", "thumbnail")VALUES ('1001', 'user2', 'contact-z-1', 'thumbnail-1');
INSERT INTO "contact" ("id", "user_id", "nickname", "thumbnail")VALUES ('1002', 'user2', 'contact-a-2', 'thumbnail-2');

-- for test delete
INSERT INTO "contact" ("id", "user_id", "nickname", "thumbnail")VALUES ('1003', 'user3', 'contact-z-1', 'thumbnail-1');
