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

INSERT INTO "contact" ("id", "user_id", "nickname", "thumbnail")	VALUES ('1000', 'user1', 'contact-1', 'thumbnail-1');