import click
import db_manager
import pandas as pd


@click.group()
def cli():
    pass


@cli.command()
def users():
    users = db_manager.get_users()
    print(f"There are {len(users)} users")
    users_df = pd.DataFrame(
        users, columns=['ID', 'Name', 'Lastname'])
    print(users_df)


@cli.command()
@click.option('--name', required=True, help="Name of the user")
@click.option('--lastname', required=True, help="Lastname of the user")
@click.pass_context
def newUser(ctx, name, lastname):
    if not name or not lastname:
        ctx.fail("Name and lastname are required")
    else:
        data = db_manager.get_users()
        new_ID = data[-1][0] + 1
        new_user = {
            "ID": new_ID,
            "Name": name,
            "Lastname": lastname
        }
        db_manager.new_user(
            new_user['ID'], new_user['Name'], new_user['Lastname'])
        print(f"User {new_ID} created")


@cli.command()
@click.argument('id', type=int)
@click.pass_context
def searchUser(ctx, id):
    if not id:
        ctx.fail("ID is required")
    else:
        data = db_manager.get_users()
        user = next((x for x in data if x[0] == id), None)
        if user is None:
            print("User not found")
        else:
            print(f"User {user[0]} - {user[1]} - {user[2]}")


@cli.command()
@click.argument('id', type=int)
@click.pass_context
def deleteUser(ctx, id):
    if not id:
        ctx.fail("ID is required")
    else:
        data = db_manager.get_users()
        user = next((x for x in data if x[0] == id), None)
        if user is None:
            print("User not found")
        else:
            db_manager.delete_user(user[0])
            print(f"User {user[0]} deleted")


@cli.command()
@click.argument('id', type=int)
@click.option('--name', required=True, help="Name of the user")
@click.option('--lastname', required=True, help="Lastname of the user")
@click.pass_context
def updateUser(ctx, id, name, lastname):
    if not id:
        ctx.fail("ID is required")
    else:
        data = db_manager.get_users()
        user = next((x for x in data if x[0] == id), None)
        if not name:
            name = user[1]
        if not lastname:
            lastname = user[2]
        db_manager.update_user(id, name, lastname)
        print(f"User {id} updated")


# pets
@cli.command()
@click.argument('id', type=int)
@click.pass_context
def pets(ctx, id):
    if not id:
        ctx.fail("User ID is required")
    else:
        pets = db_manager.user_pets(id)
        user = db_manager.get_users()
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


@cli.command()
def petList():
    pets = db_manager.get_pets()
    print(f"There are {len(pets)} pets")
    pets_df = pd.DataFrame(
        pets, columns=['ID', 'Category', 'Name',  'Sex', 'Owner', 'Age'])
    print(pets_df)


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
        user_name = next((x for x in user if x[0] == id), None)
        print(f"Pet {name} created for {user_name[1]} {user_name[2]}")


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


@cli.command()
def categorys():
    categorys = db_manager.view_categorys()
    print(f"There are {len(categorys)} categorys")
    categorys_df = pd.DataFrame(
        categorys, columns=['ID', 'Category name'])
    print(categorys_df)


def get_category(id):
    category = db_manager.get_category(id)
    if category == None:
        return None
    return category[0]


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


# exports
@cli.command()
def exportExcel():
    db_manager.export_excel()
    print("Excel exported")


@cli.command()
def exportPDF():
    db_manager.export_pdf()
    print("PDF exported")


if __name__ == '__main__':
    cli()
