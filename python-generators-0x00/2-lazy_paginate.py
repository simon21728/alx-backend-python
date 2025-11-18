#!/usr/bin/python3
import seed

def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database with given page_size and offset.
    Returns a list of rows as dictionaries.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator function that lazily paginates user_data table.
    Fetches the next page only when needed.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
