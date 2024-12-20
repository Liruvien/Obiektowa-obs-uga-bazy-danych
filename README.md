Warsztat – Obiektowa Obsługa Bazy Danych

W tym warsztacie stworzymy dwie klasy: User i Message, które będą obsługiwały użytkowników i wiadomości w systemie. Będą one zawierały atrybuty, metody do interakcji z bazą danych, oraz umożliwią wykonywanie podstawowych operacji takich jak zapis, odczyt, aktualizacja i usuwanie danych.
Klasa User

Klasa User obsługuje użytkownika systemu. Posiada następujące atrybuty i metody:
Atrybuty:

    _id: Unikalny identyfikator użytkownika, ustawiony na -1 podczas tworzenia obiektu.
    username: Nazwa użytkownika.
    _hashed_password: Zahaszowane hasło użytkownika.

Właściwości:

    id: Zwraca unikalny identyfikator użytkownika (odczyt).
    hashed_password: Zwraca zahaszowane hasło użytkownika (odczyt).

Metody:

    set_password(self, password, salt=""): Ustawia nowe hasło dla użytkownika, haszując je przy użyciu funkcji hash_password.
    hashed_password(self): Setter, który umożliwia ustawienie nowego hasła.
    save_to_db(self, cursor): Zapisuje użytkownika do bazy danych, aktualizując dane, jeśli użytkownik już istnieje lub dodając nowego, jeśli jest to nowy użytkownik.
    load_user_by_username(cursor, username): Ładuje użytkownika z bazy danych na podstawie jego nazwy użytkownika.
    load_user_by_id(cursor, id_): Ładuje użytkownika z bazy danych na podstawie jego identyfikatora.
    load_all_users(cursor): Ładuje wszystkich użytkowników z bazy danych.
    delete(self, cursor): Usuwa użytkownika z bazy danych, ustawiając jego _id na -1.

Klasa Message

Klasa Message obsługuje wiadomości między użytkownikami. Posiada następujące atrybuty i metody:
Atrybuty:

    _id: Unikalny identyfikator wiadomości, ustawiony na -1 podczas tworzenia obiektu.
    from_id: Identyfikator nadawcy wiadomości.
    to_id: Identyfikator odbiorcy wiadomości.
    text: Treść wiadomości.
    _creation_date: Data utworzenia wiadomości, początkowo ustawiona na None, zmienia się przy zapisie do bazy danych.

Właściwości:

    id: Zwraca unikalny identyfikator wiadomości (odczyt).
    creation_date: Zwraca datę utworzenia wiadomości.

Metody:

    save_to_db(self, cursor): Zapisuje wiadomość do bazy danych. Jeśli wiadomość już istnieje, aktualizuje jej dane.
    load_all_messages(cursor, user_id=None): Ładuje wszystkie wiadomości lub wiadomości dla konkretnego użytkownika, jeśli user_id jest podane.

Instrukcje Instalacji

    Zainstaluj wymagane pakiety:

    Jeśli używasz menedżera pakietów pip, upewnij się, że masz zainstalowany clcrypto, który jest wykorzystywany do haszowania haseł. Możesz zainstalować go, uruchamiając poniższe polecenie:

pip install clcrypto

Połączenie z bazą danych:

W kodzie wykorzystujemy cursor do komunikacji z bazą danych. Upewnij się, że masz połączenie z odpowiednią bazą danych i używasz odpowiedniego sterownika bazy danych (np. psycopg2 dla PostgreSQL).

Wykorzystanie klas:

Po utworzeniu instancji klasy User lub Message, możesz korzystać z metod do zapisywania, odczytywania i usuwania danych w bazie. Poniżej znajduje się przykład wykorzystania tych klas:

# Tworzenie nowego użytkownika
user = User(username="john_doe", password="password123", salt="random_salt")
user.save_to_db(cursor)

# Wczytanie użytkownika z bazy po nazwie użytkownika
loaded_user = User.load_user_by_username(cursor, "john_doe")

# Tworzenie wiadomości
message = Message(from_id=1, to_id=2, text="Hello!")
message.save_to_db(cursor)

# Wczytanie wszystkich wiadomości
messages = Message.load_all_messages(cursor)
