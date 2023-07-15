import click  # ? click library to manage the CLI commands
import db_manager  # ? to manage the database
import pandas as pd  # ? to create dataframes

# ? This script provides a command-line interface (CLI) for managing users, pets, categories, and exports in a database.
# * It utilizes the click library to define and handle CLI commands, and the db_manager module to interact with the database.
# * The script also uses the pandas library to create dataframes for displaying data.

# ! create a group of commands
# ? Command-Line Interface
# * This function serves as the main command-line interface for the program.
# * - It is decorated with `@click.group()` to create a group of commands.
# * - It doesn't have any implementation and simply serves as a placeholder.
# * - Additional commands can be added as subcommands using the `@cli.command()` decorator.
# * - To execute the program, this function needs to be invoked.


@click.group()
def cli():
    pass


# ? get users -command
# * This command retrieves users from the database and displays the information.
# * If no users are found, it prints a message. Otherwise, it  prints the number of users and displays their details in a DataFrame.


@cli.command()
def users():

    users = db_manager.get_users()

    if users == []:
        print("No users found")
        return

    print(f"There are {len(users)} users")
    users_df = pd.DataFrame(
        users, columns=['ID', 'Name', 'Lastname'])
    print(users_df)


# ? newUser - Command
# * This command creates a new user with the provided name and lastname.
# * - If the name or lastname is not provided, it raises an error.
# * - After creating the user, it retrieves the updated list of users.
# * - Finally, it prints the ID of the newly created user.


@cli.command()
@click.option('--name', required=True, help="Name of the user")
@click.option('--lastname', required=True, help="Lastname of the user")
@click.pass_context
def newUser(ctx, name, lastname):

    if not name or not lastname:
        ctx.fail("Name and lastname are required")
    else:
        new_user = {
            "Name": name,
            "Lastname": lastname
        }
        # * create the user
        db_manager.new_user(
            new_user['Name'], new_user['Lastname'])
        data = db_manager.get_users()
        # * get the last ID
        if data == []:
            new_ID = 1
        else:
            new_ID = data[-1][0]
        print(f"User {new_ID} created")


# ? searchUser - Command
# * This command searches for a user with the specified ID in the database.
# * - If the ID is not provided, it raises an error.
# * - It retrieves the list of users from the database.
# * - If no users are found, it prints a message.
# * - If a user with the specified ID is found, it prints their ID, name, and lastname.


@cli.command()
@click.argument('id', type=int)
@click.pass_context
def searchUser(ctx, id):
    if not id:
        ctx.fail("ID is required")
    else:
        data = db_manager.get_users()

        if data == []:
            print("No users found")
            return

        user = next((x for x in data if x[0] == id), None)

        if user is None:
            print("User not found")
        else:
            print(f"User {user[0]} - {user[1]} - {user[2]}")


# ? deleteUser - Command
# * This command deletes a user with the specified ID from the database.
# * - If the ID is not provided, it raises an error.
# * - It retrieves the list of users from the database.
# * - If no users are found, it prints a message.
# * - If a user with the specified ID is found, it deletes the user and prints a confirmation message.


@cli.command()
@click.argument('id', type=int)
@click.pass_context
def deleteUser(ctx, id):
    if not id:
        ctx.fail("ID is required")
    else:

        data = db_manager.get_users()

        if data == []:
            print("No users found")
            return

        user = next((x for x in data if x[0] == id), None)

        if user is None:
            print("User not found")
        else:
            db_manager.delete_user(user[0])
            print(f"User {user[0]} deleted")


# ? updateUser - Command
# * This command updates the information of a user with the specified ID in the database.
# * - The ID is required, and if not provided, it raises an error.
# * - It retrieves the list of users from the database.
# * - If no users are found, it prints a message.
# * - If a user with the specified ID is found, it updates the user's information.
# * - If the name or lastname options are not provided, it uses the existing values.
# * - It prints a confirmation message after updating the user.


@cli.command()
@click.argument('id', type=int)
@click.option('--name', help="Name of the user")
@click.option('--lastname', help="Lastname of the user")
@click.pass_context
def updateUser(ctx, id, name, lastname):
    if not id:
        ctx.fail("ID is required")
    else:

        data = db_manager.get_users()

        if data == []:
            print("No users found")
            return

        user = next((x for x in data if x[0] == id), None)

        if not name:
            name = user[1]
        if not lastname:
            lastname = user[2]

        db_manager.update_user(id, name, lastname)
        print(f"User {id} updated")


# ! pets commands

