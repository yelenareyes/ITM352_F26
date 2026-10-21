import csv

csv_filename = "taxi_1000.csv"
qualifying_trips = []

with open(csv_filename, mode="r", newline="", encoding="utf-8") as csv_file:
    reader = csv.DictReader(csv_file)
    if reader.fieldnames is None:
        raise ValueError(f"{csv_filename} is empty or missing a header row.")
    if "Fare" not in reader.fieldnames or "Trip Miles" not in reader.fieldnames:
        raise ValueError("CSV must contain 'Fare' and 'Trip Miles' columns.")

    for row in reader:
        fare = float(row["Fare"])
        if fare > 10:
            qualifying_trips.append(
                {"fare": fare, "trip_miles": float(row["Trip Miles"])}
            )

if not qualifying_trips:
    raise ValueError(f"{csv_filename} has no trips with fares greater than $10.")

fares = [trip["fare"] for trip in qualifying_trips]
trip_miles = [trip["trip_miles"] for trip in qualifying_trips]

print(f"Trips with fares greater than $10: {len(qualifying_trips)}")
print(f"Total fares: ${sum(fares):,.2f}")
print(f"Average fare: ${sum(fares) / len(fares):,.2f}")
print(f"Maximum trip distance: {max(trip_miles):,.2f} miles")
