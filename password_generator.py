def generate_password():
    return "".join(
        [
            random.SystemRandom().choice(
                string.digits + string.ascii_letters + string.punctuation
            )
            for i in range(16)
        ]
    )
