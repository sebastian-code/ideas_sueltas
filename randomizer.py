from secrets import SystemRandom

baloto = [SystemRandom().randint(1, 43) for i in range(SystemRandom().randint(1, 6))]
balota = [SystemRandom().randint(1, 16) for i in range(SystemRandom().randint(1, 6))]
print(f"BALOTO: {baloto}")
print(f"SUPERBALOTA: {balota}")
