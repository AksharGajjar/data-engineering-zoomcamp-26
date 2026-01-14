# Module 1 Homework

## Question 1: Understanding Docker First Run

**Question:** What's the version of `pip` in the image?

**Answer:** `25.3`

**Steps Taken:**
To find the version, the `python:3.13` image was run with an interactive bash entrypoint.

```console
docker run -it --entrypoint bash python:3.13

root@1bbecfdb127d:/# pip --version
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

## Question 2: Understanding Docker Networking and docker-compose

**Question:** Given the [`docker-compose.yaml`](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/01-docker-terraform/homework.md), what is the hostname and port that pgadmin should use to connect to the postgres database?

**Answer:** `postgres:5432`

* **Hostname (`postgres`):** The [`docker-compose.yaml`](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/01-docker-terraform/homework.md) explicitly sets `container_name: postgres`. This name resolves to the database container.
* **Port (`5432`):** Communication between containers happens on the internal container port (`5432`), not the host port (`5433`).

>[!NOTE]
> For questions 3-6, Data was populated by following the steps outlined in [`docker-sql README.md`](https://github.com/AksharGajjar/data-engineering-zoomcamp-26/tree/module-01-Terraform/01-docker-terraform/docker-sql#readme)

## Question 3: Counting short trips

**Question:** For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a `trip_distance` of less than or equal to 1 mile?

**Answer:** `8007`

**SQL Query:**
```SQL
SELECT count(*) 
FROM green_taxi_data
where lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```

## Question 4. Longest trip for each day

**Question:** Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors). Use the pick up time for your calculations.

**Answer:** `2025-11-14` distance: 88.03 miles

**SQL Query:**
```SQL
SELECT DATE(lpep_pickup_datetime) AS pickup_day, trip_distance AS distance
FROM green_taxi_data
where trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;
```

## Question 5. Biggest pickup zone

**Question:** Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

**Answer:** East Harlem North (total_amount: $6555.32)

**SQL Query:**
```SQL
SELECT zones."Zone", ROUND(SUM("fare_amount")::numeric, 2) AS total_amount
FROM green_taxi_data
LEFT JOIN zones
  ON green_taxi_data."PULocationID" = zones."LocationID"
WHERE lpep_pickup_datetime >= '2025-11-18' 
  AND lpep_pickup_datetime < '2025-11-19'
GROUP BY zones."Zone"
ORDER BY total_amount DESC
LIMIT 1;
```

## Question 6. Largest Tip

**Question:** For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: it's tip , not trip. We need the name of the zone, not the ID.

**Answer:** Yorkville West (tip_amount: $81.89)

**SQL Query:**
```SQL
SELECT 
    pickup_zones."Zone" AS pickup_zone, 
    dropoff_zones."Zone" AS dropoff_zone,
    green_taxi_data.tip_amount
FROM green_taxi_data
JOIN zones AS pickup_zones
  ON green_taxi_data."PULocationID" = pickup_zones."LocationID"
JOIN zones AS dropoff_zones
  ON green_taxi_data."DOLocationID" = dropoff_zones."LocationID"
WHERE 
    green_taxi_data.lpep_pickup_datetime >= '2025-11-01' 
    AND green_taxi_data.lpep_pickup_datetime < '2025-12-01'
    AND pickup_zones."Zone" = 'East Harlem North'
ORDER BY green_taxi_data.tip_amount DESC
LIMIT 1;
```

## Question 7. Terraform Workflow

**Question** Which of the following sequences, respectively, describes the workflow for:

  1. Downloading the provider plugins and setting up backend,
  2. Generating proposed changes and auto-executing the plan
  3. Remove all resources managed by terraform`

**Answer:** terraform init, terraform apply -auto-approve, terraform destroy