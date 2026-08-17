# Not used anywhere
def combine_to_64_bit_array(bit_arrays):
    combined = []
    for bits in bit_arrays.values():
        combined.extend(bits)

    # Ensure the final array is exactly 64 bits
    if len(combined) < 64:
        combined += [0] * (64 - len(combined))  # pad with zeros
    else:
        combined = combined[:64]  # truncate if longer

    return combined

# Used for CSV to regs conversion in csv_utils
def generate_fixed_length_binary_arrays(params):
    bit_arrays = {}
    for key, data in params.items():
        value = data['current']
        bit_len = data['bit_length']
        # Convert to binary, pad with leading 0s to match bit length
        # binary_str = format(value, f'0{bit_len}b')
        # bits = [int(bit) for bit in binary_str]
        # bit_arrays[key] = bits
        binary_str = bin(value)[2:]  # e.g., '101011'
        trimmed_binary = binary_str[-bit_len:].rjust(bit_len, '0')  # pad left if too short
        bits = [int(bit) for bit in trimmed_binary]
        bit_arrays[key] = bits
    return bit_arrays