CREATE TABLE opposition (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(255),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) CHECK (status IN ('open', 'closed'))
);

CREATE TABLE user_opposition (
    user_id INT,
    opposition_id INT,
    PRIMARY KEY (user_id, opposition_id),
    FOREIGN KEY (opposition_id) REFERENCES opposition(id)
);

INSERT INTO opposition (id, name, description, created_at, source, start_date, end_date, status)
VALUES
(1, 'Opposition 1', 'Description of opposition 1', NOW(), 'Source 1', '2023-01-01', '2023-12-31', 'open'),
(2, 'Opposition 2', 'Description of opposition 2', NOW(), 'Source 2', '2023-02-01', '2023-11-30', 'closed'),
(3, 'Opposition 3', 'Description of opposition 3', NOW(), 'Source 3', '2023-03-01', NULL, 'open');

INSERT INTO user_opposition (user_id, opposition_id)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 1),
(5, 2);