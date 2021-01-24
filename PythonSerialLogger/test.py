
import main as logger
import glob

from event_scripts import run_video_once

logger.filter_keywords("!eventcall Countdown")


# run_video_once.run_video("191030_V2_Countdown  Stimme Reinraum_fp.mp4")
'''
while True:

    ser = logger.scan_serial()
    print(ser)
    if ser:
        if ser.is_open:
            print("open")
        else:
            print("closed")

exit()


main()

'''

