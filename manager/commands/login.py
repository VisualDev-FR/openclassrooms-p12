import os


def execute(*args):

    email = args[0]
    password = args[1]


if __name__ == "__main__":
    password = os.environ.get("EPICEVENTS_PW")

    print(password)
