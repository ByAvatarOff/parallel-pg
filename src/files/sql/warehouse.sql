CREATE TABLE IF NOT EXISTS warehouse(
    id SERIAL PRIMARY KEY,
    count INT,
    balance INT,
    name VARCHAR
);
INSERT INTO warehouse VALUES (1, 0, 100, 'Alice');
INSERT INTO warehouse VALUES (2, 0, 200, 'Bob');