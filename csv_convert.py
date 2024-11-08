import csv


def to_csv(cars):
    with open('cars.csv', 'w', encoding='UTF-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(cars[0].keys())
        for car in cars:
            writer.writerow(car.values())

