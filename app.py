import os
import subprocess
from pathlib import Path
from tkinter import Tk, filedialog, simpledialog, Label, Button, StringVar, Entry, Frame, messagebox
import tkinter.font as tkFont

# Function to run commands in terminal
def run_command(command, cwd=None):
    """Runs a command in the terminal."""
    try:
        result = subprocess.run(command, cwd=cwd, shell=True, check=True)
        if result.returncode == 0:
            return True
    except subprocess.CalledProcessError as e:
        return False

# Function to setup the React frontend
def create_react_frontend(project_folder, project_name, status_label):
    status_label.config(text="Creating React frontend...")
    frontend_dir = project_folder / "frontend"
    if run_command(f"npx create-react-app {frontend_dir}"):
        status_label.config(text="React frontend created successfully!")
    else:
        status_label.config(text="Failed to create React frontend.")
    return frontend_dir

# Function to setup the Node.js backend
def create_express_backend(project_folder, project_name, mongo_url, status_label):
    status_label.config(text="Setting up Express backend...")
    backend_dir = project_folder / "backend"
    os.mkdir(backend_dir)
    status_label.config(text="Initializing Node.js...")
    
    if run_command("npm init -y", cwd=backend_dir):
        status_label.config(text="Node.js initialized successfully!")
    else:
        status_label.config(text="Node.js initialization failed.")
        return None

    status_label.config(text="Installing backend dependencies...")
    if run_command("npm install express mongoose dotenv cors", cwd=backend_dir):
        status_label.config(text="Backend dependencies installed successfully!")
    else:
        status_label.config(text="Failed to install backend dependencies.")
        return None

    # Basic server.js file
    server_code = f"""
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {{
    res.send('Hello from the backend!');
}});

mongoose.connect(process.env.MONGO_URI, {{
    useNewUrlParser: true,
    useUnifiedTopology: true,
}}).then(() => console.log('Connected to MongoDB'))
.catch((err) => console.log(err));

const port = process.env.PORT || 5000;
app.listen(port, () => {{
    console.log(`Server running on port {{port}}`);
}});
    """
    with open(backend_dir / "server.js", "w") as f:
        f.write(server_code)

    # Create .env file
    env_content = f"MONGO_URI={mongo_url}\nPORT=5000\n"
    with open(backend_dir / ".env", "w") as f:
        f.write(env_content)

    status_label.config(text="Express backend setup complete!")
    return backend_dir

# Function to run both frontend and backend servers
def run_projects(frontend_dir, backend_dir, status_label):
    status_label.config(text="Starting frontend and backend servers...")
    subprocess.Popen(["npm", "start"], cwd=frontend_dir, shell=True)
    subprocess.Popen(["npm", "run", "start"], cwd=backend_dir, shell=True)
    status_label.config(text="Both servers are running!")

# Main function to handle project setup
def create_project(project_name, mongo_url, base_dir, status_label):
    project_folder = Path(base_dir) / project_name
    os.mkdir(project_folder)
    
    status_label.config(text="Creating project directories...")
    
    frontend_dir = create_react_frontend(project_folder, project_name, status_label)
    if frontend_dir is None:
        return
    
    backend_dir = create_express_backend(project_folder, project_name, mongo_url, status_label)
    if backend_dir is None:
        return

    run_projects(frontend_dir, backend_dir, status_label)
    messagebox.showinfo("Setup Complete", "MERN stack project has been successfully created and both servers are running!")

# Tkinter app with enhanced UI/UX
def start_app():
    # Initialize the window
    root = Tk()
    root.title("MERN Stack Project Generator")
    root.geometry("600x400")
    root.configure(bg="#1e1e1e")

    # Set the fonts
    title_font = tkFont.Font(family="Helvetica", size=18, weight="bold")
    label_font = tkFont.Font(family="Helvetica", size=12)

    # Title
    title_label = Label(root, text="MERN Stack Project Generator", font=title_font, fg="white", bg="#1e1e1e")
    title_label.pack(pady=20)

    # Instructions
    instructions = Label(root, text="\nIt take sometime to create the app so please wait and it will automatically runs on browser ! Happy Coding \nEnter your project details below:", font=label_font, fg="white", bg="#1e1e1e")
    instructions.pack(pady=5)

    # Frame for user inputs
    input_frame = Frame(root, bg="#2e2e2e", padx=20, pady=20)
    input_frame.pack(pady=10)

    # Project name
    project_name_label = Label(input_frame, text="Project Name:", font=label_font, fg="white", bg="#2e2e2e")
    project_name_label.grid(row=0, column=0, sticky="w", pady=5)
    project_name_var = StringVar()
    project_name_entry = Entry(input_frame, textvariable=project_name_var, width=30)
    project_name_entry.grid(row=0, column=1, pady=5)

    # MongoDB URL
    mongo_url_label = Label(input_frame, text="MongoDB URL:", font=label_font, fg="white", bg="#2e2e2e")
    mongo_url_label.grid(row=1, column=0, sticky="w", pady=5)
    mongo_url_var = StringVar()
    mongo_url_entry = Entry(input_frame, textvariable=mongo_url_var, width=30)
    mongo_url_entry.grid(row=1, column=1, pady=5)

    # Directory selection
    def choose_directory():
        directory = filedialog.askdirectory(title="Select Project Directory")
        if directory:
            dir_var.set(directory)

    dir_var = StringVar()
    dir_label = Label(input_frame, text="Project Directory:", font=label_font, fg="white", bg="#2e2e2e")
    dir_label.grid(row=2, column=0, sticky="w", pady=5)
    dir_entry = Entry(input_frame, textvariable=dir_var, width=30)
    dir_entry.grid(row=2, column=1, pady=5)
    dir_button = Button(input_frame, text="Browse", command=choose_directory, bg="#61dafb", fg="black")
    dir_button.grid(row=2, column=2, padx=10, pady=5)

    # Status label
    status_label = Label(root, text="", font=label_font, fg="white", bg="#1e1e1e")
    status_label.pack(pady=10)

    # Submit Button
    def submit_details():
        project_name = project_name_var.get()
        mongo_url = mongo_url_var.get()
        base_dir = dir_var.get()

        if not project_name or not mongo_url or not base_dir:
            messagebox.showerror("Error", "All fields are required!")
        else:
            create_project(project_name, mongo_url, base_dir, status_label)

    submit_button = Button(root, text="Create Project", command=submit_details, bg="#61dafb", fg="black", padx=20, pady=10)
    submit_button.pack(pady=20)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    start_app()
