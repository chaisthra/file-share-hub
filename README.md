# File Share Hub 📁

A modern, secure file sharing application built with Python and Streamlit. Features user authentication, file upload/download capabilities, and a clean, intuitive interface.

![File Share Hub Screenshot](screenshot.png)

## 🌟 Features

- **User Authentication**
  - Secure signup and login
  - Password hashing
  - Session management
  - Animated signup process

- **File Management**
  - Multiple file upload support
  - Drag-and-drop interface
  - File type filtering
  - Search functionality
  - File size display
  - Secure file storage

- **Modern UI**
  - Clean, responsive design
  - Progress animations
  - Intuitive navigation
  - File preview
  - Sort and filter options

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/file-share-hub.git
   cd file-share-hub
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run file_sharing_app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - Default admin credentials:
     - Username: admin
     - Password: password123

## 📁 Project Structure

```
file-share-hub/
├── file_sharing_app.py    # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── data/                 # User and file metadata storage
│   └── .gitkeep
└── uploads/             # File storage directory
    └── .gitkeep
```

## 🔒 Security Features

- Password hashing using SHA-256
- Secure file storage
- Session management
- Input validation
- Protected file access

## 🛠️ Development

1. **Setup Development Environment**
   ```bash
   git clone https://github.com/yourusername/file-share-hub.git
   cd file-share-hub
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run in Development Mode**
   ```bash
   streamlit run file_sharing_app.py
   ```

## 🚀 Deployment

The application can be deployed on various platforms:

1. **Streamlit Cloud**
   - Connect your GitHub repository
   - Select the repository and branch
   - Deploy with one click

2. **Heroku**
   - Create a new Heroku app
   - Connect your GitHub repository
   - Deploy the main branch

3. **Custom Server**
   - Install requirements
   - Set up a reverse proxy
   - Run with streamlit

## 📝 Configuration

The application uses environment variables for configuration:
- Create a `.env` file in the root directory
- Add necessary configuration variables

Example `.env`:
```env
ADMIN_PASSWORD=your_secure_password
UPLOAD_PATH=/path/to/uploads
```

## 🤝 Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Contributors and users of the application

---

Made with ❤️ using Python and Streamlit 