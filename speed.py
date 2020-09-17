# Internet Speed Test

import speedtest
count = 0
def get_speed():
    try:
        st = speedtest.Speedtest()
        result = st.download()
        return result
    except:
        result = -1
        return result