--  1. Average price by neighborhood group
SELECT neighbourhood_group, AVG(price) AS avg_price
FROM airbnb_final
GROUP BY neighbourhood_group
ORDER BY avg_price DESC;

-- 2. Most expensive listings (Top 10)
SELECT id, name, neighbourhood_group, price, total_cost
FROM airbnb_final
ORDER BY price DESC
OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY;

-- 3. Count listings by room type and group
SELECT room_type, neighbourhood_group, COUNT(*) AS listing_count
FROM airbnb_final
GROUP BY room_type, neighbourhood_group
ORDER BY listing_count DESC;

--4. Listings with more than 500 reviews
SELECT id, name, number_of_reviews
FROM airbnb_final
WHERE number_of_reviews > 500
ORDER BY number_of_reviews DESC;

-- 5. Listings with above-average price in each neighbourhood
SELECT id, name, neighbourhood, price
FROM airbnb_final
WHERE price > (
  SELECT AVG(price)
  FROM airbnb_final
  WHERE airbnb_final.neighbourhood = neighbourhood
);


-- 6. Listings ranked by price within borough (dense rank)
SELECT id, name, neighbourhood_group, price,
       DENSE_RANK() OVER (PARTITION BY neighbourhood_group ORDER BY price DESC) AS price_rank
FROM airbnb_final;

--7. Average reviews per month by room type
SELECT room_type, ROUND(AVG(reviews_per_month), 2) AS avg_reviews
FROM airbnb_final
GROUP BY room_type
ORDER BY avg_reviews DESC;


--  10. Duplicate name check (same name, different host)
SELECT name, COUNT(DISTINCT host_id) AS host_count
FROM airbnb_final
GROUP BY name
HAVING COUNT(DISTINCT host_id) > 1;

-- 11. Price percentile rank by borough using NTILE
SELECT id, name, neighbourhood_group, price,
       NTILE(4) OVER (PARTITION BY neighbourhood_group ORDER BY price) AS price_quartile
FROM airbnb_final;

-- 12 Listings with above-average availability in their borough
SELECT id, name, neighbourhood_group, availability_365
FROM airbnb_final a
WHERE availability_365 > (
  SELECT AVG(availability_365)
  FROM airbnb_final
  WHERE neighbourhood_group = a.neighbourhood_group
);

-- 13. Total listings and average price per neighbourhood (subquery form)
SELECT neighbourhood,
       (SELECT COUNT(*) FROM airbnb_final b WHERE b.neighbourhood = a.neighbourhood) AS total_listings,
       (SELECT AVG(price) FROM airbnb_final b WHERE b.neighbourhood = a.neighbourhood) AS avg_price
FROM airbnb_final a
GROUP BY neighbourhood;

-- 14. Top 3 most expensive listings per room_type
SELECT *
FROM (
  SELECT *, 
         ROW_NUMBER() OVER (PARTITION BY room_type ORDER BY price DESC) AS rn
  FROM airbnb_final
) ranked
WHERE rn <= 3;

-- 15.Listings with review score below borough average
SELECT id, name, review_rate_number, neighbourhood_group
FROM airbnb_final a
WHERE review_rate_number < (
  SELECT AVG(review_rate_number)
  FROM airbnb_final
  WHERE neighbourhood_group = a.neighbourhood_group
);

-- 16.Neighbourhoods with highest price variability
SELECT neighbourhood, 
       COUNT(*) AS total_listings,
       ROUND(STDEV(price), 2) AS price_std_dev
FROM airbnb_final
GROUP BY neighbourhood
HAVING COUNT(*) > 5
ORDER BY price_std_dev DESC;

--17. Listings where service fee is more than 20% of price
SELECT id, name, price, service_fee,
       ROUND((service_fee * 1.0 / NULLIF(price, 0)) * 100, 2) AS fee_percent
FROM airbnb_final
WHERE service_fee > 0 AND (service_fee * 1.0 / NULLIF(price, 0)) > 0.2;

