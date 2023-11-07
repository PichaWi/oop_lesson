import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cities = []
with open(os.path.join(__location__, 'Cities.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        cities.append(dict(r))

countries = []
with open(os.path.join(__location__, 'Countries.csv')) as f:
    rows = csv.DictReader(f)
    for r in rows:
        countries.append(dict(r))


class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None


import copy


class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table

    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            temps.append(float(item1[aggregation_key]))
        return function(temps)

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def __str__(self):
        return self.table_name + ':' + str(self.table)


table1 = Table('cities', cities)
table2 = Table('countries', countries)
my_DB = DB()
my_DB.insert(table1)
my_DB.insert(table2)
my_table1 = my_DB.search('cities')
my_table1_filtered = my_table1.filter(lambda x: x['country'] == 'Italy')
my_table1_selected = my_table1.select(['city', 'latitude'])
print(my_table1)
print()
print(my_table1_selected)

temps = []
for item in my_table1_filtered.table:
    temps.append(float(item['temperature']))
print(sum(temps) / len(temps))
print("Using aggregation")
print(my_table1_filtered.aggregate(lambda x: sum(x) / len(x), 'temperature'))

print()
my_table2 = my_DB.search('countries')
my_table3 = my_table1.join(my_table2, 'country')
my_table3_filtered = my_table3.filter(lambda x: x['EU'] == 'no').filter(lambda x: float(x['temperature']) < 5.0)
print(my_table3_filtered.table)

print(" ")
eu_cities_no_coastline = my_table3.filter(lambda x: x['EU'] == 'yes' and x['coastline'] == 'no').table
min_temp = min(float(city['temperature']) for city in eu_cities_no_coastline)
max_temp = max(float(city['temperature']) for city in eu_cities_no_coastline)
print("Min temperature:", min_temp)
print("Max temperature:", max_temp)
print(" ")

country_latitudes = {}

for city in my_table1.table:
    country = city['country']
    latitude = float(city['latitude'])

    if country not in country_latitudes:
        country_latitudes[country] = {'min_latitude': latitude, 'max_latitude': latitude}
    else:
        if latitude < country_latitudes[country]['min_latitude']:
            country_latitudes[country]['min_latitude'] = latitude
        if latitude > country_latitudes[country]['max_latitude']:
            country_latitudes[country]['max_latitude'] = latitude

for country, latitudes in country_latitudes.items():
    print(f"Country: {country}")
    print(f"Min Latitude: {latitudes['min_latitude']}")
    print(f"Max Latitude: {latitudes['max_latitude']}")