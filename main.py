from av_by import extract_cars_list as extract_av_cars
from kufar import extract_cars_list as extract_kufar_cars
from csv_convert import to_csv

av_cars = extract_av_cars()
kufar_cars = extract_kufar_cars()
to_csv(av_cars + kufar_cars)
