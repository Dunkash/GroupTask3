def hex_to_rgb(hex_str):
    return int(hex_str[1:3], 16), int(hex_str[3:5], 16), int(hex_str[5:7], 16)


assert hex_to_rgb("#ff0000"), (255, 0, 0)
assert hex_to_rgb("#0a040b"), (10, 4, 11)
assert hex_to_rgb("#fe1000"), (254, 16, 0)
