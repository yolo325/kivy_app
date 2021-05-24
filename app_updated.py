from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.graphics import *
import cv2
import numpy as np
import time


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def work():
####основная логика приложения

def blur_face(frame):
    (h,w) = frame.shape[:2]
    dW = int(w / 3.0)
    dH = int(h / 3.0)
    if dW % 2 == 0:
        dW -= 1
    if dH % 2 == 0:
        dH -= 1
    return cv2.GaussianBlur(frame, (dW, dH), 0)

class ConnectPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [200]

        self.add_widget(Label(text="Введите дату"))
        self.date = TextInput()
        self.add_widget(self.date)

        self.add_widget(Label(text="Введите имя"))
        self.name = TextInput()
        self.add_widget(self.name)

        self.join = Button(text="Продолжить")
        self.join.bind(on_press=self.button_work)
        self.add_widget(self.join)

        self.join2 = Button(text="данные уже введены")
        self.join2.bind(on_press=self.button_work_third)
        self.add_widget(self.join2)

    def button_work(self, instance):
        general_app.screen_manager.current = 'Main_Page'


    def button_work_third(self, instance):
        general_app.screen_manager.current = 'Final_Page'

class MainPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img1 = Image()
        self.add_widget(self.img1)

        self.orientation = 'vertical'
        self.padding = 100

        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/33.0)

        self.join = Button(text="Продолжить", background_color = [0, 153, 204, 1])
        self.join.bind(on_press=self.second_button_work)
        self.add_widget(self.join)

    def second_button_work(self, instance):
        general_app.screen_manager.current = 'Final_Page'

    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.5,minNeighbors=5,minSize=(20,20) )
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            img_gray_face = frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(img_gray_face, 1.1, 19)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (255, 0, 0), 2)

        cv2.imshow("CV2 Image", frame)
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer.
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = texture1

class FinalPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 200

        self.main_label = Label(text="information")
        self.add_widget(self.main_label)
        self.join = Button(text="Вывод информации")
        self.join.bind(on_press= self.final_button_work)
        self.add_widget(self.join)

    def final_button_work(self, event):
        self.main_label.text = str(work())




class TestApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.connect_page = ConnectPage()
        screen = Screen(name="Connect")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.main_page = MainPage()
        screen2 = Screen(name="Main_Page")
        screen2.add_widget(self.main_page)
        self.screen_manager.add_widget(screen2)

        self.final_page = FinalPage()
        screen3 = Screen(name="Final_Page")
        screen3.add_widget(self.final_page)
        self.screen_manager.add_widget(screen3)

        Clock.schedule_once(self.set_background, 0)

        return self.screen_manager

    def set_background(self, *args):
        self.root_window.bind(size=self.do_resize)
        with self.root_window.canvas.before:
            self.bg = Rectangle(source='nptcry.jpg', pos=(0, 0), size=(self.root_window.size))

    def do_resize(self, *args):
        self.bg.size = self.root_window.size

if __name__ == '__main__':
    general_app =TestApp()
    general_app.run()