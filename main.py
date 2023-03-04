import datetime
import os.path
import subprocess
import tkinter as tk
import  cv2
import util
from PIL import Image, ImageTk

class App:
    def __init__(self):
        # here the main window is created with dimension and all that
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        # new login button is created here using the get_button which is available in util.py
        self.login_button = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button.place(x=750, y=300)

        # new register button is created same as login button
        self.register_button = util.get_button(self.main_window, 'Register new user', 'white', self.register, fg='grey')
        self.register_button.place(x=750, y=400)

        # here the label of webcam is set , of what shape and size it should be
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        # here the add_webcam function which takes label as argument and proceeds the next step
        self.add_webcam(self.webcam_label)

        # here we are maiking a database if the path does not exist
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self,label):
        # using cv2 we arer getting the videoCapture functionality and using cap we are checking if it has been
        # done already in the system
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label

        # here the function process_webcam() is called which tell what to capture and how
        self.process_webcam()

    def process_webcam(self):
        # this will read from the videocapture
        ret, frame = self.cap.read()

        # here the frame is set to most_recent_capture_arr which will be further used to convert to pillow
        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_PIL = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_PIL)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        # in order to behave like it is streaming we will call the function process_webcam
        # every 20ms
        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_path = './.tmp.jpg'
        cv2.imwrite(unknown_path, self.most_recent_capture_arr)
        output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_path]))
        name = output.split(',')[1][:-3]
        print(name)

        if name in ['unknown_person', 'no_person_found']:
            util.msg_box('ops', 'Unknown user please register new user or try again')
        else:
            util.msg_box('Welcome back','Welcome, {}'.format(name))
            with open(self.log_path, 'a') as f:
                f.write('{},{}\n'.format(name, datetime.datetime.now()))
                f.close()

        os.remove(unknown_path)

    def register(self):
        # Read the main window comment it is similar to that
        # we have created a new window ie the register_new_user_window which will be same as main_window as earlier
        # but few more functionality and here we will capture the image not run it again and again.

        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+350+120")

        self.accept_new_user_register = util.get_button(self.register_new_user_window,
                                                        'login', 'green', self.accept_new_user)
        self.accept_new_user_register.place(x=750, y=300)

        self.try_again_new_user_register = util.get_button(self.register_new_user_window,
                                                           'Try again', 'red',self.try_again_new_user)
        self.try_again_new_user_register.place(x=750, y=400)

        # here label is fixed to whatever size we need
        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        # here the image is added to the label we have created
        self.add_img_label(self.capture_label)

        self.new_user_text_entry = util.get_entry_text(self.register_new_user_window)
        self.new_user_text_entry.place(x=750, y=150)

        self.input_text_label = util.get_text_label(self.register_new_user_window,'Please:  Enter Username')
        self.input_text_label.place(x=750, y=70)

    def try_again_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_PIL)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_new_user(self):
        name = self.new_user_text_entry.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)
        util.msg_box('Sucess!', 'User was registered Sucessfully')

        self.register_new_user_window.destroy()

    def start(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
