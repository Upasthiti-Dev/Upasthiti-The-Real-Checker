# Python program to test
# internet speed

import speedtest

def get_speed():
    st = speedtest.Speedtest()
    return st.download()
