
pt = [
    {
        "pattern": r"authentication failure; logname=(\w+) uid=(\d+) euid=(\d+) tty=(\S+) ruser=(\w+) rhost=(\S*) user=(\w+)",
        "template": "An authentication attempt failed, involving the user '{!1!}' with User ID {!2!} attempting to gain elevated privileges (Effective User ID {!3!}) through the terminal '{!4!}' while originating from the remote user '{!5!}'{!6!}, with the attempted username '{!7!}'."
    }
]