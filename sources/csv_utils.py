import csv
import sources.binary_utils as binary_utils
from sources.constants import csv_filename

def read_csv(filename):
    parameters = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            param = row['Parameter']
            # default_max = int(row['DefaultMax'])
            default_max = int(row['Value'])
            parameters[param] = {'default': default_max, 'current': 0}
    return parameters

def read_csv_with_bit_length(filename):
    parameters = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            param = row['Parameter']
            default_max = int(row['Value'])
            binary_len = int(row['BinaryLength'])
            parameters[param] = {
                'default': default_max,
                'current': 0,
                'bit_length': binary_len
            }
    return parameters

# def generate_fixed_length_binary_arrays(params):
#     bit_arrays = {}
#     for key, data in params.items():
#         value = data['current']
#         bit_len = data['bit_length']
#         # Convert to binary, pad with leading 0s to match bit length
#         # binary_str = format(value, f'0{bit_len}b')
#         # bits = [int(bit) for bit in binary_str]
#         # bit_arrays[key] = bits
#         binary_str = bin(value)[2:]  # e.g., '101011'
#         trimmed_binary = binary_str[-bit_len:].rjust(bit_len, '0')  # pad left if too short
#         bits = [int(bit) for bit in trimmed_binary]
#         bit_arrays[key] = bits
#     return bit_arrays

def display_parameters(params):
    print("\nCurrent Parameters:")
    for key, val in params.items():
        print(f"  {key}: Current = {val['current']} (Default Max = {val['default']})")
    print()

def update_parameters_manual(params):
    while True:
        display_parameters(params)
        print("Do you want to change any values?")
        print("  1. Yes")
        print("  2. No (Continue with current values and exit)")
        choice = input("Enter your choice (1/2): ")

        if choice == '2':
            break
        elif choice == '1':
            param_names = list(params.keys())
            for idx, name in enumerate(param_names):
                print(f"  {idx + 1}. {name}")
            print(f"  {len(param_names) + 1}. Cancel")

            try:
                selection = int(input("Select a parameter to change: "))
                if 1 <= selection <= len(param_names):
                    selected_param = param_names[selection - 1]
                    new_value = input(f"Enter new value for {selected_param}: ")
                    bounded_value = max(0, min(int(new_value), params[selected_param]['default']))
                    params[selected_param]['current'] = int(bounded_value)
                elif selection == len(param_names) + 1:
                    continue
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("Invalid choice. Try again.")

    print("\nFinal Parameter Values:")
    display_parameters(params)
    return params

# --- Main Program ---
# if __name__ == "__main__":
# filename = 'params.csv'  # Change path if needed
# parameters = read_csv(filename)
# params_updated = update_parameters_manual(parameters)

def csv_reg_value_extraction(print_option, print_regs_start, print_regs_end):
    parameters = read_csv_with_bit_length(csv_filename)

    for param in parameters:
        parameters[param]['current'] = parameters[param]['default']
    updated_params = parameters

    bit_arrays = binary_utils.generate_fixed_length_binary_arrays(updated_params)

    regf2 = bit_arrays['regf2']
    efuse_prog_enable_bits = bit_arrays['efuse_prog_enable']
    efuse_reload_bits = bit_arrays['efuse_reload']
    pwr_5v_enable_bits = bit_arrays['pwr_5v_enable']
    regff = 5*[1] + pwr_5v_enable_bits + efuse_reload_bits + efuse_prog_enable_bits

    regs = [bit_arrays[f'reg0{i}'] for i in range(8)] + [regf2] + [regff]

    if (print_option == 1):
        for i in range(print_regs_start,print_regs_end):
            print(f"{i} = ",regs[i])

    return regs