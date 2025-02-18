import streamlit as st
import os
import base64
import json
import hashlib
from datetime import datetime
from pathlib import Path
import re
import shutil
import time

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "login"

# Create necessary directories
DATA_DIR = Path("data")
UPLOAD_DIR = Path("uploads")
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize JSON files if they don't exist
USERS_FILE = DATA_DIR / "users.json"
FILES_FILE = DATA_DIR / "files.json"

if not USERS_FILE.exists():
    with open(USERS_FILE, 'w') as f:
        json.dump({
            "admin": {
                "password": hashlib.sha256("password123".encode()).hexdigest(),
                "email": "admin@example.com",
                "created_at": datetime.now().strftime("%Y-%m-%d")
            }
        }, f, indent=4)

if not FILES_FILE.exists():
    with open(FILES_FILE, 'w') as f:
        json.dump({"files": []}, f, indent=4)

def load_users():
    """Load users from JSON file"""
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_files():
    """Load file metadata from JSON file"""
    with open(FILES_FILE, 'r') as f:
        return json.load(f)

def save_files(files):
    """Save file metadata to JSON file"""
    with open(FILES_FILE, 'w') as f:
        json.dump(files, f, indent=4)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

# Set page configuration
st.set_page_config(
    page_title="File Share Hub",
    page_icon="📁",
    layout="wide"
)

