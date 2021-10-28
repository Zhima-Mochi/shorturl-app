CREATE TABLE long_to_code (
    code CHAR(6) NOT NULL, 
    orig_url VARCHAR(500) NOT NULL,
    created_time TIMESTAMP DEFAULT now() ON UPDATE now(),
    CONSTRAINT pk_code PRIMARY KEY (code),
    CONSTRAINT uc_orig_url UNIQUE (orig_url)
);