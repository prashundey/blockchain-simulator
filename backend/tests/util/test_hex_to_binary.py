from backend.util.hex_to_binary import hex_to_binary

def test_hex_to_binary():
    num = 123
    hex_num = hex(num)[2:]
    bin_num = hex_to_binary(hex_num)
    assert num == int(bin_num, 2)
