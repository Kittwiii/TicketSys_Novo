# Novo Ticket-System (Educational Purpose Only)

This is a simple ticket management system built using Python and SQLite.  **This project is for educational purposes only and should not be used in a production environment.**  It demonstrates basic database interactions and command-line menu functionality.

## Features

*   Create new tickets with user name, problem description, priority, category.
*   Edit existing tickets (user name, problem, priority, status, category).
*   View ticket details.
*   Delete tickets.
*   Search tickets by user name, problem, priority, status, or category.
*   Help menu with information about priorities and processing times.

## How to Run

1.  Make sure you have Python 3 installed.
2.  Save the code as a `.py` file (e.g., `ticket_system.py`).
3.  Open a terminal or command prompt.
4.  Navigate to the directory where you saved the file.
5.  Run the application using: `python ticket_system.py`

## Usage

The application presents a menu with the following options:

1.  **Neues Ticket erstellen:** Creates a new ticket. You'll be prompted to enter user name, problem description, priority (Major, Normal, Minor), and category (Hardware, Software, Netzwerk). Due dates are automatically calculated based on the priority.
2.  **Ticket bearbeiten:** Edits an existing ticket. You'll need to enter the ticket ID. You can then modify the user name, problem, priority, status (Offen, In Bearbeitung, Geschlossen), and category.
3.  **Ticket anzeigen:** Displays the details of a specific ticket. You'll need to enter the ticket ID.
4.  **Ticket löschen:** Deletes a ticket. You'll need to enter the ticket ID.
5.  **Tickets suchen:** Searches for tickets based on various criteria (user name, problem, priority, status, category).  You can leave fields blank to skip filtering.
6.  **Benutzer Handbuch:** Displays the help menu with information about priorities and processing times.
7.  **Beenden:** Exits the application.

## Code Explanation

*   **`main()`:**  Handles the main program loop, displays the menu, and calls the appropriate functions based on user input.  Includes error handling for database connections and invalid input.
*   **`create_database()`:** Creates the `tickets` table in the `tickets.db` database if it doesn't exist.
*   **`create_ticket()`:** Creates a new ticket, generates a unique ticket ID using `uuid`, gets priority and due date, and inserts the ticket data into the database.
*   **`edit_ticket()`:** Allows editing of existing tickets. Retrieves the ticket information, prompts the user for updates, and updates the database.
*   **`show_ticket()`:** Displays the details of a specific ticket.
*   **`delete_ticket()`:** Deletes a ticket from the database.
*   **`search_tickets()`:** Searches for tickets based on user-provided criteria. Uses parameterized queries to prevent SQL injection vulnerabilities (important, even for educational projects).
*   **`get_priority_and_due_date()`:** Gets the ticket priority and calculates the due date based on the priority.
*   **`generate_ticket_id()`:** Generates a unique ticket ID using `uuid`.
*   **`get_category()`:** Gets the ticket category from the user.
*   **`calculate_due_date()`:** Calculates the due date based on the priority.
*   **`show_help()`:** Displays the help information.

## Disclaimer

**This code is for educational purposes only.**  It is not suitable for production use due to its simplicity and lack of robust error handling and security measures.  Specifically:

*   **Security:** While parameterized queries are used in the search function, other parts of the code might be vulnerable to SQL injection if user input is not properly sanitized.  In a real-world application, all user input should be carefully validated and sanitized before being used in database queries.
*   **Error Handling:** The error handling is basic.  A production system would require more comprehensive error handling to gracefully handle various unexpected situations.
*   **User Interface:** The command-line interface is very basic. A real-world application would likely use a graphical user interface (GUI).
*   **Concurrency:** This application does not handle concurrent access to the database.  In a multi-user environment, proper locking mechanisms would be required to prevent data corruption.

This example is intended to demonstrate basic database operations with SQLite and Python.  For production applications, consider using a more robust database system and a well-established framework.
