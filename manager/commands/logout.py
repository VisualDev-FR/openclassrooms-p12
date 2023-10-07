from authentification.login import logout


def execute(*args):
    """
    Entry point for Logout feature.\n
    Deletes the token stored on the user's disk.
    """
    logout()


if __name__ == "__main__":
    execute()
