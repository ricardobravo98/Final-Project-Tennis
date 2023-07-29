use sys;

#Create the table
CREATE TABLE IF NOT EXISTS tennis_players (
    ranking INT,
    players VARCHAR(100),
    atp_points INT,
    ages INT,
    turned_pro VARCHAR(10),
    weight VARCHAR(10),
    height VARCHAR(10),
    w_l_year VARCHAR(20),
    w_l_career VARCHAR(20),
    title_year INT,
    title_career INT,
    career_high_date VARCHAR(20),
    career_high_rank INT,
    year_price_money INT,
    career_price_money INT,
    aces INT,
    double_faults INT,
    first_serves INT,
    first_serve_points_won INT,
    second_serve_points_won INT,
    break_points_faced INT,
    break_points_saved INT,
    service_games_played INT,
    service_games_won INT,
    total_service_points_won INT,
    first_serve_return_points_won INT,
    second_serve_return_points_won INT,
    break_points_opportunities INT,
    break_points_converted INT,
    return_games_played INT,
    return_games_won INT,
    return_points_won INT,
    total_points_won INT,
    w_year INT,
    l_year INT,
    w_career INT,
    l_career INT,
    w_l_year_final INT,
    w_l_career_final INT
);

DESCRIBE tennis_players;

# Changing Data Types of columns

UPDATE tennis_players SET Atp_points = REPLACE(Atp_points, ',', '') WHERE Atp_points REGEXP '[^0-9]';

ALTER TABLE tennis_players
MODIFY COLUMN Atp_points INT;


ALTER TABLE tennis_players
MODIFY COLUMN Atp_points INT NULL,
MODIFY COLUMN title_year INT NULL,
MODIFY COLUMN Aces INT NULL,
MODIFY COLUMN `Double Faults` INT NULL,
MODIFY COLUMN `Break Points Faced` INT NULL,
MODIFY COLUMN `Break Points Opportunities` INT NULL,
MODIFY COLUMN `Return Games Played` INT NULL;

Select * from tennis_players
Limit 5;


## We need to Alter the table names because whenever it says year, Sql thinks it´s a function
ALTER TABLE tennis_players
CHANGE COLUMN `W-L Year` w_l_year  VARCHAR(20);

ALTER TABLE tennis_players
CHANGE COLUMN `W-L Year` w_l_year  VARCHAR(20);

ALTER TABLE tennis_players
CHANGE COLUMN `W-L Career` w_l_career VARCHAR(20),
CHANGE COLUMN `Title Year` title_year Int;

## Re RUN
Select * from tennis_players
Limit 5;

#Let´s do some queries on the top servers

#I want to rank the top servers
SELECT
    Players,
    aces,
    (SELECT COUNT(DISTINCT t2.aces) + 1
     FROM tennis_players t2
     WHERE t2.aces > t1.aces) AS Rank_Aces
FROM tennis_players t1
ORDER BY aces DESC
LIMIT 20;






   

