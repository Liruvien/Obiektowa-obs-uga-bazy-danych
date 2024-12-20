from clcrypto import hash_password


class User:
    """
    Represents a User in the system.
    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        hashed_password (str): The hashed password of the user.
    """

    def __init__(self, username="", password="", salt=""):
        """
        Initializes a User instance with the given username, password, and salt.
        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            salt (str): The salt used for hashing the password.
        """
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        """Returns the unique identifier of the user."""
        return self._id

    @property
    def hashed_password(self):
        """Returns the hashed password of the user."""
        return self._hashed_password

    def set_password(self, password, salt=""):
        """
        Sets a new password for the user and hashes it.
        Args:
            password (str): The new password to be set.
            salt (str): The salt used for hashing the password.
        """
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        """
        Sets a new password using the setter method.
        Args:
            password (str): The new password to be set.
        """
        self.set_password(password)

    def save_to_db(self, cursor):
        """
        Saves the user to the database. If the user doesn't exist,
        it inserts a new record; if the user already exists, it updates
        the existing record.
        Args:
            cursor: The database cursor used to execute SQL queries.
        Returns:
            bool: True if the operation is successful.
        """
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                           WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_username(cursor, username):
        """
        Loads a user from the database by the username.
        Args:
            cursor: The database cursor used to execute SQL queries.
            username (str): The username of the user to load.
        Returns:
            User: The loaded User object, or None if the user doesn't exist.
        """
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s"
        cursor.execute(sql, (username,))  # (username, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_user_by_id(cursor, id_):
        """
        Loads a user from the database by the user's ID.
        Args:
            cursor: The database cursor used to execute SQL queries.
            id_ (int): The ID of the user to load.
        Returns:
            User: The loaded User object, or None if the user doesn't exist.
        """
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user

    @staticmethod
    def load_all_users(cursor):
        """
        Loads all users from the database.
        Args:
            cursor: The database cursor used to execute SQL queries.
        Returns:
            list: A list of all User objects.
        """
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete(self, cursor):
        """
        Deletes the user from the database.
        Args:
            cursor: The database cursor used to execute SQL queries.
        Returns:
            bool: True if the deletion is successful.
        """
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True


class Message:
    """
    Represents a Message between users.
    Attributes:
        id (int): The unique identifier of the message.
        from_id (int): The ID of the user who sent the message.
        to_id (int): The ID of the user who receives the message.
        text (str): The content of the message.
        creation_date (datetime): The creation date of the message.
    """

    def __init__(self, from_id, to_id, text):
        """
        Initializes a Message instance with the given from_id, to_id, and text.
        Args:
            from_id (int): The ID of the user who sends the message.
            to_id (int): The ID of the user who receives the message.
            text (str): The content of the message.
        """
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_date = None

    @property
    def creation_date(self):
        """Returns the creation date of the message."""
        return self._creation_date

    @property
    def id(self):
        """Returns the unique identifier of the message."""
        return self._id

    @staticmethod
    def load_all_messages(cursor, user_id=None):
        """
        Loads all messages from the database, optionally filtering by the user ID.
        Args:
            cursor: The database cursor used to execute SQL queries.
            user_id (int, optional): The ID of the user to filter the messages by.
        Returns:
            list: A list of Message objects.
        """
        if user_id:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE to_id=%s"
            cursor.execute(sql, (user_id,))  # (user_id, ) - cause we need a tuple
        else:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages"
            cursor.execute(sql)
        messages = []
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = row
            loaded_message = Message(from_id, to_id, text)
            loaded_message._id = id_
            loaded_message._creation_date = creation_date
            messages.append(loaded_message)
        return messages

    def save_to_db(self, cursor):
        """
        Saves the message to the database. If the message doesn't exist,
        it inserts a new record; if the message already exists, it updates
        the existing record.
        Args:
            cursor: The database cursor used to execute SQL queries.
        Returns:
            bool: True if the operation is successful.
        """
        if self._id == -1:
            sql = """INSERT INTO Messages(from_id, to_id, text)
                            VALUES(%s, %s, %s) RETURNING id, creation_date"""
            values = (self.from_id, self.to_id, self.text)
            cursor.execute(sql, values)
            self._id, self._creation_date = cursor.fetchone()
            return True
        else:
            sql = """UPDATE Messages SET to_id=%s, from_id=%s, text=%s WHERE id=%s"""
            values = (self.self.from_id, self.to_id, self.text, self.id)
            cursor.execute(sql, values)
            return True