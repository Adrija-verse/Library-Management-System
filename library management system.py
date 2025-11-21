import tkinter as tk
from tkinter import messagebox, simpledialog
import os

FILE = "books.txt"


def load_books():
    if not os.path.exists(FILE):
        return []
    books = []
    with open(FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            parts = line.split(",")
            if len(parts) != 4:
                continue
            books.append(parts)
    return books


def save_books(books):
    with open(FILE, "w") as f:
        for b in books:
            f.write(",".join(b) + "\n")




def refresh_display():
    """Show books inside the GUI text area."""
    text_area.delete("1.0", tk.END)
    books = load_books()

    if not books:
        text_area.insert(tk.END, "No books found.\n")
        return

    for b in books:
        text_area.insert(tk.END,
                         f"ID: {b[0]} | {b[1]} - {b[2]} [{b[3]}]\n")


def add_book():
    name = entry_name.get()
    author = entry_author.get()

    if name == "" or author == "":
        messagebox.showerror("Error", "Enter both Book Name & Author")
        return

    books = load_books()
    book_id = str(len(books) + 1)

    books.append([book_id, name, author, "Available"])
    save_books(books)

    entry_name.delete(0, tk.END)
    entry_author.delete(0, tk.END)

    messagebox.showinfo("Success", "Book added!")
    refresh_display()


def search_book():
    key = simpledialog.askstring("Search", "Enter book name or author:")
    if not key:
        return

    books = load_books()
    text_area.delete("1.0", tk.END)

    found = False
    for b in books:
        if key.lower() in b[1].lower() or key.lower() in b[2].lower():
            found = True
            text_area.insert(tk.END,
                             f"ID: {b[0]} | {b[1]} - {b[2]} [{b[3]}]\n")

    if not found:
        text_area.insert(tk.END, "No matching books found.\n")


def delete_book():
    book_id = simpledialog.askstring("Delete", "Enter Book ID:")
    if not book_id:
        return

    books = load_books()
    new_list = [b for b in books if b[0] != book_id]

    if len(new_list) == len(books):
        messagebox.showerror("Error", "Book ID not found")
        return

    save_books(new_list)
    messagebox.showinfo("Deleted", "Book deleted!")
    refresh_display()


def issue_book():
    book_id = simpledialog.askstring("Issue Book", "Enter Book ID:")
    if not book_id:
        return

    books = load_books()

    for b in books:
        if b[0] == book_id:
            if b[3] == "Issued":
                messagebox.showerror("Error", "Book already issued!")
                return
            b[3] = "Issued"
            save_books(books)
            messagebox.showinfo("Issued", "Book issued!")
            refresh_display()
            return

    messagebox.showerror("Error", "Book ID not found")


def return_book():
    book_id = simpledialog.askstring("Return Book", "Enter Book ID:")
    if not book_id:
        return

    books = load_books()

    for b in books:
        if b[0] == book_id:
            if b[3] == "Available":
                messagebox.showerror("Error", "Book already available!")
                return
            b[3] = "Available"
            save_books(books)
            messagebox.showinfo("Returned", "Book returned!")
            refresh_display()
            return

    messagebox.showerror("Error", "Book ID not found")


def edit_book():
    book_id = simpledialog.askstring("Edit Book", "Enter Book ID:")
    if not book_id:
        return

    books = load_books()

    for b in books:
        if b[0] == book_id:
            new_name = simpledialog.askstring("Edit", "New Book Name:", initialvalue=b[1])
            new_author = simpledialog.askstring("Edit", "New Author:", initialvalue=b[2])

            if new_name:
                b[1] = new_name
            if new_author:
                b[2] = new_author

            save_books(books)
            messagebox.showinfo("Updated", "Book details updated!")
            refresh_display()
            return

    messagebox.showerror("Error", "Book ID not found")




root = tk.Tk()
root.title("Library Management System")
root.geometry("600x600")
root.config(bg="#1f1f2e")

header = tk.Label(root, text="📚 Library Management System",
                  font=("Arial Rounded MT Bold", 22),
                  fg="#00f7ff", bg="#1f1f2e")
header.pack(pady=20)

# Form Frame
card = tk.Frame(root, bg="#2a2a40", bd=5, relief="groove")
card.pack(pady=10)

tk.Label(card, text="Book Name:", font=("Arial", 14),
         bg="#2a2a40", fg="white").grid(row=0, column=0, pady=10, padx=10)
entry_name = tk.Entry(card, width=30, font=("Arial", 12),
                      bg="#3d3d59", fg="white")
entry_name.grid(row=0, column=1)

tk.Label(card, text="Author:", font=("Arial", 14),
         bg="#2a2a40", fg="white").grid(row=1, column=0, pady=10, padx=10)
entry_author = tk.Entry(card, width=30, font=("Arial", 12),
                        bg="#3d3d59", fg="white")
entry_author.grid(row=1, column=1)


# Neon Button Maker
def neon_button(text, cmd):
    return tk.Button(
        root, text=text, width=22, height=1,
        command=cmd, font=("Arial Rounded MT Bold", 12),
        bg="#00d4ff", fg="black",
        activebackground="#00f7ff",
        bd=0, relief="flat", cursor="hand2"
    )


neon_button("Add Book", add_book).pack(pady=4)
neon_button("Search Book", search_book).pack(pady=4)
neon_button("Delete Book", delete_book).pack(pady=4)
neon_button("Issue Book", issue_book).pack(pady=4)
neon_button("Return Book", return_book).pack(pady=4)
neon_button("Edit Book", edit_book).pack(pady=4)


display_label = tk.Label(root, text="📘 Book Records",
                         font=("Arial Rounded MT Bold", 16),
                         fg="#00f7ff", bg="#1f1f2e")
display_label.pack(pady=10)


text_frame = tk.Frame(root)
text_frame.pack()

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_area = tk.Text(text_frame, width=68, height=12,
                    bg="#2a2a40", fg="white", font=("Arial", 12),
                    yscrollcommand=scrollbar.set)
text_area.pack()

scrollbar.config(command=text_area.yview)


refresh_display()

root.mainloop()

