# Internet Speed Test

import speedtest
count = 0
def get_speed():
    try:
        st = speedtest.Speedtest()
        result = st.download()
        print(result%1000000)
        return result
    except:
        result = -1
        return result