# Custom CSS to improve UI
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #009688;
        color: white;
        border-radius: 5px;
        padding: 0.5rem;
    }
    .logout-btn {
        position: absolute;
        right: 2rem;
        top: 2rem;
    }
    .logout-btn .stButton>button {
        background-color: rgba(255, 255, 255, 0.2);
        border: 1px solid white;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
        width: auto !important;
    }
    .logout-btn .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.3);
    }
    .upload-header {
        color: #fff;
        font-family: 'Helvetica Neue', sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .file-list {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #fff;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.2) !important;
    }
    /* Main background with teal gradient */
    .main {
        background: linear-gradient(135deg, #4DB6AC 0%, #26A69A 100%);
        padding: 2rem;
        border-radius: 10px;
        margin: -1rem -1rem 2rem -1rem;
    }
    /* Override Streamlit's default background */
    .stApp {
        background: linear-gradient(135deg, #F5F9F9 0%, #E0F2F1 100%);
    }
    .drag-and-drop {
        border: 2px dashed #009688;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: rgba(255, 255, 255, 0.9);
        cursor: pointer;
    }
    .drag-and-drop:hover {
        background-color: rgba(255, 255, 255, 1);
        border-color: #00796B;
    }
    .search-box {
        margin-bottom: 20px;
    }
    .auth-form {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        max-width: 400px;
        margin: 0 auto;
    }
    </style>
    <script>
    // Add drag and drop highlighting
    const preventDefault = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };
    </script>
""", unsafe_allow_html=True)

def signup_form():
    """Display signup form and handle registration"""
    st.markdown("<h2 style='color: #009688; text-align: center;'>Sign Up</h2>", unsafe_allow_html=True)
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submitted = st.form_submit_button("Sign Up")
        if submitted:
            users = load_users()
            if username in users:
                st.error("Username already exists!")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Invalid email address!")
            elif password != confirm_password:
                st.error("Passwords do not match!")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long!")
            else:
                # Create progress bar for signup animation
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate signup process with animation
                for i in range(100):
                    progress_bar.progress(i + 1)
                    if i < 30:
                        status_text.text("Creating your account...")
                    elif i < 60:
                        status_text.text("Setting up your profile...")
                    elif i < 90:
                        status_text.text("Almost there...")
                    else:
                        status_text.text("Finalizing...")
                    time.sleep(0.01)

                # Save user data
                users[username] = {
                    "password": hash_password(password),
                    "email": email,
                    "created_at": datetime.now().strftime("%Y-%m-%d")
                }
                save_users(users)
                
                # Clear progress bar and status
                progress_bar.empty()
                status_text.empty()
                
                # Show success message with confetti
                st.balloons()
                success_msg = st.success("🎉 Account created successfully!")
                
                # Automatically log in the user
                st.session_state.authenticated = True
                st.session_state.username = username
                
                # Wait for 2 seconds to show the success message
                time.sleep(2)
                st.rerun()

def login_form():
    """Display login form and handle authentication"""
    st.markdown("<h2 style='color: #009688; text-align: center;'>Login</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        submitted = st.form_submit_button("Login")
        if submitted:
            users = load_users()
            if username in users and users[username]["password"] == hash_password(password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")

def save_file(uploaded_file):
    """Save uploaded file and metadata"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
    file_path = UPLOAD_DIR / f"{timestamp}{uploaded_file.name}"
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Save metadata
    files_data = load_files()
    files_data["files"].append({
        "name": file_path.name,
        "original_name": uploaded_file.name,
        "path": str(file_path),
        "size": os.path.getsize(file_path),
        "uploaded_by": st.session_state.username,
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": os.path.splitext(uploaded_file.name)[1].lower()
    })
    save_files(files_data)
    return file_path

def get_download_link(file_path, file_meta):
    """Generate download link for a file"""
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_meta["original_name"]}" style="text-decoration:none;color:#009688;background-color:white;padding:5px 10px;border-radius:5px;">📥 Download</a>'

def filter_files(files_data, search_term):
    """Filter files based on search term"""
    if not search_term:
        return files_data["files"]
    pattern = re.compile(search_term, re.IGNORECASE)
    return [f for f in files_data["files"] if pattern.search(f["original_name"])]

def handle_logout():
    """Handle logout with animation"""
    with st.spinner("Logging out..."):
        time.sleep(0.5)  # Short delay for smooth transition
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()

# Main App
if not st.session_state.authenticated:
    # Authentication UI
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.title("📁 File Share Hub")
    st.markdown('</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        with st.container():
            st.markdown('<div class="auth-form">', unsafe_allow_html=True)
            login_form()
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        with st.container():
            st.markdown('<div class="auth-form">', unsafe_allow_html=True)
            signup_form()
            st.markdown('</div>', unsafe_allow_html=True)
else:
    # Main app UI
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    # Create a container for the header with logout button
    header_col1, header_col2 = st.columns([4, 1])
    with header_col1:
        st.title("📁 File Share Hub")
        st.markdown(f"<h3 class='upload-header'>Welcome, {st.session_state.username}!</h3>", unsafe_allow_html=True)
    
    with header_col2:
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("🚪 Logout", key="logout", use_container_width=False):
            handle_logout()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📤 Upload Files", "📥 Download Files"])

    with tab1:
        st.markdown("<h4 style='color: #009688;'>Upload New Files</h4>", unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "Drag and drop files here or click to choose",
            type=None,
            accept_multiple_files=True,
            key="file_uploader"
        )

        if uploaded_files:
            for uploaded_file in uploaded_files:
                with st.spinner(f"Uploading {uploaded_file.name}..."):
                    file_path = save_file(uploaded_file)
                    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            st.balloons()

    with tab2:
        st.markdown("<h4 style='color: #009688;'>Available Files</h4>", unsafe_allow_html=True)
        search_term = st.text_input("🔍 Search files", key="search")
        
        st.markdown("<div class='file-list'>", unsafe_allow_html=True)
        
        files_data = load_files()
        filtered_files = filter_files(files_data, search_term)
        
        if not filtered_files:
            if search_term:
                st.info("No matching files found.")
            else:
                st.info("No files available. Upload a file to get started!")
        else:
            file_types = list(set(f["type"] for f in filtered_files if f["type"]))
            selected_type = st.selectbox("Filter by type", ["All"] + file_types)
            
            displayed_files = filtered_files
            if selected_type != "All":
                displayed_files = [f for f in filtered_files if f["type"] == selected_type]
            
            for file_meta in displayed_files:
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                with col1:
                    st.write(f"📄 {file_meta['original_name']}")
                with col2:
                    size_kb = file_meta['size'] / 1024
                    if size_kb > 1024:
                        st.write(f"Size: {size_kb/1024:.2f} MB")
                    else:
                        st.write(f"Size: {size_kb:.1f} KB")
                with col3:
                    st.write(f"Uploaded by: {file_meta['uploaded_by']}")
                with col4:
                    st.markdown(get_download_link(file_meta['path'], file_meta), unsafe_allow_html=True)
                st.divider()

        st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #009688;'>Made with ❤️ using Streamlit</p>", unsafe_allow_html=True) 