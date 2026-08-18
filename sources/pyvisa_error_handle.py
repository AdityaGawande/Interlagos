import time
import pyvisa
import sources.gsheet_util as gsheet_util
from sources.constants import error_handle_retries as retries, error_handle_delay as delay

# Import this as rm. 
# Comment out rm = pyvisa.ResourceManager(). 
# Nothing else changes in the code.

# retries = 50
# delay = 0.1

rm = pyvisa.ResourceManager()

class RetryInstrument:
    # Usage example -
    # afg = RetryInstrument(afg, error_handler)
    def __init__(self, instrument, error_handler, retries=50, delay=0.1):
        self.instrument = instrument
        self.error_handler = error_handler
        self.retries = retries
        self.delay = delay

    def write(self, command):
        for attempt in range(1, self.retries + 1):
            try:
                return self.instrument.write(command)

            except Exception as e:
                print(f"Write failed (attempt {attempt}/{self.retries}): {e}")

                if attempt < self.retries:
                    time.sleep(self.delay)

        # All retries failed
        self.error_handler()

    def query(self, command):
        for attempt in range(1, self.retries + 1):
            try:
                return self.instrument.query(command)

            except Exception as e:
                print(f"Query failed (attempt {attempt}/{self.retries}): {e}")

                if attempt < self.retries:
                    time.sleep(self.delay)

        # All retries failed
        self.error_handler()
    
    def close(self):
        for attempt in range(1, self.retries + 1):
            try:
                return self.instrument.close()

            except Exception as e:
                print(f"Write failed (attempt {attempt}/{self.retries}): {e}")

                if attempt < self.retries:
                    time.sleep(self.delay)

        # All retries failed
        self.error_handler()

def open_resource_safe(rm, resource_name, error_handler,
                        retries=50, delay=0.1):
    # Usage example -
    # afg = open_resource_retry(
    #     rm,
    #     "TCPIP0::192.168.1.10::inst0::INSTR",
    #     error_handler
    # )
    for attempt in range(1, retries + 1):
        try:
            return rm.open_resource(resource_name)

        except Exception as e:
            if attempt > 1:
                print(f"Open resource failed "
                    f"(attempt {attempt}/{retries}): {e}")

            if attempt < retries:
                time.sleep(delay*attempt*attempt)

    # All retries failed
    error_handler()

def error_handler():
    print("Send an email here")
    gsheet_util.email_sender("There is an error in the script.")
    input("Program paused for manual intervention")
    
def open_resource(res_addr):
    res = open_resource_safe(
        rm,
        res_addr,
        error_handler,
        retries,
        delay
    )
    res = RetryInstrument(res, error_handler, retries, delay)
    return res

# i = 100
# while(i > 0):
#     # dmm = open_resource(dmm1_addr)
#     dmm = open_resource("TCPIP0::10.9.0.81::inst0::INSTR")
#     print("Connected to:", dmm.query("*IDN?").strip())
#     dmm.close()
#     print(f"Iter no. {100-i} was successful")
#     i = i-1