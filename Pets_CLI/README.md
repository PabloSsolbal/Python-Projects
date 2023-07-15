# CLI Application for Users and Pet Management

This CLI application allows you to manage users and their associated pets. It provides commands to perform operations such as creating new users, searching for users, updating user information, deleting users, retrieving user pets, creating new pets, updating pet information, deleting pets, and exporting data to Excel and PDF formats.

## DEMO

You can check the [video demo](https://youtu.be/2S_g0_LQL0Q) of the CLI application.

## Technologies Used

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=py,sqlite" />
  </a>
</p>

## How to Run

1. Ensure you have the necessary modules installed. You can install the required modules by running the following commands:

   ```bash
   pip install click
   pip install pandas
   pip install openpyxl
   pip install sqlite3
   pip install reportlab
   ```

2. Save the code provided in a Python file, e.g., `cli.py`.  
2.1 Is requiered to save the `db_manager.py`.

3. Run the clilication by executing the Python file:

   ```bash
   python cli.py COMMAND [OPTIONS]
   ```

   Replace `COMMAND` with the desired command and provide the required options as necessary.

## Available Commands

- `users`: Get a list of all users.
- `newuser`: Create a new user.
- `searchuser`: Search for a user by ID.
- `deleteuser`: Delete a user by ID.
- `updateuser`: Update user information.
- `pets`: Get a list of pets for a specific user.
- `petlist`: Get a list of all pets.
- `newpet`: Create a new pet for a specific user.
- `updatepet`: Update pet information.
- `deletepet`: Delete a pet by ID.
- `categorys`: Get a list of all categories.
- `petscategory`: Get a list of pets in a specific category.
- `newcategory`: Create a new category.
- `deletecategory`: Delete a category by ID.
- `exportexcel`: Export data to an Excel file.
- `exportpdf`: Export data to a PDF file.

## Usage Examples

- Get a list of all users:

  ```bash
  python cli.py users
  ```

- Create a new user:

  ```bash
  python cli.py newuser --name John --lastname Doe
  ```

- Search for a user by ID:

  ```bash
  python cli.py searchuser 1
  ```

- Delete a user by ID:

  ```bash
  python cli.py deleteuser 1
  ```

- Update user information:

  ```bash
  python cli.py updateuser 1 --name John --lastname Smith
  ```

- Get a list of pets for a specific user:

  ```bash
  python cli.py pets 1
  ```

- Get a list of all pets:

  ```bash
  python cli.py petlist
  ```

- Create a new pet for a specific user:

  ```bash
  python cli.py newpet 1 --category 2 --name Max --sex Male --age 3
  ```

- Update pet information:

  ```bash
  python cli.py updatepet 1 --category 3 --name Charlie
  ```

- Delete a pet by ID:

  ```bash
  python cli.py deletepet 1
  ```

- Get a list of all categories:

  ```bash
  python cli.py categorys
  ```

- Get a list of pets in a specific category:

  ```bash
  python cli.py petscategory 2
  ```

- Create a new category:

  ```bash
  python cli.py newcategory "Dogs"
  ```

- Delete a category by ID:

  ```bash
  python cli.py deletecategory 2
  ```

- Export data to an Excel file:

  ```bash
  python cli.py exportexcel
  ```

- Export data to a PDF file:

  ```bash
  python cli.py exportpdf
  ```

## Contribution

Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request.

## Author

- [Pablo Solbal](https://github.com/pablossolbal)

## License

This project is licensed under the [MIT License](https://www.mit.edu/~amini/LICENSE.md).
