from tkinter import ttk
import tkinter as tk
from functools import partial

class ParamsPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        paramsLabel = ttk.Label(self,text="This page will be used to view and modify parameters!").grid(row=0,column=0,columnspan=2,pady=5)