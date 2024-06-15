import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

kivy.require('2.1.0')  # Replace with your Kivy version

class ToDoApp(App):
    def build(self):
        self.title = "To-Do List"
        self.tasks = []
        
        self.layout = BoxLayout(orientation='vertical')
        
        self.task_input = TextInput(hint_text='Enter a new task', size_hint_y=None, height=30, multiline=False)
        self.layout.add_widget(self.task_input)
        
        self.add_button = Button(text='Add Task', size_hint_y=None, height=50, on_press=self.add_task)
        self.layout.add_widget(self.add_button)
        
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 500))
        self.task_list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.task_list_layout.bind(minimum_height=self.task_list_layout.setter('height'))
        self.scroll_view.add_widget(self.task_list_layout)
        
        self.layout.add_widget(self.scroll_view)
        
        return self.layout

    def add_task(self, instance):
        task_text = self.task_input.text.strip()
        if task_text:
            task_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            
            task_label = Label(text=task_text, size_hint_x=0.8)
            task_layout.add_widget(task_label)
            
            remove_button = Button(text='Remove', size_hint_x=0.2, on_press=lambda instance: self.remove_task(task_layout))
            task_layout.add_widget(remove_button)
            
            self.task_list_layout.add_widget(task_layout)
            self.tasks.append(task_text)
            self.task_input.text = ''

    def remove_task(self, task_layout):
        self.task_list_layout.remove_widget(task_layout)

if __name__ == '__main__':
    ToDoApp().run()
