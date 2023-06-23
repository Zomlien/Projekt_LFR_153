from rich.console import Console
from zoo.zooApp import zooApp
from rich.table import Table

console = Console()

class ZooInput:
    def __init__(self, configfile, section):
        self.dao = zooApp(configfile, section)
        self.dao.connect()
        self.dao.create_tables()
    
     
    def __repr__(self):
        return ""


    # validation
    def get_valid_input(self, prompt, data_type):
        while True:
            value = input(prompt)
            if len(value.strip()) > 0:
                try:
                    if data_type == str:
                        return str(value)
                    elif data_type == int:
                        return int(value)
                    # If the data type is not supported
                    print("Error: Invalid data type. Please try again.")
                except ValueError:
                    print("Error: Invalid input. Please try again.")
            else:
                print("Error: Input cannot be empty. Please try again.")
    
    # checks input (menu)
    def get_user_choice(self):
        while True:
            choice = input()
            try:
                choice = int(choice)
                return choice
            except ValueError:
                print("Error: Invalid input. Please enter a number.")

    # input menu
    def display_menu(self):
        console.print("[bold magenta]What would you like to do:[/bold magenta]")
        console.print("1. View all enclosures")
        console.print("2. View all categories")
        console.print("3. View all breeds")
        console.print("4. View all keepers")
        console.print("5. View all animals")
        console.print("6. Search for animal by ID")
        console.print("7. Filter animal breeds by their categories")
        console.print("0. Exit")
        console.print("Enter your choice:")


    #enclosures
    def display_enclosures(self):
        enclosures = self.dao.view_all_enclosures()

        if len(enclosures) == 0:
            console.print("No enclosures found.")
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Size")

        for enclosure in enclosures:
            table.add_row(str(enclosure[0]), enclosure[1], str(enclosure[2]))

        console.print(table)

    def display_menu_enclosures(self):
        console.print("[bold magenta]Menu:  Enclosure:[/bold magenta]")
        console.print("1. Create new enclosure")
        console.print("2. Edit enclosure")
        console.print("3. Delete enclosure")
        console.print("0. Back to main menu")
        console.print("Enter your choice:")

    #animalcat
    def display_animalcats(self):
        animalcats = self.dao.view_all_animalcats()

        if len(animalcats) == 0:
            console.print("No animalcats found.")
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("category")

        for animalcat in animalcats:
            table.add_row(str(animalcat[0]), animalcat[1])

        console.print(table)


    def display_menu_animalcats(self):
        console.print("[bold magenta]Menu:  categorie:[/bold magenta]")
        console.print("1. Create new categorie")
        console.print("2. Edit categorie")
        console.print("3. Delete categorie")
        console.print("0. Back to main menu")
        console.print("Enter your choice:")

    #breed
    def display_animalbreed(self):
        animalbreed = self.dao.view_all_animalbreed()

        if len(animalbreed) == 0:
            console.print("No breeds found.")
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Breed")
        table.add_column("Animal cat ID")

        for breed in animalbreed:
            table.add_row(str(breed[0]), breed[1], str(breed[2]))

        console.print(table)


    def display_menu_animalbreed(self):
        console.print("[bold magenta]Menu:  Breeds:[/bold magenta]")
        console.print("1. Create new animal breed")
        console.print("2. Edit animal breed")
        console.print("3. Delete animal breed")
        console.print("0. Back to main menu")
        console.print("Enter your choice:")

    #keeper
    def display_keepers(self):
        keepers = self.dao.view_all_keepers()

        if len(keepers) == 0:
            console.print("No keepers found.")
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Enclosure ID")

        for keeper in keepers:
            table.add_row(str(keeper[0]), keeper[1], str(keeper[2]))

        console.print(table)


    def display_menu_keepers(self):
        console.print("[bold magenta]Menu:  Keepers:[/bold magenta]")
        console.print("1. Create new keeper")
        console.print("2. Edit keeper")
        console.print("3. Delete keeper")
        console.print("0. Back to main menu")
        console.print("Enter your choice:")

    #animal
    def display_animals(self):
        animals = self.dao.view_all_animals()

        if len(animals) == 0:
            console.print("No animals found.")
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Birthday")
        table.add_column("Breed ID")
        table.add_column("Enclosure ID")

        for animal in animals:
            table.add_row(str(animal[0]), animal[1], str(animal[2]), str(animal[3]), str(animal[4]))

        console.print(table)


    def display_menu_animals(self):
        console.print("[bold magenta]Menu:  Animals:[/bold magenta]")
        console.print("1. Create new animal")
        console.print("2. Edit animal")
        console.print("3. Delete animal")
        console.print("0. Back to main menu")
        console.print("Enter your choice:")

    #search
    def handle_search(self):
        console.print("Enter the Animal ID to search.")
        keyword = self.get_valid_input("Keyword: ", str)
        results = self.dao.search_animal_name(keyword)

        if len(results) == 0:
            console.print("No matching animals found.")
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Birthday")
        table.add_column("Breed")
        table.add_column("Enclosure")

        for result in results:
            animal_id, name, birthday, breed, enclosure = result
            table.add_row(str(animal_id), name, str(birthday), str(breed), str(enclosure))

        console.print(table)


    #filter
    def handle_filter(self):
        console = Console()
        console.print("Enter animal category name to filter by.")
        category_name = input("Category Name: ")
        breeds = self.dao.filter_breeds_by_category(category_name)

        if len(breeds) == 0:
            console.print("No matching breeds found.")
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Breed")
        table.add_column("Animal Category")

        for breed in breeds:
            breed_id = str(breed[0])
            breed_name = breed[1]
            animal_category = self.dao.get_category_by_name(category_name)  # Assuming you have a method to get the category name

            table.add_row(breed_id, breed_name, animal_category)

        console.print(table)


    #big menu
    def run(self):
        print(self.dao)
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            if choice == 1:
                self.display_enclosures()
                self.display_menu_enclosures()
                enclosure_choice = self.get_user_choice()
                
                if enclosure_choice == 1:
                    name = self.get_valid_input("Enter the name of the enclosure: ", str)
                    size = self.get_valid_input("Enter the size in m2 of the enclosure: ", int)
                    self.dao.add_enclosure(name, size)
                    
                elif enclosure_choice == 2:
                    enclosure_id = self.get_valid_input("Enter the ID of the enclosure to edit: ", int)
                    name = self.get_valid_input("Enter the new name of the enclosure: ", str)
                    size = self.get_valid_input("Enter the new size of the enclosure in m2: ", int)
                    self.dao.edit_enclosure(enclosure_id, name, size)
                    
                elif enclosure_choice == 3:
                    enclosure_id = self.get_valid_input("Enter the ID of the enclosure to delete: ", int)
                    self.dao.delete_enclosure(enclosure_id)
                    
                elif enclosure_choice == 0:
                    continue
                    
                else:
                    console.print("Invalid choice. Please try again.")
            if choice == 2:
                self.display_animalcats()
                self.display_menu_animalcats()
                animalcat_choice = self.get_user_choice()
                
                if animalcat_choice == 1:
                    category = self.get_valid_input("Enter the name of the category: ", str)
                    self.dao.add_animalcat(category)
                    
                elif animalcat_choice == 2:
                    animalcat_id = self.get_valid_input("Enter the ID of the category to edit: ", int)
                    category = self.get_valid_input("Enter the new category: ", str)
                    self.dao.edit_animalcat(animalcat_id, category)
                    
                elif animalcat_choice == 3:
                    animalcat_id = self.get_valid_input("Enter the ID of the category to delete: ", int)
                    self.dao.delete_animalcat(animalcat_id)
                    
                elif animalcat_choice == 0:
                    continue
                    
                else:
                    console.print("Invalid choice. Please try again.")
            if choice == 3:
                self.display_animalbreed()
                self.display_menu_animalbreed()
                animalbreed_choice = self.get_user_choice()
                
                if animalbreed_choice == 1:
                    breed = self.get_valid_input("Enter the breed: ", str)
                    animalcat_id = self.get_valid_input("Enter the ID of the associated category: ", int)
                    self.dao.add_animalbreed(breed, animalcat_id)
                    
                elif animalbreed_choice == 2:
                    animalbreed_id = self.get_valid_input("Enter the ID of the breed to edit: ", int)
                    breed = self.get_valid_input("Enter the new breed: ", str)
                    animalcat_id = self.get_valid_input("Enter the new associated Category ID: ", int)
                    self.dao.edit_animalbreed(animalbreed_id, breed, animalcat_id)
                    
                elif animalbreed_choice == 3:
                    animalbreed_id = self.get_valid_input("Enter the ID of the breed to delete: ", int)
                    self.dao.delete_animalbreed(animalbreed_id)
                    
                elif animalbreed_choice == 0:
                    continue
                    
                else:
                    console.print("Invalid choice. Please try again.")
            if choice == 4:
                self.display_keepers()
                self.display_menu_keepers()
                keeper_choice = self.get_user_choice()
                
                if keeper_choice == 1:
                    name = self.get_valid_input("Enter the name of the keeper: ", str)
                    enclosure_id = self.get_valid_input("Enter the ID of the enclosure: ", int)
                    self.dao.add_keeper(name, enclosure_id)
                    
                elif keeper_choice == 2:
                    keeper_id = self.get_valid_input("Enter the ID of the keeper to edit: ", int)
                    name = self.get_valid_input("Enter the new name: ", str)
                    enclosure_id = self.get_valid_input("Enter the new ID of the enclosure: ", int)
                    self.dao.edit_keeper(keeper_id, name, enclosure_id)
                    
                elif keeper_choice == 3:
                    keeper_id = self.get_valid_input("Enter the ID of the keeper to delete: ", int)
                    self.dao.delete_keeper(keeper_id)
                    
                elif keeper_choice == 0:
                    continue       
                else:
                    console.print("Invalid choice. Please try again.")
            if choice == 5:
                self.display_animals()
                self.display_menu_animals()
                animal_choice = self.get_user_choice()
                
                if animal_choice == 1:
                    name = self.get_valid_input("Enter the name of the animal: ", str)
                    birthday = self.get_valid_input("Enter the birthday of the animal (YYYY-MM-DD): ", str)
                    breed_id = self.get_valid_input("Enter the ID of the animal breed: ", int)
                    enclosure_id = self.get_valid_input("Enter the ID of the enclosure: ", int)
                    self.dao.add_animal(name, birthday, breed_id, enclosure_id)
                    
                elif animal_choice == 2:
                    animal_id = self.get_valid_input("Enter the ID of the animal to edit: ", int)
                    name = self.get_valid_input("Enter the new name: ", str)
                    birthday = self.get_valid_input("Enter the new birthday (YYYY-MM-DD): ", str)
                    breed_id = self.get_valid_input("Enter the new ID of the animal breed: ", int)
                    enclosure_id = self.get_valid_input("Enter the new ID of the enclosure: ", int)
                    self.dao.edit_animal(animal_id, name, birthday, breed_id, enclosure_id)
                    
                elif animal_choice == 3:
                    animal_id = self.get_valid_input("Enter the ID of the animal to delete: ", int)
                    self.dao.delete_animal(animal_id)
                    
                elif animal_choice == 0:
                    continue
                else:
                    console.print("Invalid choice. Please try again.")
            elif choice == 6:
                self.handle_search()
            elif choice == 7:
                self.handle_filter()
            elif choice == 0:
                console.print('🐊See you later alligator🐊')
                break
            else:
                console.print("...")

    

