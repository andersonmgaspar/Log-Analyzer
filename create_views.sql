CREATE OR REPLACE VIEW errorcount AS
SELECT time::date as date, count(time) as totalerrors
FROM log
WHERE status like '%404%'
GROUP BY date;

CREATE OR REPLACE VIEW logcount AS
SELECT time::date as date, count(time) as totalcount
FROM log
GROUP BY date;
