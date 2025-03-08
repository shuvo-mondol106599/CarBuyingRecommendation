Author:Shuvo Mondol
Project:Car Buying
import tkinter as tk
from tkinter import ttk, messagebox
import csv

# Class representing a single car
class Car:
    def __init__(self, model, price, fuel_efficiency, brand, horsepower, safety_rating, color):
        self.model = model
        self.price = float(price)  # Convert price to float for calculations
        self.fuel_efficiency = float(fuel_efficiency)  # Convert fuel efficiency to float
        self.brand = brand
        self.horsepower = int(horsepower)  # Convert horsepower to integer
        self.safety_rating = float(safety_rating)  # Convert safety rating to float
        self.color = color
    
    def __repr__(self):
        return f"{self.model} ({self.brand}) - ${self.price}, {self.fuel_efficiency} MPG, Safety: {self.safety_rating} Stars"

# Class representing the car shop with available cars
class CarShop:
    def __init__(self, filename='cars.csv'):
        self.filename = filename
        self.cars = self.load_cars()
    
    def load_cars(self):
        cars = []
        try:
            with open(self.filename, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip the header row
                for row in reader:
                    if len(row) == 7:  # Ensure proper row format
                        cars.append(Car(*row))
        except FileNotFoundError:
            messagebox.showerror("Error", "Cars data file not found!")
        return cars
    
    def get_available_cars(self):
        return self.cars

# Class representing a car buyer with specific preferences
class CarBuyer:
    def __init__(self, budget, min_fuel_efficiency, brand_preference, min_safety_rating):
        self.budget = budget
        self.min_fuel_efficiency = min_fuel_efficiency
        self.brand_preference = brand_preference.lower()
        self.min_safety_rating = min_safety_rating
    
    def filter_cars(self, cars):
        return [
            car for car in cars
            if car.price <= self.budget
            and car.fuel_efficiency >= self.min_fuel_efficiency
            and (self.brand_preference in car.brand.lower() or self.brand_preference == "")
            and car.safety_rating >= self.min_safety_rating
        ]

# Initialize car shop
car_shop = CarShop()

# GUI Setup
root = tk.Tk()
root.title("Car Buying Recommendation")
root.geometry("850x500")

# Input Frame
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(pady=10)

# Budget Input
tk.Label(input_frame, text="Enter your budget ($):").grid(row=0, column=0, sticky="w")
budget_entry = tk.Entry(input_frame)
budget_entry.grid(row=0, column=1)

# Fuel Efficiency Input
tk.Label(input_frame, text="Minimum Fuel Efficiency (MPG):").grid(row=1, column=0, sticky="w")
fuel_entry = tk.Entry(input_frame)
fuel_entry.grid(row=1, column=1)

# Brand Preference Input
tk.Label(input_frame, text="Preferred Brand (optional):").grid(row=2, column=0, sticky="w")
brand_entry = tk.Entry(input_frame)
brand_entry.grid(row=2, column=1)

# Safety Rating Input
tk.Label(input_frame, text="Minimum Safety Rating (1-5):").grid(row=3, column=0, sticky="w")
safety_entry = tk.Entry(input_frame)
safety_entry.grid(row=3, column=1)

# Results Frame
result_frame = tk.Frame(root, padx=10, pady=10)
result_frame.pack(pady=10)

# Treeview to display car recommendations with scrollbar
tree_frame = tk.Frame(result_frame)
tree_frame.pack()
tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(tree_frame, columns=("Model", "Brand", "Price", "MPG", "Safety"), show="headings", yscrollcommand=tree_scroll.set)
tree.heading("Model", text="Model", command=lambda: sort_tree("Model"))
tree.heading("Brand", text="Brand", command=lambda: sort_tree("Brand"))
tree.heading("Price", text="Price ($)", command=lambda: sort_tree("Price"))
tree.heading("MPG", text="Fuel Efficiency (MPG)", command=lambda: sort_tree("MPG"))
tree.heading("Safety", text="Safety Rating", command=lambda: sort_tree("Safety"))
tree.pack()
tree_scroll.config(command=tree.yview)

# Function to get car recommendations
def get_recommendations():
    try:
        budget = float(budget_entry.get()) if budget_entry.get() else float('inf')
        min_fuel_efficiency = float(fuel_entry.get()) if fuel_entry.get() else 0
        brand_preference = brand_entry.get()
        min_safety_rating = float(safety_entry.get()) if safety_entry.get() else 0
        
        buyer = CarBuyer(budget, min_fuel_efficiency, brand_preference, min_safety_rating)
        recommended_cars = buyer.filter_cars(car_shop.get_available_cars())
        
        tree.delete(*tree.get_children())
        if recommended_cars:
            for car in recommended_cars:
                tree.insert("", tk.END, values=(car.model, car.brand, car.price, car.fuel_efficiency, car.safety_rating))
        else:
            messagebox.showinfo("No Cars Found", "No cars match your criteria.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for budget, fuel efficiency, and safety rating.")

# Function to view all available cars
def view_all_cars():
    tree.delete(*tree.get_children())
    cars = car_shop.get_available_cars()
    if cars:
        for car in cars:
            tree.insert("", tk.END, values=(car.model, car.brand, car.price, car.fuel_efficiency, car.safety_rating))
    else:
        messagebox.showinfo("No Cars Available", "No cars available.")

# Function to sort treeview columns
def sort_tree(col):
    items = [(tree.set(k, col), k) for k in tree.get_children("")]
    items.sort(key=lambda t: float(t[0]) if t[0].replace('.', '', 1).isdigit() else t[0])
    for index, (val, k) in enumerate(items):
        tree.move(k, "", index)

# Buttons Frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Get Recommendations", command=get_recommendations).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="View All Cars", command=view_all_cars).grid(row=0, column=1, padx=5)

# Start GUI event loophttps://open.spotify.com/track/5RdroZJbJzyQiKWBJy3cEO
root.mainloop()
