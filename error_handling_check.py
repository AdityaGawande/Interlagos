import time
import pyvisa
from constants import *

rm = pyvisa.ResourceManager()


class RetryInstrument:
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

# afg = RetryInstrument(afg, error_handler)


def open_resource_safe(rm, resource_name, error_handler,
                        retries=50, delay=0.1):

    for attempt in range(1, retries + 1):
        try:
            return rm.open_resource(resource_name)

        except Exception as e:
            print(f"Open resource failed "
                  f"(attempt {attempt}/{retries}): {e}")

            if attempt < retries:
                time.sleep(delay)

    # All retries failed
    error_handler()

# afg = open_resource_retry(
#     rm,
#     "TCPIP0::192.168.1.10::inst0::INSTR",
#     error_handler
# )

def error_handler():
    print("Send an email here")
    input("Program paused for manual intervention")
    
    
def open_resource(res_addr):
    res = open_resource_safe(
        rm,
        res_addr,
        error_handler
    )
    res = RetryInstrument(res, error_handler)
    return res

i = 100
while(i > 0):
    # dmm = rm.open_resource(dmm1_addr)
    # dmm = open_resource_safe(
    #     rm,
    #     dmm1_addr,
    #     error_handler
    # )
    # dmm = open_resource(dmm1_addr)
    dmm = open_resource("TCPIP0::10.9.0.81::inst0::INSTR")
    # str = dmm.query("READ?")
    print("Connected to:", dmm.query("*IDN?").strip())
    # time.sleep(1)
    # print(str)
    dmm.close()
    print(f"Iter no. {100-i} was successful")
    # if(i < 50):
    # time.sleep(0.1)
    i = i-1