--  18. Daily average review frequency by room type (CTE + derived value)
WITH review_stats AS (
  SELECT room_type,
         COUNT(*) AS total_listings,
         SUM(reviews_per_month) AS total_reviews
  FROM airbnb_final
  GROUP BY room_type
)
SELECT room_type,
       total_listings,
       total_reviews,
       ROUND(total_reviews * 30.0 / total_listings, 2) AS avg_daily_reviews
FROM review_stats;

-- 19. Availability tier classification using CASE
SELECT id, name, availability_365,
       CASE
         WHEN availability_365 >= 300 THEN 'Always Available'
         WHEN availability_365 >= 180 THEN 'Frequent'
         WHEN availability_365 >= 60 THEN 'Occasional'
         ELSE 'Rarely Available'
       END AS availability_tier
FROM airbnb_final;

--20.  Suggest an index for fast price filtering (query planning)
SELECT id, name, price, total_cost
FROM airbnb_final
WHERE price BETWEEN 100 AND 300
ORDER BY price;

-- 21.Listings joined with aggregated reviews per neighborhood
SELECT a.id, a.name, a.neighbourhood, a.price, r.avg_reviews
FROM airbnb_final a
JOIN (
    SELECT neighbourhood, ROUND(AVG(reviews_per_month), 2) AS avg_reviews
    FROM airbnb_final
    GROUP BY neighbourhood
) r ON a.neighbourhood = r.neighbourhood
ORDER BY avg_reviews DESC;

--22.  Identify host power users (more than 5 listings)
SELECT host_id, COUNT(*) AS listing_count
FROM airbnb_final
GROUP BY host_id
HAVING COUNT(*) > 5
ORDER BY listing_count DESC;

--23. Listings where price bucket mismatches ranking (detect anomalies)
SELECT id, name, price, price_bucket, price_rank_within_area
FROM airbnb_final
WHERE (price_bucket = 'Luxury' AND price_rank_within_area > 100)
   OR (price_bucket = 'Low' AND price_rank_within_area <= 10);

-- 24. Listings with extreme availability but low reviews
SELECT id, name, availability_365, reviews_per_month
FROM airbnb_final
WHERE availability_365 > 300 AND reviews_per_month < 0.5
ORDER BY availability_365 DESC;

--  25. Rank listings by total cost within room type + borough
SELECT id, name, neighbourhood_group, room_type, total_cost,
       RANK() OVER (PARTITION BY neighbourhood_group, room_type ORDER BY total_cost DESC) AS cost_rank
FROM airbnb_final;

-- 26. Find underpriced listings based on room type and area average
WITH avg_price_rt AS (
  SELECT room_type, neighbourhood_group, AVG(price) AS avg_price
  FROM airbnb_final
  GROUP BY room_type, neighbourhood_group
)
SELECT a.id, a.name, a.room_type, a.neighbourhood_group, a.price, ap.avg_price
FROM airbnb_final a
JOIN avg_price_rt ap
  ON a.room_type = ap.room_type AND a.neighbourhood_group = ap.neighbourhood_group
WHERE a.price < ap.avg_price * 0.75;

--  27. Listings with similar name and lat/long (potential duplicates)

SELECT a.id, b.id AS possible_duplicate, a.name, a.lat, a.long
FROM airbnb_final a
JOIN airbnb_final b
  ON a.name = b.name AND a.id <> b.id
WHERE ABS(a.lat - b.lat) < 0.001 AND ABS(a.long - b.long) < 0.001;

-- 28. High availability & review-rate clusters (ML insight start)
SELECT id, name, room_type, price,
       availability_365_scaled, reviews_per_month_scaled
FROM airbnb_final
WHERE availability_365_scaled > 0.7 AND reviews_per_month_scaled > 0.7
ORDER BY reviews_per_month_scaled DESC;

--  29. Listings with missing or empty house rules
SELECT id, name, house_rules
FROM airbnb_final
WHERE house_rules IS NULL OR LTRIM(RTRIM(house_rules)) = '';

















