import sqlite3
import uuid
from datetime import datetime, timedelta

def main():
    try:
        conn = sqlite3.connect('tickets.db')
        create_database(conn)

        while True:
            print("\nNova Ticket-System Menü:")
            print("1. Neues Ticket erstellen")
            print("2. Ticket bearbeiten")
            print("3. Ticket anzeigen")
            print("4. Ticket löschen")
            print("5. Tickets suchen")
            print("6. Benutzer Handbuch")
            print("7. Beenden")

            try:
                option = int(input("Wähle eine Option: "))
            except ValueError:
                print("Ungültige Eingabe. Bitte eine Zahl eingeben.")
                continue

            if option == 1:
                create_ticket(conn)
            elif option == 2:
                edit_ticket(conn)
            elif option == 3:
                show_ticket(conn)
            elif option == 4:
                delete_ticket(conn)
            elif option == 5:
                search_tickets(conn)
            elif option == 6:
                show_help()
            elif option == 7:
                print("Programm beendet.")
                conn.close()
                return
            else:
                print("Ungültige Option.")

    except sqlite3.Error as e:
        print(f"Fehler bei der Datenbankverbindung: {e}")


def create_database(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            user_name TEXT NOT NULL,
            problem TEXT NOT NULL,
            priority TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL,
            category TEXT NOT NULL,
            creation_time TEXT NOT NULL
        )
    """)
    conn.commit()


def create_ticket(conn):
    user_name = input("Benutzername: ")
    problem = input("Problem: ")
    priority, due_date = get_priority_and_due_date()
    ticket_id = generate_ticket_id()
    status = "Offen"
    category = get_category()
    creation_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    summary = f"Ticket {ticket_id} für {user_name} mit Priorität {priority} erstellt am {creation_time}. Fälligkeitsdatum: {due_date}, Status: {status}, Kategorie: {category}"
    print(summary)

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tickets (ticket_id, user_name, problem, priority, due_date, status, category, creation_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, user_name, problem, priority, due_date, status, category, creation_time))
    conn.commit()
    print("Ticket erstellt!")


def edit_ticket(conn):
    ticket_id = input("Gib die Ticket-ID ein, die du bearbeiten möchtest: ")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
    ticket = cursor.fetchone()

    if ticket:
        print("\nTicket gefunden:")
        print("Ticket-ID:", ticket[0])
        print("Benutzername:", ticket[1])
        print("Problem:", ticket[2])
        print("Priorität:", ticket[3])
        print("Fälligkeitsdatum:", ticket[4])
        print("Status:", ticket[5])
        print("Kategorie:", ticket[6])
        print("Erstellungszeit:", ticket[7])

        new_user_name = input("Neuer Benutzername (leer lassen, um nicht zu ändern): ")
        new_problem = input("Neues Problem (leer lassen, um nicht zu ändern): ")
        new_priority = input("Neue Priorität (Major, Normal, Minor, leer lassen, um nicht zu ändern): ").lower()
        new_status = input(
            "Neuer Status (Offen, In Bearbeitung, Geschlossen, leer lassen, um nicht zu ändern): ").lower()
        new_category = input("Neue Kategorie (Hardware, Software, Netzwerk, leer lassen, um nicht zu ändern): ").lower()

        update_data = []
        if new_user_name:
            update_data.append(("user_name", new_user_name))
        if new_problem:
            update_data.append(("problem", new_problem))
        if new_priority:
            new_due_date = calculate_due_date(new_priority)
            update_data.append(("priority", new_priority))
            update_data.append(("due_date", new_due_date))
        if new_status:
            update_data.append(("status", new_status))
        if new_category:
            update_data.append(("category", new_category))

        if update_data:
            set_clause = ", ".join([f"{key} = ?" for key, _ in update_data])
            cursor.execute(f"UPDATE tickets SET {set_clause} WHERE ticket_id = ?",
                           [value for _, value in update_data] + [ticket_id])
            conn.commit()
            print("Ticket erfolgreich aktualisiert.")
        else:
            print("Keine Änderungen vorgenommen.")


    else:
        print("Ticket nicht gefunden.")


def show_ticket(conn):
    ticket_id = input("Gib die Ticket-ID ein, die du anzeigen möchtest: ")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
    ticket = cursor.fetchone()

    if ticket:
        print("\nTicket gefunden:")
        print("Ticket-ID:", ticket[0])
        print("Benutzername:", ticket[1])
        print("Problem:", ticket[2])
        print("Priorität:", ticket[3])
        print("Fälligkeitsdatum:", ticket[4])
        print("Status:", ticket[5])
        print("Kategorie:", ticket[6])
        print("Erstellungszeit:", ticket[7])
    else:
        print("Ticket nicht gefunden.")


def delete_ticket(conn):
    ticket_id = input("Gib die Ticket-ID ein, die du löschen möchtest: ")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print("Ticket erfolgreich gelöscht.")
    else:
        print("Ticket nicht gefunden.")


def search_tickets(conn):
    print("\nSuchkriterien:")
    user_name = input("Benutzername (leer lassen, um nicht zu filtern): ")
    problem = input("Problem (leer lassen, um nicht zu filtern): ")
    priority = input("Priorität (Major, Normal, Minor, leer lassen, um nicht zu filtern): ").lower()
    status = input("Status (Offen, In Bearbeitung, Geschlossen, leer lassen, um nicht zu filtern): ").lower()
    category = input("Kategorie (Hardware, Software, Netzwerk, leer lassen, um nicht zu filtern): ").lower()

    cursor = conn.cursor()
    query = "SELECT * FROM tickets WHERE 1=1"
    params = []

    if user_name:
        query += " AND user_name LIKE ?"
        params.append(f"%{user_name}%")
    if problem:
        query += " AND problem LIKE ?"
        params.append(f"%{problem}%")
    if priority:
        query += " AND priority = ?"
        params.append(priority)
    if status:
        query += " AND status = ?"
        params.append(status)
    if category:
        query += " AND category = ?"
        params.append(category)

    cursor.execute(query, params)
    tickets = cursor.fetchall()

    if tickets:
        for ticket in tickets:
            print("\nTicket gefunden:")
            print("Ticket-ID:", ticket[0])
            print("Benutzername:", ticket[1])
            print("Problem:", ticket[2])
            print("Priorität:", ticket[3])
            print("Fälligkeitsdatum:", ticket[4])
            print("Status:", ticket[5])
            print("Kategorie:", ticket[6])
            print("Erstellungszeit:", ticket[7])
    else:
        print("Keine Tickets gefunden.")

# Priority
def get_priority_and_due_date():
    while True:
        priority = input("Priorität (Major, Normal, Minor): ").lower()
        if priority in ("major", "normal", "minor"):
            now = datetime.now()
        if priority == 'major':
            due_date = now + timedelta(hours=1)
        elif priority == 'normal':
            due_date = now + timedelta(days=1)
        else:
            due_date = now + timedelta(days=3)
        return priority, due_date.strftime("%Y-%m-%d %H:%M")

def generate_ticket_id():
    return str(uuid.uuid4())

def get_category():
    while True:
        category = input("Kategorie (Hardware, Software, Netzwerk): ").lower()
        if category in ("hardware", "software", "netzwerk"):
            return category
        else:
            print("Ungültige Kategorie. Bitte wähle Hardware, Software oder Netzwerk.")

def calculate_due_date(priority):
    now = datetime.now()
    if priority == 'major':
        due_date = now + timedelta(hours=1)
    elif priority == 'normal':
        due_date = now + timedelta(days=1)
    else:
        due_date = now + timedelta(days=3)
    return due_date.strftime("%d-%m-%Y %H:%M")

def show_help():
    print("\nNova Ticket-System Hilfe:")
    print("\nPrioritäten:")
    print("  Major (Hoch): Ein schwerwiegendes Problem, das die Arbeit des Benutzers stark beeinträchtigt und schnellstmöglich gelöst werden muss.")
    print("  Normal (Mittel): Ein Problem, das die Arbeit des Benutzers beeinträchtigt, aber nicht kritisch ist.")
    print("  Minor (Niedrig): Ein kleines Problem oder eine Anfrage, die keine dringende Bearbeitung erfordert.")
    print("\nBearbeitungszeiten:")
    print("  Major: Innerhalb von einer Stunde")
    print("  Normal: Innerhalb von einem Tag")
    print("  Minor: Innerhalb von drei Tagen")

if __name__ == "__main__":
    main()