# ? pets - Command
# * This command retrieves the pets belonging to a user with the specified ID from the database.
# * - The user ID is required, and if not provided, it raises an error.
# * - It retrieves the list of pets for the user from the database.
# * - It retrieves the list of users from the database.
# * - If no users are found, it prints a message.
# * - If a user with the specified ID is found, it retrieves their name.
# * - If the user is not found, it prints a message.
# * - If the user has no pets, it prints a message indicating that.
# * - If the user has pets, it prints their name and displays their details in a DataFrame.

@cli.command()
@click.argument('id', type=int)
@click.pass_context
def pets(ctx, id):
    if not id:
        ctx.fail("User ID is required")
    else:

        pets = db_manager.user_pets(id)
        user = db_manager.get_users()

        if user == []:
            print("No users found")
            return

        user_name = next((x for x in user if x[0] == id), None)

        if user_name is None:
            print("User not found")
        else:
            if not pets:
                print(f"{user_name[1]} {user_name[2]} has no pets")
                return
            else:
                print(f"Pets of {user_name[1]} {user_name[2]}")
                pets_df = pd.DataFrame(
                    pets, columns=['ID', 'Category', 'Name', 'Sex', 'Age'])
                print(pets_df)


# ? petList - Command
# * This command retrieves all pets from the database and displays the information.
# * - If no pets are found, it prints a message. Otherwise, it prints the number
# * of pets and displays their details, including the category, name, sex, owner, and age,
# * in a DataFrame.

@cli.command()
def petList():

    pets = db_manager.get_pets()

    if pets == []:
        print("No pets found")
        return

    print(f"There are {len(pets)} pets")
    pets_df = pd.DataFrame(
        pets, columns=['ID', 'Category', 'Name',  'Sex', 'Owner', 'Age'])
    print(pets_df)


# ? newPet - Command
# * This command creates a new pet for a user in the database.
# * - It requires the following parameters:
# *   - id: User ID
# *   - category: Category of the pet
# *   - name: Name of the pet
# *   - sex: Sex of the pet
# *   - age: Age of the pet
# * - If any of the required parameters are missing, the command fails with an appropriate error message.
# * - After successfully creating the pet, it retrieves the user's information and prints a message confirming
# *   the creation of the pet for the user.

@cli.command()
@click.argument('id', type=int)
@click.option('--category', type=int, required=True, help="Category of the pet")
@click.option('--name', required=True, help="Name of the pet")
@click.option('--sex', required=True, help="Sex of the pet")
@click.option('--age', required=True, help="Age of the pet")
@click.pass_context
def newPet(ctx, id, category, name, sex, age):

    if not category:
        ctx.fail("Category is required")
    if not name:
        ctx.fail("Name is required")
    if not sex:
        ctx.fail("sex is required")
    if not age:
        ctx.fail("age is required")
    else:

        db_manager.create_pet(id, category, name, sex, age)
        user = db_manager.get_users()

        if user == []:
            print("No users found")
            return

        user_name = next((x for x in user if x[0] == id), None)
        print(f"Pet {name} created for {user_name[1]} {user_name[2]}")


# ? updatePet - Command
# * This command updates the information of a pet in the database.
# * - It requires the following parameters:
# *   - id: Pet ID
# * - It also supports optional parameters to update specific fields of the pet:
# *   - category: Category of the pet
# *   - name: Name of the pet
# *   - sex: Sex of the pet
# *   - owner: Owner of the pet
# *   - age: Age of the pet
# * - If the pet with the given ID is not found, it prints a message indicating that the pet was not found.
# * - If any of the optional parameters are not provided, the existing values of the corresponding fields are retained.
# * - After successfully updating the pet, it prints a message confirming the update.

@cli.command()
@click.argument('id', type=int)
@click.option('--category', type=int,  help="Category of the pet")
@click.option('--name',  help="Name of the pet")
@click.option('--sex',  help="Sex of the pet")
@click.option('--owner',  help="Owner of the pet")
@click.option('--age', help="Age of the pet")
@click.pass_context
def updatePet(ctx, id, category, name, sex, owner, age):

    if not id:
        ctx.fail("Pet ID is required")
    else:

        data = db_manager.get_pet(id)
        pet = data

        if pet == []:
            print("Pet not found")
            return

        if not category:
            category = pet[1]
        if not name:
            name = pet[2]
        if not sex:
            sex = pet[3]
        if not owner:
            owner = pet[4]
        if not age:
            age = pet[5]

        db_manager.update_pet(id, category, name, sex, owner, age)
        print(f"Pet {name} updated")


# ? deletePet - Command
# * This command deletes a pet from the database based on its ID.
# * - It requires the following parameter:
# *   - id: Pet ID
# * - If the ID is not provided, it prints a message indicating that the Pet ID is required.
# * - If the pet with the given ID is not found, it prints a message indicating that the pet was not found.
# * - After successfully deleting the pet, it prints a message confirming the deletion.

