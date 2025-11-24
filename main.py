import sys, os
sys.path.append(os.path.dirname(__file__))
import tkinter as tk
from tkinter import ttk, messagebox

from userinfo import add_user, update_user, delete_user, get_users
from news import add_news, update_news, delete_news, get_news


DARK_BG = "#D7EDD7"
ENTRY_BG = "#ffffff"
TEXT_FG = "black"

BUTTON_BG = "#3c3c3c"
ADD_BTN_BG = "#4CAF50"
UPDATE_BTN_BG = "#FF9800"
DELETE_BTN_BG = "#F44336"
ACCENT = "#4e8cff"


def dashboard():
    app = tk.Tk()
    app.title("NEWS DATABASE")
    app.geometry("1100x650")
    app.configure(bg=DARK_BG)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background=ENTRY_BG,
                    foreground="black",
                    fieldbackground=ENTRY_BG,
                    rowheight=28)
    style.configure("TLabel", background=DARK_BG, foreground="black")
    style.map("Treeview", background=[("selected", ACCENT)])

    tab_control = ttk.Notebook(app)
    tab_control.pack(expand=1, fill="both", side="right")

    #USER TAB

    tab_users = tk.Frame(tab_control, bg=DARK_BG)
    tab_control.add(tab_users, text="Users")

    user_frame = tk.Frame(tab_users, bg=DARK_BG)
    user_frame.pack(side="left", padx=10, pady=10, fill="y")

    tk.Label(user_frame, text="Name:", fg=TEXT_FG, bg=DARK_BG).pack(anchor="w")
    name_entry = tk.Entry(user_frame, bg=ENTRY_BG, fg=TEXT_FG)
    name_entry.pack(fill="x", pady=3)

    tk.Label(user_frame, text="Email:", fg=TEXT_FG, bg=DARK_BG).pack(anchor="w")
    email_entry = tk.Entry(user_frame, bg=ENTRY_BG, fg=TEXT_FG)
    email_entry.pack(fill="x", pady=3)

    tk.Label(user_frame, text="Age:", fg=TEXT_FG, bg=DARK_BG).pack(anchor="w")
    age_entry = tk.Entry(user_frame, bg=ENTRY_BG, fg=TEXT_FG)
    age_entry.pack(fill="x", pady=3)

    tk.Label(user_frame, text="Contact:", fg=TEXT_FG, bg=DARK_BG).pack(anchor="w")
    contact_entry = tk.Entry(user_frame, bg=ENTRY_BG, fg=TEXT_FG)
    contact_entry.pack(fill="x", pady=3)

    tk.Button(user_frame, text="Add", bg=ADD_BTN_BG, fg="white",
              command=lambda: add_user_fn()).pack(fill="x", pady=5)

    tk.Button(user_frame, text="Refresh", bg=BUTTON_BG, fg="white",
              command=lambda: refresh_users()).pack(fill="x", pady=5)
    
    tk.Label(user_frame, text="Search User:", fg=TEXT_FG, bg=DARK_BG).pack(anchor="w")
    user_search_entry = tk.Entry(user_frame, bg=ENTRY_BG, fg=TEXT_FG)
    user_search_entry.pack(fill="x", pady=3)

    def search_users():
        keyword = user_search_entry.get().strip()
        for row in users_table.get_children():
            users_table.delete(row)

        from userinfo import search_user_by_name
        results = search_user_by_name(keyword)

        for u in results:
            users_table.insert("", "end", values=u)

    tk.Button(user_frame, text="Search", bg=ACCENT, fg="white",
        command=lambda: search_users()).pack(fill="x", pady=5)


    users_table = ttk.Treeview(
        tab_users,
        columns=("uid", "name", "email", "age", "contact"),
        show="headings"
    )

    users_table.heading("uid", text="UID")
    users_table.heading("name", text="Name")
    users_table.heading("email", text="Email")
    users_table.heading("age", text="Age")
    users_table.heading("contact", text="Contact")

    users_table.column("uid", width=0, stretch=False)
    users_table.column("name", width=150)
    users_table.column("email", width=180)
    users_table.column("age", width=60)
    users_table.column("contact", width=120)

    users_table.pack(side="right", expand=1, fill="both", padx=10, pady=10)

    #USER FUNCTION

    def refresh_users():
        for row in users_table.get_children():
            users_table.delete(row)
        for u in get_users():
            users_table.insert("", "end", values=u)

    def clear_user_fields():
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        contact_entry.delete(0, tk.END)

    def on_user_select(event):
        selected = users_table.selection()
        if not selected:
            return

        uid, uname, uemail, uage, ucontact = users_table.item(selected[0], "values")

        open_user_window(uid, uname, uemail, uage, ucontact)

    

    def open_user_window(uid, uname, uemail, uage, ucontact):
        win = tk.Toplevel(app)
        win.title("Edit User")
        win.geometry("350x350")
        win.configure(bg=DARK_BG)

        tk.Label(win, text="Name:", bg=DARK_BG, fg="black").pack(anchor="w")
        name_e = tk.Entry(win, bg="white", fg="black")
        name_e.pack(fill="x", pady=5)
        name_e.insert(0, uname)

        tk.Label(win, text="Email:", bg=DARK_BG, fg="black").pack(anchor="w")
        email_e = tk.Entry(win, bg="white", fg="black")
        email_e.pack(fill="x", pady=5)
        email_e.insert(0, uemail)

        tk.Label(win, text="Age:", bg=DARK_BG, fg="black").pack(anchor="w")
        age_e = tk.Entry(win, bg="white", fg="black")
        age_e.pack(fill="x", pady=5)
        age_e.insert(0, uage)

        tk.Label(win, text="Contact:", bg=DARK_BG, fg="black").pack(anchor="w")
        contact_e = tk.Entry(win, bg="white", fg="black")
        contact_e.pack(fill="x", pady=5)
        contact_e.insert(0, ucontact)

        def save_changes():
            update_user(
                uid,
                name_e.get(),
                email_e.get(),
                age_e.get(),
                contact_e.get()
            )
            refresh_users()
            win.destroy()

        def delete_user_popup():
            delete_user(uid)
            refresh_users()
            win.destroy()

        tk.Button(win, text="Update", bg=UPDATE_BTN_BG, fg="white",
              command=save_changes).pack(fill="x", pady=8)

        tk.Button(win, text="Delete", bg=DELETE_BTN_BG, fg="white",
              command=delete_user_popup).pack(fill="x", pady=8)


    users_table.bind("<<TreeviewSelect>>", on_user_select)

    def add_user_fn():
        uname = name_entry.get().strip()
        uemail = email_entry.get().strip()
        age = age_entry.get().strip()
        contact = contact_entry.get().strip()

        if not (uname and uemail and age and contact):
            messagebox.showerror("Error", "All fields required")
            return

        add_user(uname, uemail, age, contact)
        clear_user_fields()
        refresh_users()
        refresh_usernames()


    refresh_users()

    #NEWS TAB

    tab_news = tk.Frame(tab_control, bg=DARK_BG)
    tab_control.add(tab_news, text="News")

    news_frame = tk.Frame(tab_news, bg=DARK_BG)
    news_frame.pack(side="left", padx=10, pady=10, fill="y")

    tk.Label(news_frame, text="User:", fg=TEXT_FG, bg=DARK_BG).pack(anchor="w")
    user_combo = ttk.Combobox(news_frame, state="readonly")
    user_combo.pack(fill="x", pady=3)

    tk.Label(news_frame, text="Title:", fg=TEXT_FG, bg=DARK_BG).pack(anchor="w")
    title_entry = tk.Entry(news_frame, bg=ENTRY_BG, fg=TEXT_FG, width=40)
    title_entry.pack(fill="x", pady=3)

    tk.Label(news_frame, text="Body:", fg=TEXT_FG, bg=DARK_BG).pack(anchor="w")
    body_text = tk.Text(news_frame, bg=ENTRY_BG, fg=TEXT_FG, height=13, width=55)
    body_text.pack(fill="both", pady=3)

    tk.Button(news_frame, text="Add", bg=ADD_BTN_BG, fg="white",
              command=lambda: add_news_fn()).pack(fill="x", pady=5)

    tk.Button(news_frame, text="Refresh", bg=BUTTON_BG, fg="white",
              command=lambda: refresh_news()).pack(fill="x", pady=5)
    
    tk.Label(news_frame, text="Search News:", fg=TEXT_FG, bg=DARK_BG).pack(anchor="w")
    news_search_entry = tk.Entry(news_frame, bg=ENTRY_BG, fg=TEXT_FG)
    news_search_entry.pack(fill="x", pady=3)

    def search_news():
        keyword = news_search_entry.get().strip()
        for row in news_table.get_children():
            news_table.delete(row)

        from news import search_news_by_title, search_news_by_content

        results = []

        results += search_news_by_title(keyword)
    
        results += search_news_by_content(keyword)

    
        seen = set()
        unique = []
        for r in results:
            if r[0] not in seen:
                unique.append(r)
                seen.add(r[0])

        for n in unique:
            news_table.insert("", "end", values=n)

    tk.Button(news_frame, text="Search", bg=ACCENT, fg="white",
          command=lambda: search_news()).pack(fill="x", pady=5)


    news_table = ttk.Treeview(
        tab_news,
        columns=("news_id", "username", "title", "body", "created"),
        show="headings"
    )

    for c in ("news_id", "username", "title", "body", "created"):
        news_table.heading(c, text=c.capitalize())

    news_table.column("news_id", width=0, stretch=False)
    news_table.column("username", width=150)
    news_table.column("title", width=200)
    news_table.column("body", width=300)
    news_table.column("created", width=150)

    news_table.pack(side="right", expand=1, fill="both", padx=10, pady=10)

    news_id_var = tk.StringVar()

    #NEWS FUNCTION

    def refresh_usernames():
        users = get_users()
        user_combo["values"] = [u[1] for u in users]

    def find_u_id(username):
        users = get_users()
        for u in users:
            if u[1] == username:
                return u[0]
        return None

    def refresh_news():
        for row in news_table.get_children():
            news_table.delete(row)
        for n in get_news():
            news_table.insert("", "end", values=n)

    def clear_news_fields():
        user_combo.set("")
        title_entry.delete(0, tk.END)
        body_text.delete("1.0", tk.END)
        news_id_var.set("")

    def on_news_select(event):
        selected = news_table.selection()
        if not selected:
            return

        news_id, username, title, body, created = news_table.item(selected[0], "values")
        open_news_window(news_id, username, title, body)


    def open_news_window(news_id, username, title, body):
        win = tk.Toplevel(app)
        win.title("Edit News")
        win.geometry("400x450")
        win.configure(bg=DARK_BG)

        tk.Label(win, text="User:", bg=DARK_BG, fg="black").pack(anchor="w")
        user_c = ttk.Combobox(win, state="readonly")
        all_users = get_users()
        user_c["values"] = [u[1] for u in all_users]
        user_c.set(username)
        user_c.pack(fill="x", pady=3)

        tk.Label(win, text="Title:", bg=DARK_BG, fg="black").pack(anchor="w")
        title_e = tk.Entry(win, bg="white", fg="black")
        title_e.pack(fill="x", pady=5)
        title_e.insert(0, title)

        tk.Label(win, text="Body:", bg=DARK_BG, fg="black").pack(anchor="w")
        body_t = tk.Text(win, bg="white", fg="black", height=12)
        body_t.pack(fill="both", pady=5)
        body_t.insert("1.0", body)

        def save_news_changes():
            all_users = get_users() 
            u_id = None
            for u in all_users:
                if u[1] == user_c.get():
                    u_id = u[0]

            update_news(news_id, title_e.get(), body_t.get("1.0", tk.END).strip())
            refresh_news()
            win.destroy()

        def delete_news_popup():
            delete_news(news_id)
            refresh_news()
            win.destroy()

        tk.Button(win, text="Update", bg=UPDATE_BTN_BG, fg="white",
              command=save_news_changes).pack(fill="x", pady=8)

        tk.Button(win, text="Delete", bg=DELETE_BTN_BG, fg="white",
              command=delete_news_popup).pack(fill="x", pady=8)


    news_table.bind("<<TreeviewSelect>>", on_news_select)

    def add_news_fn():
        username = user_combo.get()
        title = title_entry.get().strip()
        body = body_text.get("1.0", tk.END).strip()

        if not (username and title and body):
            messagebox.showerror("Error", "All fields are required")
            return

        u_id = find_u_id(username)
        add_news(u_id, title, body)

        clear_news_fields()
        refresh_news()


    refresh_usernames()
    refresh_users()
    refresh_news()

    app.mainloop()



dashboard()
