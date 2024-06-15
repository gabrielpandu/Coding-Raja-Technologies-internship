import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
import json
import os

kivy.require('2.1.0')  # Replace with your Kivy version

DATA_FILE = 'budget_data.json'

class BudgetTrackerApp(App):
    def build(self):
        self.title = "Budget Tracker"
        self.budget_data = []

        self.load_data()

        self.layout = BoxLayout(orientation='vertical')

        self.income_input = TextInput(hint_text='Enter income', size_hint_y=None, height=40, multiline=False)
        self.layout.add_widget(self.income_input)

        self.expense_input = TextInput(hint_text='Enter expense', size_hint_y=None, height=40, multiline=False)
        self.layout.add_widget(self.expense_input)

        self.add_button = Button(text='Add Entry', size_hint_y=None, height=50, on_press=self.add_entry)
        self.layout.add_widget(self.add_button)

        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 500))
        self.entry_list_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.entry_list_layout.bind(minimum_height=self.entry_list_layout.setter('height'))
        self.scroll_view.add_widget(self.entry_list_layout)

        self.layout.add_widget(self.scroll_view)

        self.total_label = Label(text='Total Balance: $0.00', size_hint_y=None, height=40)
        self.layout.add_widget(self.total_label)

        self.summary_label = Label(text='', size_hint_y=None, height=40)
        self.layout.add_widget(self.summary_label)

        self.populate_entries()
        self.update_total()

        return self.layout

    def add_entry(self, instance):
        income_text = self.income_input.text.strip()
        expense_text = self.expense_input.text.strip()

        if income_text or expense_text:
            try:
                income = float(income_text) if income_text else 0
                expense = float(expense_text) if expense_text else 0

                if income == 0 and expense == 0:
                    raise ValueError("Both fields cannot be zero")

                entry_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)

                entry_label = Label(text=f"Income: ${income:.2f}, Expense: ${expense:.2f}", size_hint_x=0.8)
                entry_layout.add_widget(entry_label)

                remove_button = Button(text='Remove', size_hint_x=0.2, on_press=lambda instance: self.remove_entry(entry_layout, income, expense))
                entry_layout.add_widget(remove_button)

                self.entry_list_layout.add_widget(entry_layout)
                self.budget_data.append((income, expense))
                self.save_data()
                self.update_total()

                self.income_input.text = ''
                self.expense_input.text = ''
            except ValueError:
                popup = Popup(title='Invalid Input',
                              content=Label(text='Please enter valid numbers for income and expense.'),
                              size_hint=(0.6, 0.4))
                popup.open()

    def remove_entry(self, entry_layout, income, expense):
        self.entry_list_layout.remove_widget(entry_layout)
        self.budget_data.remove((income, expense))
        self.save_data()
        self.update_total()

    def update_total(self):
        total_income = sum(income for income, expense in self.budget_data)
        total_expense = sum(expense for income, expense in self.budget_data)
        total_balance = total_income - total_expense
        self.total_label.text = f'Total Balance: ${total_balance:.2f}'
        self.summary_label.text = f'Total Income: ${total_income:.2f}, Total Expense: ${total_expense:.2f}'

    def save_data(self):
        with open(DATA_FILE, 'w') as file:
            json.dump(self.budget_data, file)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                self.budget_data = json.load(file)

    def populate_entries(self):
        for income, expense in self.budget_data:
            entry_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)

            entry_label = Label(text=f"Income: ${income:.2f}, Expense: ${expense:.2f}", size_hint_x=0.8)
            entry_layout.add_widget(entry_label)

            remove_button = Button(text='Remove', size_hint_x=0.2, on_press=lambda instance: self.remove_entry(entry_layout, income, expense))
            entry_layout.add_widget(remove_button)

            self.entry_list_layout.add_widget(entry_layout)

if __name__ == '__main__':
    BudgetTrackerApp().run()