@cli.command()
@click.argument('id', type=int)
@click.pass_context
def deletePet(ctx, id):
    if not id:

        ctx.fail("Pet ID is required")
    else:

        data = db_manager.get_pet(id)
        pet = data

        if not pet:
            print("Pet not found")
        else:
            db_manager.delete_pet(id)
            print(f"Pet {pet[2]} deleted")


# ? categorys - Command
# * This command retrieves the list of categories from the database and displays the information.
# * - If no categories are found, it prints a message indicating that no categories were found.
# * - If categories are found, it prints the number of categories and displays their details in a DataFrame.
# * - The DataFrame includes the following columns:
# *   - ID: Category ID
# *   - Category name: Name of the category

@cli.command()
def categorys():

    categorys = db_manager.view_categorys()

    if categorys == []:
        print("No categorys found")
        return

    print(f"There are {len(categorys)} categorys")

    categorys_df = pd.DataFrame(
        categorys, columns=['ID', 'Category name'])
    print(categorys_df)


def get_category(id):

    category = db_manager.get_category(id)

    if category == None:
        return None
    return category[0]


# ? petsCategory - Command
# * This command retrieves the pets belonging to a specific category from the database and displays the information.
# * - It requires the 'id' argument, which represents the Category ID.
# * - If the 'id' argument is not provided, it fails and displays an error message.
# * - If the specified category is not found, it prints a message indicating that the category was not found.
# * - If pets are found in the category, it prints the number of pets and displays their details in a DataFrame.
# * - The DataFrame includes the following columns:
# *   - ID: Pet ID
# *   - Name: Name of the pet
# *   - Sex: Sex of the pet
# *   - Owner: Owner of the pet
# *   - Age: Age of the pet

@cli.command()
@click.argument('id', type=int)
@click.pass_context
def petsCategory(ctx, id):

    if not id:
        ctx.fail("Category ID is required")

    else:

        category = get_category(id)

        if category == None:
            print("Category not found")
            return

        pets = db_manager.category_pets(id)

        print(f"there are {len(pets)} pets in category {category}")

        if pets == []:
            return

        pets_df = pd.DataFrame(
            pets, columns=['ID', 'Name',  'Sex', 'Owner', 'Age'])
        print(pets_df)


# ? newCategory - Command
# * This command creates a new category in the database.
# * - It takes the 'name' option as input, which represents the name of the category.
# * - If the 'name' option is not provided, it prints an error message indicating that the category name is required.
# * - If the 'name' option is provided, it creates a new category with the given name in the database.
# * - After creating the category, it prints a message indicating that the category has been successfully created.

@cli.command()
@click.option('--name', type=str)
def newCategory(name):

    if not name:
        print("Category name is required")
        return

    db_manager.create_category(name)
    print(f"Category {name} created")


# ? deleteCategory - Command
# * This command deletes a category from the database based on the provided category ID.
# * - It takes the 'id' argument as input, which represents the ID of the category to be deleted.
# * - If the 'id' argument is not provided, it prints an error message indicating that the Category ID is required.
# * - If the provided category ID is valid and exists in the database, it deletes the category and prints a success message.
# * - If the provided category ID does not exist in the database, it prints a message indicating that the category was not found.

@cli.command()
@click.argument('id', type=int)
def deleteCategory(id):

    if not id:
        print("Category ID is required")
        return

    category = get_category(id)

    if category == None:
        print("Category not found")
        return

    db_manager.delete_category(id)
    print(f"Category {category} deleted")

# ! exports

# ? exportExcel - Command
# * This command exports the database data to an Excel file.
# * - It calls the 'export_excel' function from 'db_manager' module to perform the export.
# * - After the export is completed, it prints a message indicating that the Excel file has been exported.


@cli.command()
def exportExcel():

    db_manager.export_excel()
    print("Excel exported")


# ? exportPDF - Command
# * This command exports the database data to a PDF file.
# * - It calls the 'export_pdf' function from 'db_manager' module to perform the export.
# * - After the export is completed, it prints a message indicating that the PDF file has been exported.

@cli.command()
def exportPDF():

    db_manager.export_pdf()
    print("PDF exported")

# ! Entry Point
# * This is the entry point of the program.
# * - It first calls the 'create_db' function from 'db_manager' module to create the database if it doesn't exist.
# * - It then calls the 'create_excel' function from 'db_manager' module to create the Excel file if it doesn't exist.
# * - Finally, it invokes the 'cli' command-line interface to start the program.


if __name__ == '__main__':
    db_manager.create_db()
    db_manager.create_excel()
    cli()
