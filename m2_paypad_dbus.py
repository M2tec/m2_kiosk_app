

def on_bus_acquired(connection, name):

    """
    The function that introduces our server to the world. It is called automatically
    when we get the bus we asked.
    """

    # Remember the node we made earlier? That has a list as interfaces attribute.
    # From that get our interface. We made only one interface, so we get the first
    # interface.

    print("Bus acquired for name, ", name)
    reg_id = connection.register_object(
        "/org/m2tec/paypad", node.interfaces[0], handle_method_call, None, None
    )


def on_name_acquired(connection, name):

    """
    What to do after name acquired?
    """

    print("Name acquired :", name)


def on_name_lost(connection, name):

    """
    What to do after our name is lost? May be just exit.
    """

    print("Name lost :", name)
    exit(0)