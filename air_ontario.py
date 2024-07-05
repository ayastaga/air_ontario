# Load up all libraries for this project
import random
import copy
import re
import pyfiglet
import pandas as pd
from datetime import datetime
from datetime import timedelta
from tabulate import tabulate
from randomtimestamp import random_time
from geopy.distance import geodesic as GD

# Load up all files for this project
airline_codes_file = pd.read_csv('canadian_airline_codes.txt', sep=";", header=None)

# Allows us to color customization
    # Note: To write this function, I used the following: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal    
class color:
    # Arrived
    GREEN = '\033[92m'
    # Departed
    BLUE = '\033[94m'
    # Delayed
    ORANGE = '\033[0;33m'
    # Cancelled
    RED = '\033[91m'
    # Bold
    BOLD = '\033[1m'
    END = '\033[0m'
    
# Returns random canadian airline codes
def random_airline_code_generator():
    airline_code = random.choice(list(airline_codes_file[1]))
    flight_num = random.randrange(3000, 5999)
    return f'{airline_code}{flight_num}'

# Returns random ETD (Expected Time of Departure) & ETA (Expected Time of Arrival)
def random_time_generator():    
    return random_time(text=True, pattern="%H:%M")

# Return random airport terminal
def random_terminal_generator():
    terminal = random.randint(1, 3)
    return f'T{terminal}'

# Return random carousel
def random_carousel_generator():
    return random.randint(1, 13)

# Return random gate
def random_gate_generator():
    gate_alpha = random.choice(list(map(chr, range(65, 91))))
    gate_num = random.randint(1, 99)
    return f'{gate_alpha}{gate_num}'

# Return random airplane status
def random_status_generator():
    status = ["Arrived", "Delayed", "Ontime", "Canceled"]
    return random.choice(status)

# Return random airplane seat
def random_seat_generator():
    seat = ['A', 'B', 'C', 'D', 'E', 'F']
    num = list(range(1, 31))
    return f"{random.choice(num)}{random.choice(seat)}"

# Returns all labels bolded
def bold(labels):
    return [color.BOLD + elem + color.END for elem in labels]

# Returns a color coded table
def color_code(cities):
    for i in range(len(cities)):
        city = cities[i]
        if city[-1] == "Arrived":
            cities[i] = [color.BLUE + str(elem) + color.END for elem in city]
        elif city[-1] == "Ontime":
            cities[i] = [color.GREEN + str(elem) + color.END for elem in city]
        elif city[-1] == "Delayed":
            cities[i] = [color.ORANGE + str(elem) + color.END for elem in city]
        else:
            cities[i] = [color.RED + str(elem) + color.END for elem in city]
    return cities

# Draws a horizontal line
def horizontal_line():
    print("-"*82)

# Creates a unique title
def line_title(prompt):
    diff = int((82 - len(prompt) - 2) / 2)
    print("-" * diff + f" {prompt} " + "-" * diff)

# Service cities
cities = [
    ["Regina", "YQR"], 
    ["Thunder Bay", "YQT"], 
    ["Winnipeg", "YWG"], 
    ["Ottawa", "YOW"], 
    ["Yellowknife", "YZF"], 
    ["PEI", "YYG"], 
    ["Halifax", "YHZ"], 
    ["Edmonton", "YEG"], 
    ["Hamilton", "YHM"], 
    ["Montreal", "YUL"], 
    ["Vancouver", "YVR"], 
    ["Calgary", "YYC"]
    ]
# List of valid cities
valid_service_cities = [city[0] for city in cities]

# Air Ontario Display
print("\n")
print(pyfiglet.Figlet(font="slant").renderText(" "*6 + "Air Ontario"))
print(" "*27 + f"{datetime.now()}\n")

# ARRIVALS
arrivals_header = bold(["Destination", "Code", "Flight", "ETA", "Terminal", "Carousel", "Status"])
arrival_cities = copy.deepcopy(cities)
for city in arrival_cities:
    city.extend([
        random_airline_code_generator(),
        random_time_generator(),
        random_terminal_generator(),
        random_carousel_generator(),
        random_status_generator()
    ])
line_title("ARRIVALS")
color_code(arrival_cities)
print(tabulate(arrival_cities, headers=arrivals_header, tablefmt="fancy_grid", 
               numalign="center", stralign="center"))

