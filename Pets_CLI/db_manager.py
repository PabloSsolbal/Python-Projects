from openpyxl import Workbook, load_workbook
import pandas as pd
import sqlite3 as sql
import os

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


def get_users():
    if os.path.exists("data.db"):
        with sql.connect("data.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Users")
            data = cur.fetchall()
            return data
    else:
        print("connection failed")


def new_user(ID, Name, Lastname):
    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO Users VALUES ({ID},'{Name}','{Lastname}')")
        con.commit()


def delete_user(ID):
    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM Users WHERE UserID={ID}")


def update_user(ID, Name, Lastname):
    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(
            f"UPDATE Users SET Name='{Name}', Lastname='{Lastname}' WHERE UserID={ID}")


def user_pets(userID):
    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(
            f"""
            SELECT p.PetID, c.Name AS Category, p.Name, p.Sex, p.Age FROM Pets AS p
            Join Categorys As c On p.CategoryID = c.CategoryID
            WHERE p.UserID = {userID}
            """)
        if cur.rowcount == 0:
            return None
        data = cur.fetchall()
        return data


def get_pets():
    if os.path.exists("data.db"):
        with sql.connect("data.db") as con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT p.PetID, c.Name AS Category, p.Name, p.Sex,u.Name AS Owner, p.Age FROM Pets AS p
                Join Categorys As c On p.CategoryID = c.CategoryID
                Join Users AS u On p.UserID = u.UserID
                """
            )
            data = cur.fetchall()
            return data
    else:
        print("connection failed")


def get_pet(id):
    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(
            f"SELECT * FROM Pets WHERE PetID='{id}'")
        if cur.rowcount == 0:
            return None
        data = cur.fetchone()
        return data


def update_pet(petID, Category, Name, Sex, Owner, Age):
    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(
            f"UPDATE Pets Set CategoryID={Category}, Name='{Name}', Sex='{Sex}',UserID={Owner}, Age={Age} WHERE PetID='{petID}'")


def create_pet(userID, categoryID, name, sex, age):
    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(
            f"INSERT INTO Pets (UserID, CategoryID, Name, Sex, Age) VALUES ({userID}, {categoryID}, '{name}', '{sex}', {age})")
        con.commit()


def delete_pet(id):
    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(
            f"DELETE FROM Pets WHERE PetID={id}")


def view_categorys():
    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(
            """
            SELECT * FROM Categorys
            """
        )
        data = cur.fetchall()
        return data


def category_pets(categoryID):
    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(
            f"""SELECT p.PetID, p.Name, p.Sex,u.Name AS Owner, p.Age FROM Pets AS p
            Join Users AS u On p.UserID = u.UserID
            WHERE p.CategoryID={categoryID}
            """)
        if cur.rowcount == 0:
            return None
        data = cur.fetchall()
        return data


def get_category(id):
    with sql.connect("data.db") as con:
        cur = con.cursor()
        cur.execute(
            f"SELECT Name FROM Categorys WHERE CategoryID={id}")
        if cur.rowcount == 0:
            return None
        data = cur.fetchone()
        return data


def export_excel():
    with sql.connect('data.db') as conn:
        # Cargar el archivo Excel existente
        book = load_workbook('data.xlsx')

        # Crear el objeto ExcelWriter y adjuntar el archivo Excel existente
        writer = pd.ExcelWriter('data.xlsx', engine='openpyxl')
        writer.book = book

        # Leer la tabla de usuarios y guardarla en una hoja llamada 'Usuarios'
        users_df = pd.read_sql_query("SELECT * FROM Users", conn)
        users_df.to_excel(writer, sheet_name='Users', index=False)

        # Leer la tabla de mascotas y guardarla en una hoja llamada 'Mascotas'
        pets_df = pd.read_sql_query("SELECT * FROM Pets", conn)
        pets_df.to_excel(writer, sheet_name='Pets', index=False)

        # Leer la tabla de categorias y guardarla en una hoja llamada 'Categorias'
        categories_df = pd.read_sql_query("SELECT * FROM Categorys", conn)
        categories_df.to_excel(writer, sheet_name='Categories', index=False)

        # Guardar los cambios en el archivo Excel
        writer.save()


def export_pdf():
    with sql.connect('data.db') as conn:
        users = pd.read_sql_query("SELECT * FROM Users", conn)
        pets = pd.read_sql_query("""
                SELECT p.PetID, c.Name AS Category, p.Name, p.Sex,u.Name AS Owner, p.Age FROM Pets AS p
                Join Categorys As c On p.CategoryID = c.CategoryID
                Join Users AS u On p.UserID = u.UserID
                """, conn)
        categorys = pd.read_sql_query("SELECT * FROM Categorys", conn)
        dataframes = [users, pets, categorys]
        pdf_filename = "tables.pdf"
        pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)

        table_list = []

        for df in dataframes:
            table_data = [df.columns.tolist()]+df.values.tolist()
            table = Table(table_data)

            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            table_list.append(table)

        pdf.build(table_list)
