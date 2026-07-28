# import pyvisa
import time
from constants import psu_addr, res_connection_delay

def vsense_res_disconnect():

    print("Values have been set")
    # # --- Define settings for each channel ---
    # channel_settings = {
    #     1: {'voltage': 5, 'current': 0.20},
    #     2: {'voltage': 5, 'current': 0.20},
    #     3: {'voltage': 5, 'current': 0.20}
    # }

    # # Connect to the HMC8043 power supply
    # rm = pyvisa.ResourceManager()
    # psu = rm.open_resource(psu_addr)
    # #print("Connected to:", psu.query("*IDN?").strip())

    # # Apply settings to each channel
    # for channel, settings in channel_settings.items():
    #     voltage = settings['voltage']
    #     current = settings['current']
        
    #     psu.write(f"INST:NSEL {channel}")
    #     psu.write(f"VOLT {voltage}")
    #     psu.write(f"CURR {current}")
    #     psu.write("OUTP ON")  # Turn on output for the channel

    #     # print(f"Channel {channel} set to {voltage} V, {current} A")

    time.sleep(res_connection_delay)  # Let outputs stay on for some time (adjust as needed)

    # --- Turn off the master output (disables all channels) ---
    #psu.write("OUTP:MAST OFF")
    #print("Master output turned OFF.")

    # Optional: close connection
    # psu.close()



def vsense_res_connect():
    print("Values have been set")
    # # --- Define settings for each channel ---
    # channel_settings = {
    #     1: {'voltage': 5, 'current': 0.2},
    #     2: {'voltage': 0, 'current': 0.2},  # Use parameter here
    #     3: {'voltage': 5, 'current': 0.2}
    # }

    # # Connect to the HMC8043 power supply
    # rm = pyvisa.ResourceManager()
    # psu = rm.open_resource(psu_addr)
    # # print("Connected to:", psu.query("*IDN?").strip())

    # # Apply settings to each channel
    # for channel, settings in channel_settings.items():
    #     voltage = settings['voltage']
    #     current = settings['current']
        
    #     psu.write(f"INST:NSEL {channel}")
    #     psu.write(f"VOLT {voltage}")
    #     psu.write(f"CURR {current}")
    #     psu.write("OUTP ON")

    #     # print(f"Channel {channel} set to {voltage} V, {current} A")

    time.sleep(res_connection_delay)  # Delay to stabilize output

    # Optional: turn off or close
    # psu.write("OUTP:MAST OFF")
    # psu.close()
