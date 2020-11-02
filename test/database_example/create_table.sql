--create table named "users"
--this table stores user information such as name, id, corresponding playlist
CREATE TABLE IF NOT EXISTS users (
    index SERIAL,
    name VARCHAR(50) NOT NULL,
    id VARCHAR(50) NOT NULL,
    listen_playlist VARCHAR(50) NOT NULL,  
    recommended_playlist VARCHAR(50) NOT NULL, 
    PRIMARY KEY (index)
);

--create table named "song features_r"
CREATE TABLE IF NOT EXISTS song_features_r (
    index SERIAL,
    name VARCHAR(50) NOT NULL,
    uri VARCHAR(50) NOT NULL,
    acousticness DOUBLE PRECISION NOT NULL,
    danceability DOUBLE PRECISION NOT NULL,
    energy DOUBLE PRECISION NOT NULL,
    instrumentalness DOUBLE PRECISION NOT NULL,
    key DOUBLE PRECISION NOT NULL,
    liveness DOUBLE PRECISION NOT NULL,
    loudness DOUBLE PRECISION NOT NULL,
    mode DOUBLE PRECISION NOT NULL,
    speechiness DOUBLE PRECISION NOT NULL,
    tempo DOUBLE PRECISION NOT NULL,
    time_signature DOUBLE PRECISION NOT NULL,
    valence DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (index)
);

--create table named "song features_y"
CREATE TABLE IF NOT EXISTS song_features_y (
    index SERIAL,
    name VARCHAR(50) NOT NULL,
    uri VARCHAR(50) NOT NULL,
    acousticness DOUBLE PRECISION NOT NULL,
    danceability DOUBLE PRECISION NOT NULL,
    energy DOUBLE PRECISION NOT NULL,
    instrumentalness DOUBLE PRECISION NOT NULL,
    key DOUBLE PRECISION NOT NULL,
    liveness DOUBLE PRECISION NOT NULL,
    loudness DOUBLE PRECISION NOT NULL,
    mode DOUBLE PRECISION NOT NULL,
    speechiness DOUBLE PRECISION NOT NULL,
    tempo DOUBLE PRECISION NOT NULL,
    time_signature DOUBLE PRECISION NOT NULL,
    valence DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (index)
);

--create table named "playlist_r"
CREATE TABLE IF NOT EXISTS playlist_r (
    index SERIAL,
    name VARCHAR(50) NOT NULL,
    uri VARCHAR(50) NOT NULL,
    PRIMARY KEY (index)
);

--create table named "playlist_y"
CREATE TABLE IF NOT EXISTS playlist_y (
    index SERIAL,
    name VARCHAR(50) NOT NULL,
    uri VARCHAR(50) NOT NULL,
    PRIMARY KEY (index)
);

--create table named "recommended_r"
--this table is used for putting recommended_song made by RecommendAI
CREATE TABLE IF NOT EXISTS recommended_r (
    index SERIAL,
    name VARCHAR(50) NOT NULL,
    uri VARCHAR(50) NOT NULL,
    evaluation INTEGER NOT NULL,
    PRIMARY KEY (index)
);

--create table named "recommended_y"
--this table is used for putting recommended_song made by RecommendAI
CREATE TABLE IF NOT EXISTS recommended_y (
    index SERIAL,
    name VARCHAR(50) NOT NULL,
    uri VARCHAR(50) NOT NULL,
    evaluation INTEGER NOT NULL,
    PRIMARY KEY (index)
);

--create table named "random_selected"
--this table will be read by RecommendAI only
CREATE TABLE IF NOT EXISTS random_selected (
    index SERIAL,
    name VARCHAR(50) NOT NULL,
    uri VARCHAR(50) NOT NULL,
    acousticness DOUBLE PRECISION NOT NULL,
    danceability DOUBLE PRECISION NOT NULL,
    energy DOUBLE PRECISION NOT NULL,
    instrumentalness DOUBLE PRECISION NOT NULL,
    key DOUBLE PRECISION NOT NULL,
    liveness DOUBLE PRECISION NOT NULL,
    loudness DOUBLE PRECISION NOT NULL,
    mode DOUBLE PRECISION NOT NULL,
    speechiness DOUBLE PRECISION NOT NULL,
    tempo DOUBLE PRECISION NOT NULL,
    time_signature DOUBLE PRECISION NOT NULL,
    valence DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (index)
);