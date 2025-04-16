
CREATE DATABASE IF NOT EXISTS bookmyshow;

USE bookmyshow;

#user 
CREATE TABLE IF NOT EXISTS users(
    email INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- -- #Movies
-- CREATE TABLE IF NOT EXISTS movies(
--     movie_id INT AUTO_INCREMENT PRIMARY KEY,
--     movie_name VARCHAR(255) NOT NULL,
--     movie_genre VARCHAR(255) NOT NULL,
--     movie_duration INT NOT NULL,
--     movie_rating DECIMAL(3,2) NOT NULL,
--     movie_release_date DATE NOT NULL,
--     movie_image_url VARCHAR(255),
--     movie_description TEXT,
--     movie_language VARCHAR(255)
-- );

-- INSERT INTO movies (title, genre, language, duration, rating, release_date, description) VALUES
-- ('Inception', 'Sci-Fi', 'English', 148, 8.8, '2010-07-16', 'A thief who steals corporate secrets through dream-sharing.'),
-- ('3 Idiots', 'Comedy/Drama', 'Hindi', 171, 8.4, '2009-12-25', 'Three engineering students learn life lessons.'),
-- ('Interstellar', 'Sci-Fi', 'English', 169, 8.6, '2014-11-07', 'A team travels through a wormhole in space.'),
-- ('Bahubali: The Beginning', 'Action/Fantasy', 'Telugu', 159, 8.1, '2015-07-10', 'An orphan raised in a tribe discovers his royal heritage.'),
-- ('The Dark Knight', 'Action', 'English', 152, 9.0, '2008-07-18', 'Batman faces the Joker, a criminal mastermind.'),
-- ('PK', 'Comedy/Drama', 'Hindi', 153, 8.1, '2014-12-19', 'An alien on Earth questions religious dogmas.'),
-- ('Avengers: Endgame', 'Action/Sci-Fi', 'English', 181, 8.4, '2019-04-26', 'Superheroes assemble to undo the damage caused by Thanos.'),
-- ('Dangal', 'Biography/Sports', 'Hindi', 161, 8.4, '2016-12-23', 'A father trains his daughters to become world-class wrestlers.'),
-- ('RRR', 'Action/Drama', 'Telugu', 182, 8.0, '2022-03-25', 'Two revolutionaries fight for independence.'),
-- ('Shershaah', 'Biography/War', 'Hindi', 135, 8.4, '2021-08-12', 'Biopic of Captain Vikram Batra, Kargil war hero.');
-- -- #Theaters 
-- -- CREATE TABLE IF NOT EXISTS theaters(
-- --     theater_id INT AUTO_INCREMENT PRIMARY KEY,
-- --     theater_name VARCHAR(255) NOT NULL,
-- --     theater_address VARCHAR(255) NOT NULL,
-- --     total_seats INT
-- -- );
-- -- #Shows 
-- -- CREATE TABLE IF NOT EXISTS shows(
-- --     show_id INT AUTO_INCREMENT PRIMARY KEY,
-- --     movie_id INT NOT NULL,
-- --     threater_id INT,
-- --     show_date DATE NOT NULL,
-- --     show_time TIME NOT NULL,
-- --     price DECIMAL(8,2),
--     -- FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
--     -- FOREIGN KEY (threater_id) REFERENCES theaters(theater_id)
-- -- );

-- -- #Booking 
-- CREATE TABLE IF NOT EXISTS bookings(
--     booking_id INT AUTO_INCREMENT PRIMARY KEY,
--     user_id INT NOT NULL,
--     show_id INT NOT NULL,
--     seats TEXT,
--     total_price DECIMAL(10,2),
--     FOREIGN KEY (user_id) REFERENCES users(user_id),
--     FOREIGN KEY (show_id) REFERENCES shows(show_id)
-- );