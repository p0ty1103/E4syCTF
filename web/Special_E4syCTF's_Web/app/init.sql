DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    flag VARCHAR(255)
);

INSERT INTO users (username, password, flag) VALUES
('guest', 'guestpass123', NULL),
('user', 'securepass', NULL),
('admin', 'SuPeRsEcReTaDmInPaSsWoRd1234', 'E4syCTF{SuPeR_E4sy_Sq1_4Nd_Xss_Ch4ll3nge}');
