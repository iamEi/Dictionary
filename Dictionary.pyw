import tkinter as tk
from tkinter import messagebox
import os, json

class mainApplication:
	def __init__(self,screen):
		self.screen = screen
		self.window_width = 400
		self.window_height = 200
		self.screen.iconbitmap("dict_icon.ico")

		self.screen.title("Dictionary")
		self.screen.minsize(self.window_width,self.window_height)
		self.update()
		self.screen.bind("<Return>",lambda event: self.search())
		self.screen.bind("<Escape>",lambda event: self.clear())

	def container(self):
		self.container1 = tk.Frame(self.screen, height = self.window_height, width = self.window_width)
		self.container1.grid(column = 0, row = 0)

		self.container2 = tk.Frame(self.screen, height = self.window_height, width = self.window_width)
		self.container2.grid(column = 0, row = 1)

	def search_bar(self):
		self.word = tk.StringVar()
		self.bar = tk.Entry(self.container1, width = 45,bd = 5, justify = 'center', relief = "groove", textvariable=self.word)
		self.bar.grid(column = 0, row = 0, padx = 10, pady = 20)

	def go_button(self):
		go = tk.Button(self.container1, width = 10, text = "Go", relief = "groove", bd = 5, command = self.search)
		go.grid(column = 1, row = 0, padx = 10, pady = 20)


	def search(self):
		word_types = {"Noun": [], "Pronoun": [], "Adjective": [], "Verb": [], "Adverb": [], "Preposition": [], "Conjunction": [],"Interjection": []}
		word_syn = []
		rows = 0
		width = 0
		self.delete_children()
		file_path = os.getcwd()
		file_path = os.path.join(file_path, "data")
		dictionary = os.path.join(file_path,f"{self.word.get()[0].upper()}.json")
		try:
			with open(dictionary) as f:
				file = json.load(f)
				meanings = file[self.word.get().upper()]["MEANINGS"].values()
				synonyms = file[self.word.get().upper()]["SYNONYMS"]
				if meanings:
					for key in meanings:
						word_types[key[0]].append(key[1])
					for key, values in word_types.items():
						if values:
							type_label = tk.Label(self.container2,text = f"{key}:", fg = 'Red', font = 'bold')
							type_label.grid(column = 0, row = rows)
							rows += 1
							for value in values:
								meaning_label = tk.Label(self.container2, text = f">> {value.capitalize()}")
								meaning_label.grid(column = 1, row = rows, sticky = 'w')
								rows += 1
								if len(value)>width: width = len(value)
				else:
					type_label = tk.Label(self.container2,text = f"SYNONYMS:", fg = 'Red', font = 'bold')
					type_label.grid(column = 0, row = rows)
					rows += 1
					for synonym in synonyms:
						word_syn.append(synonym)
						meaning_label = tk.Label(self.container2, text = f">> {synonym.capitalize()}")
						meaning_label.grid(column = 1, row = rows, sticky = 'w')
						rows += 1
			
		except KeyError:
			tk.messagebox.showwarning("Failed", "Word not Found")

		self.adjust_window(rows, width)

	def delete_children(self):
		for child in self.container2.winfo_children():
			child.destroy()

	def adjust_window(self,line_count, line_width):
		self.window_width = 500 + line_width*2
		self.window_height = 80 + (line_count+1)*20
		self.set_window()

	def set_window(self):
		screen_width = self.screen.winfo_screenwidth()
		screen_height = self.screen.winfo_screenheight()
		center_x = screen_width//2 - self.window_width//2
		center_y = screen_height//2 - self.window_height//2
		self.screen.geometry(f"{self.window_width}x{self.window_height}+{center_x}+{center_y}")

	def clear(self):
		self.word.set("")

	def update(self):
		self.set_window()
		self.container()
		self.search_bar()
		self.go_button()



if __name__ == '__main__':
	screen = tk.Tk()
	mainApplication(screen)
	screen.mainloop()

