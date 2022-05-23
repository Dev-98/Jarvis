import os, pyautogui, datetime
import subprocess as sp
from PIL import Image


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def screenshot(s_name):
    img = pyautogui.screenshot()
    name = f"D:\\{s_name}.png"
    img.save(name)

    # try:
    #     img = Image.open(f"D:\\{s_name}.png")
    #     img.show(img)
    #     # speak('Here it is sir')
    #     time.sleep(2)
    # except IOError:
    #     print( 'sorry')
    #     # speak('Sorry, I am unable to display it now sir ')

def notepad():
    # exec(Path(paths['notepad']).read_text())
    sp.Popen(paths['notepad'])

def curr_time():
    return datetime.datetime.now().strftime('%I:%M:%p')

def graphi():
    # This can be a replacement of sp.call([]) but some time this doesn't work
    exec(open(paths['design']).read())

def shinchan():
    # If you want to open any apps or file that is not of system use call function of subprocess
    sp.call(['python.exe',paths['shinchan']])

    
def calculator():
    sp.Popen(paths['calculator'])

def open_cmd():
    os.system('start cmd')

def paint():
    sp.Popen(paths['paint'])


paths = {'notepad':"C:\\Windows\\System32\\notepad.exe",
    'design': "C:\\Users\\Dev Gupta\\Documents\\GUI\\grahical_pen_2.py",
    'calculator': "C:\\Windows\\System32\\calc.exe",
    'paint':'C:\\Windows\\System32\\mspaint.exe',
    'shinchan':'C:\\Users\\Dev Gupta\\Documents\\GUI\\shinchan.py'
}

if __name__ == '__main__':
    # calculator()
    # notepad()
    # print(curr_time())
    # graphi()
    shinchan()
    # screenshot('try3')