# DEPARTURE
departure_header = bold(["Destination", "Code", "Flight", "ETD", "Terminal", "Gate No.", "Status"])
departure_cities = copy.deepcopy(cities)
for city in departure_cities:
    city.extend([
        random_airline_code_generator(),
        random_time_generator(),
        random_terminal_generator(),
        random_gate_generator(),
        random_status_generator()
    ])
line_title("DEPARTURES")
color_code(departure_cities)
print(tabulate(departure_cities, headers=departure_header, tablefmt="fancy_grid", 
               numalign="center", stralign="center"))
print()
line_title("Thank you for choosing Air Ontario")

################################################################################

# Validates date input
def validate_date(prompt, starting_date=datetime.now()):
    # Note that since this was out of my scope of knowledge, I used the Datetime documentation & common resources
        # Idea of normalizing: https://stackoverflow.com/questions/61798474/how-to-replace-the-day-in-a-date-with-another-date     
        # Formatting dates using regex: https://docs.python.org/3/howto/regex.html
        # Strptime: https://www.programiz.com/python-programming/datetime/strptime
        # Datetime documentation: https://docs.python.org/3/library/datetime.html 
        
    starting_date = starting_date.replace(hour=0, minute=0, second=0, microsecond=0)
    while True:
        user_input = input(prompt)
        if re.match(r'^\d{2}/\d{2}/\d{2}$', user_input):
            try:
                # Normalization (aka remove the hours, minutes, seconds and microseconds) to ensure they can be compared equally
                input_date = datetime.strptime(user_input, '%m/%d/%y').replace(hour=0, minute=0, second=0, microsecond=0)
                tomorrow = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                
                if input_date < tomorrow:
                    print(color.RED + "You cannot depart before or during the same day as the booking. Please try again." + color.END)
                elif input_date <= starting_date:
                    print(color.RED + "You cannot arrive before or during the same day as the departure date. Please try again."+ color.END)
                else:
                    return user_input
            except ValueError:
                print(color.RED + "The date is not valid. Try again and use the MM/DD/YY format." + color.END)
        else:
            print(color.RED + "Invalid input. Try again and use the MM/DD/YY format." + color.END)

# Validates radio-like options input
def validate_option(prompt, min_option, max_option):
    while True:
        try:
            user_input = int(input(prompt))
            if user_input in range(min_option, max_option + 1):
                return user_input
            else:
                print(color.RED + f"\nInput must be between {min_option} and {max_option} (inclusive). Please try again." + color.END)
        except ValueError:
            print(color.RED + "Invalid input. Try again and input a valid number." + color.END)

# Validates city name by comparing to valid service cities
def validate_city(prompt, duplicate = None):
    while True:
        user_input = input(prompt)
        if user_input.title() in valid_service_cities and user_input != duplicate:
            return user_input
        # Special case for PEI
        elif user_input.title() == 'Pei' or user_input.title() == "Prince Edward Island" and user_input != duplicate:
            return user_input
        else:
            print(color.RED + "\nInvalid input. Try again and input a service city." + color.END)

# Validates whether input is Yes or No
def validate_Y_N(prompt):
    while True:
        user_input = input(prompt)
        if user_input.upper() in ['Y', 'YES', 'N', 'NO']:
            return 'Y'
        else:
            print(color.RED + "\nInvalid input. Try again and input either Y or N." + color.END)

# Booking display
print()
horizontal_line()
line_title("Book your flight")
horizontal_line()

# Retrieves user name
first_name = input("\nWhat is your first name? ")
last_name = input("\nWhat is your last name? ")

# Retrieves type of trip
print("\nWhich type of trip would you like?")
print("\n 1. Round Trip\n 2. One-way")
trip_type = validate_option("\nPlease type 1 or 2: ", 1, 2)

