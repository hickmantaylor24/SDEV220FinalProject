INSTALLATION

1.	Using the terminal in the directory containing the project enter command pip install -r requirements.txt
   
STARTING UP

1.	In the terminal, enter python manage.py createsuperuser
2.	Follow the prompts in the terminal to create a superuser account. Remember the details because you will need them to use the program.
3.	In the terminal, enter python manage.py runserver
4.	Use the link in the terminal to open the library application (ctrl+click) 
5.	Log in using the superuser account details you just created.

USING THE PROGRAM

Using the login page, you can log in using any created superuser or staff account.

The manage staff page is accessible via the admin dashboard (home page for superuser accounts) and will allow you to create accounts for staff members. The staff accounts created will have access to all the same functions as the superuser, except for adding and removing other staff members. If you wish for a staff member to have that ability, you can create them a superuser account using python manage.py createsuperuser in the terminal. Regular staff accounts created by the staff account creation form can be deleted on the manage staff page as well.

The manage books page will allow you to add and remove books from the database. This should only be done if a new title is entering or being removed from the library. In the case of additional copies of a book being received, the add a book copy option should be used. If a copy of a book is lost or destroyed, but other copies remain, then use the remove a copy option. 
The manage customers page will allow you to add and remove customers from the database. When new customers wish to check out a book, you can create a customer object for them here. You can also select a customer to remove from the database for whatever reason may occur (death, moving away, banned form the library).

The checkout page will allow you to assign a copy of a book to a customer. This marks the copy as unavailable, and attributes it to that customer so you can track who has what books checked out.

The return page will allow you to unassign a book that is assigned to a customer. This marks the copy returned as available so it can be assigned to other customers. 