# While loop to reprompt options if the user is not satisfied
option_selected = False
while option_selected == False:
    # -- Provides information on service cities --
    horizontal_line()
    print("\nNote that currently, Air Ontario only operates from the following cities:\n")
    # Prints out all cities for user to see
    for i in range(len(valid_service_cities)):
        print(valid_service_cities[i], end=", ")
        if i == 5:
            print()
    
    # Booking Menu Display
    print("\n")
    line_title("BOOKING MENU")
    
    # -- Gather information from user --
    # Retrieves original city and destination
    origin = validate_city("\nWhere are you headed from? ").upper()
    destination = validate_city("\nWhere are you headed to? ", duplicate = origin).upper()
    
    # Retrieves date of departure and return day (latter is if round-trip is selected)
    departure_date = validate_date("\nWhen would you like to depart? (MM/DD/YY): ")    
    if trip_type == 1:
        departure_date_modified = datetime.strptime(departure_date, '%m/%d/%y')
        return_date = validate_date("\nWhen would you like to return? (MM/DD/YY): ", starting_date = departure_date_modified)

    # -- Calculate cost of trip using distance --
    # Location of each airport; uppercase to accomodate for all cases
    cities_location = {"REGINA": (50.4337, -104.6560),
                    "THUNDER BAY": (48.3720, -89.3121),
                    "WINNIPEG": (49.9097, -97.2364),
                    "OTTAWA": (45.3178, -75.6659),
                    "YELLOWKNIFE": (62.4712, -114.4381),
                    "PEI": (46.2858, -63.1313),
                    "HALIFAX": (44.8875, -63.5075),
                    "EDMONTON": (53.3062, -113.5828),
                    "HAMILTON": (43.1728, -79.9317),
                    "MONTREAL": (45.4657, -73.7455),
                    "VANCOUVER": (49.1934, -123.1751),
                    "CALGARY": (51.1182, -114.0032)}

    # Calculates distance and multiplies by a certain factor
        # Note: I used the Geopy documentation to develop this method
            # I found the method here: https://www.webscale.com/engineering-education/how-to-calculate-distance-between-two-points-using-geopy-in-python/
            # Geopy documentation: https://geopy.readthedocs.io/en/stable/
    economy_ticket_price = format(float(GD(cities_location[origin], cities_location[destination]).km) / 6, ".2f")
    business_ticket_price = format(float(economy_ticket_price) * 3, ".2f")
    first_ticket_price = format(float(economy_ticket_price) * 9, ".2f")
    
    connecting_economy_ticket_price = format(float(economy_ticket_price) * 0.8, ".2f")
    connecting_business_ticket_price = format(float(first_ticket_price) * 0.85, ".2f")
    connecting_first_ticket_price = format(float(first_ticket_price) * 0.9, ".2f")
    
    # -- Organizes and displays data based on trip type -- 
    if trip_type == 1:
        # Since it's a roundtrip, assuming simplest scenario, price stays the same
        economy_ticket_price *= 2
        business_ticket_price *= 2
        first_ticket_price *= 2
        
        # Roundtrip data
        print()
        horizontal_line()
        print(f'\nFor a round trip from {origin} to {destination}:')
        flight_pricing_information = [[origin, "Direct", destination, "Economy", economy_ticket_price],
                    [origin, "Connecting", destination, "Economy", connecting_economy_ticket_price],
                    [origin, "Direct", destination, "Business", business_ticket_price],
                    [origin, "Connecting", destination, "Business", connecting_business_ticket_price],
                    [origin, "Direct", destination, "First", first_ticket_price],
                    [origin, "Connecting", destination, "First", connecting_first_ticket_price]]
    else:  
        # Oneway data
        print("\n")
        horizontal_line()
        print(f'For a oneway trip from {origin} to {destination}:')
        flight_pricing_information = [[origin, "Direct", destination, "Economy", economy_ticket_price],
                    [origin, "Connecting", destination, "Economy", connecting_economy_ticket_price],
                    [origin, "Direct", destination, "Business", business_ticket_price],
                    [origin, "Connecting", destination, "Business", connecting_business_ticket_price],
                    [origin, "Direct", destination, "First", first_ticket_price],
                    [origin, "Connecting", destination, "First", connecting_first_ticket_price]]
    
    # Displays table of costs
    print(tabulate(flight_pricing_information, 
                headers=["Origin", "Type of Stop", "Destination", "Class", "Total Cost"], 
                tablefmt="fancy_grid", numalign="center", stralign="center"))

    # -- Select options to continue to restart --
    print("Select one of the options below:")
    print("\n 1. Purchase ticket\n 2. Return to Menu")
    decision = validate_option("\nPlease type 1 or 2: ", 1, 2)
    
    # -- If user decides to purchase ticket, go through checkout otherwise return menu --
    if decision == 1:
        # -- Gather user information for checkout --
        # Select type of flight package
        print()
        line_title("Select Package")
        print("\nWhich package would you like to select? ")
        print("\n 1. Economy class, direct")
        print(" 2. Economy class, Connecting")
        print(" 3. Business class, direct")
        print(" 4. Business class, Connecting")
        print(" 5. First class, direct")
        print(" 6. First class, Connecting")
        ticket_option = validate_option("\nSelect a number from 1 to 6: ", 1, 6)
        
        # Retrieve chosen class (useful for boarding pass)
        ticket_class = "Economy"
        if ticket_option == 3 or ticket_option == 4:
            ticket_class = "Business"
        elif ticket_option == 5 or ticket_option == 6:
            ticket_class = "First"
        
        # Retrieve chose type of package  (useful for boarding pass)
        package = "Direct"
        if ticket_option == 2 or ticket_option == 4 or ticket_option == 6:
            package = "Connecting"
        
        # Select passenger count
        passenger_count = validate_option("\nHow many passengers are boarding this trip? ", 1, 9)
        
        # Baggage Checking Styling
        print()
        line_title("Baggage Checking")
        
        # -- Bagging Checking section --
        print("\nNote: Certain restrictions on carry-on luggages apply, click below for more information: ")
        print("https://www.aircanada.com/ca/en/aco/home/plan/baggage/carry-on.html ")

        # Choose rewards program
        print("\nList of Rewards programs: Being a rewards program gives you benefits on pricing!")
        print(" 1. Bronze Loyalty Program")
        print(" 2. Silver Loyalty Program")
        print(" 3. Gold Loyalty Program")
        program_choice = validate_option("\nAre you a part of any of the programs listed above? If not, enter 0: ", 0, 3)
        
        # Set of prices based on rewards program chosen & class of flight
        prices = {
            # Loyalty program #: Economy (1st bag, 2nd bag, extra), Business (...), First (...)
            0: [[50, 70, 100, 140], [40, 60, 90, 140], [35, 55, 85, 140]],
            1: [[40, 60, 90, 120], ["Free", 50, 80, 120], ["Free", "Free", 70, 120]],
            2: [["Free", 50, 70, 100], ["Free", "Free", 60, 80], ["Free", "Free", "Free", 70]],
            3: [["Free", "Free", 50, 70], ["Free", "Free", "Free", 70], ["Free", "Free", "Free", "Free"]],
        }

        # -- Calculates & Displays luggage fee --
        # Cost of economy class tickets
        if ticket_class == "Economy":
            luggage_fee = prices[program_choice][0]
        # Cost of business class tickets
        elif ticket_class == "Business":
            luggage_fee = prices[program_choice][1]
        # Cost of first class tickets
        else:
            luggage_fee = prices[program_choice][2]
            
        # Displays luggage cost 
        luggage_header = ["Luggage", "Price"]
        luggage_price = [
            ["1st bag", f"${luggage_fee[0]}"],
            ["2nd bag", f"${luggage_fee[1]}"],
            ["3rd bag", f"${luggage_fee[2]}"],
            ["Extra bags", f"${luggage_fee[3]}"]
        ]
        print()
        print(tabulate(luggage_price, luggage_header, tablefmt="fancy_grid", numalign="center", stralign="center"))
        
        # -- Luggage count and verification --
        # Counts the number of luggage
        luggage_count = validate_option("\nHow many bags are you planning to check in? ", 0, 9)
        # Provides information on the restrictions for luggages + associated costs
        print()
        line_title("Luggage Verification")
        print("\nNote, that the max weight per bag is 23kg (50lbs) & max size limit is 158cm (62in).")
        print("\nIf the bag exceeds the weight by up to 32kg (70lbs) and/or exceeds the max height \nby up to 292cm (115in), a $120 fee will be charged for each penalty on top of the \noriginal cost. Any heavier than this, and the bag will not be allowed on board.\n")
        horizontal_line()

        # Retrieve weight and dimension for checking, then decide the price otherwise reprompt if too much
        luggage_cost = 0 
        for i in range(luggage_count):
            # Do not add anything if "Free" ($0)
            if luggage_count > 3:
                if luggage_fee[3] != "Free":
                    luggage_cost += luggage_fee[3]
            elif luggage_fee[i] != "Free":
                luggage_cost += luggage_fee[i]
            
            # Verify proper input
            luggage_weight = validate_option(f"\nLuggage {i + 1} weight (kg): ", 5, 32)
            luggage_dimensions = validate_option(f"\nLuggage {i + 1} dimensions (cm): ", 50, 292)
            
            # Add additional fee if bag is overweight or oversized
            if luggage_weight > 23:
                luggage_cost += 120
            if luggage_dimensions > 292:
                luggage_cost += 120
            print()

        # -- Calculates cost of flight (grand total) --
        # Calculates all associated costs
        plane_ticket_cost = format(float(flight_pricing_information[ticket_option][-1]) * passenger_count, ".2f")
        carrier_surcharges = 534.02
        subtotal = format(float(plane_ticket_cost) + luggage_cost + carrier_surcharges, ".2f")
        luggage_cost = format(luggage_cost, ".2f")
        
        # Additional taxes and charges
        hst = format(0.13 * float(subtotal), ".2f")
        security_fee = 25.64
        passenger_service_fee = 3.13
        airport_improvement_fee = 35.42
        user_development_fee = 3.27
        grand_total = format(float(subtotal) + float(hst) + security_fee + passenger_service_fee + \
            airport_improvement_fee + user_development_fee, ".2f")
       
        # Change appearance of luggage in table
        if luggage_cost == 0:
            luggage_cost = "None!"
            
        # Displays final cost
        line_title("CHECKOUT")
        checkout_table = [
            ["Base Fare - {passenger_count} passengers", plane_ticket_cost],
            ["Luggage Cost", luggage_cost],
            ["Carrier surcharges", carrier_surcharges],
            ["Aviation Security Fee", security_fee],
            ["Harmonized Sales Tax (HST)", hst],
            ["Passenger Service fee", passenger_service_fee],
            ["Airport Improvement Fee", airport_improvement_fee],
            ["User Development Fee", user_development_fee],
            ["Grand total", grand_total]
        ]
        print(tabulate(checkout_table, tablefmt="fancy_grid", numalign="center"))
        
        # Confirmation to checkout
        checkout_confirmation = validate_Y_N("Would you like to checkout? If not, you will be taken back to the booking menu (Y/N): ")
        
        # Proceed with checkout if yes, otherwise loop again to menu
        if checkout_confirmation == 'Y':
            if trip_type == 1:
                horizontal_line()
                print(color.GREEN + "\nCongratulations!" + color.END + f"You have booked your flight. It is scheduled to depart at {departure_date} and return at {return_date}!")
                option_selected = True
            else:
                horizontal_line()
                print(color.GREEN + "\nCongratulations!" + color.END + f"You have booked your flight. It is scheduled to depart at {departure_date}!")
                option_selected = True
            
            # -- Create a Boarding Pass --
            # Assign random airplane
            col_1 = list(airline_codes_file[0])
            col_2 = list(airline_codes_file[1])
            random_flight_code = random_airline_code_generator()
            random_flight_name = col_1[col_2.index(random_flight_code[:2])]

            # Organize boarding pass information with a header & then display
            boarding_pass_info = [
                [f"{first_name} {last_name}", f"Flight {random_flight_code}", f"Terminal {random_terminal_generator()}"],
                [f"ETD > {random_time_generator()}", f"ETA > {random_time_generator()}", f"Gate {random_gate_generator()}"],
                [f"Leaving {origin}", f"Arriving {destination}", f"Seat No. {random_seat_generator()}"],
                [random_flight_name, "----------->", "||!!||!|||!|"]
            ]
            boarding_pass_headers = ["Boarding Pass", f"{ticket_class} class", f"{package}"]
            print()
            line_title("Boarding Pass")
            print('\n' + tabulate(boarding_pass_info, headers=boarding_pass_headers, tablefmt="rst") + '\n')   
            print(pyfiglet.Figlet(font="slant", width=100).renderText("Safe journey !"))
