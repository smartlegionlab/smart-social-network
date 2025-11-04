# Smart Social Network <sup>v1.0.0</sup>

## 🌐 Modern Django-Powered Social Network Platform

A comprehensive, feature-rich social networking platform built from the ground up with Django. 
Smart Social Network offers a complete suite of social features with real-time interactions.

**Development Note:** The complete development history, including experimental features, iterations, 
and testing phases, was conducted in a private repository.
The full development history with over 1000+ commits is available upon request for serious collaborators or potential employers.

![Smart Social Network](https://github.com/smartlegionlab/smart-social-network/raw/master/data/images/smart_social_network.png)

---

[![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-social-network)](https://github.com/smartlegionlab/smart-social-network)
[![GitHub license](https://img.shields.io/github/license/smartlegionlab/smart-social-network)](https://github.com/smartlegionlab/smart-social-network/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/smartlegionlab/smart-social-network)](https://github.com/smartlegionlab/smart-social-network/)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-social-network?style=social)](https://github.com/smartlegionlab/smart-social-network/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-social-network?style=social)](https://github.com/smartlegionlab/smart-social-network/network/members)

---

## 📋 Table of Contents

1. [🌟 Key Features](#-key-features)
2. [🏗️ Architecture & Tech Stack](#-architecture--tech-stack)
3. [🚀 Quick Start](#-quick-start)
4. [🔐 Authentication & Security](#-authentication--security)
5. [💬 Social Features](#-social-features)
6. [📱 Real-Time Communication](#-real-time-communication)
7. [🎵 Media Management](#-media-management)
8. [⚙️ Administration](#-administration)
9. [📊 System Monitoring](#-system-monitoring)
10. [🛠️ Installation Guide](#-installation-guide)
11. [📜 License](#-license)
12. [⚠️ Disclaimer](#-disclaimer)

---

## 🌟 Key Features

### 🔐 Advanced Authentication System
- **Secure and minimized** Registration & Login
- **Custom Two-Factor Authentication** via Telegram bot integration
- **Password Recovery** with Telegram bot verification
- **Session Management** with comprehensive login history tracking

### 👥 Complete User Profiles
- **Customizable Profiles** with avatar management (upload/reset to default)
- **Real-time User Status Indicators** (online/offline)
- **Profile Visits Tracking** with management
- **Advanced Friends System** with request management and mutual connections
- **Granular Privacy Controls** for profile visibility settings

### 📝 Content Management
- **Personal Walls** for user posts
- **Rich Text Posts** with emoji support (51+ integrated emojis)
- **Post Interactions** - likes, comments, editing, deletion
- **Intelligent Rate Limiting** for posts, comments and interactions

### 💬 Advanced Messaging System
- **Real-time Chat** with WebSocket integration for instant messaging
- **Group Chats & Direct Messaging** with flexible participant management
- **Message Editing** with instant synchronization across all users
- **Comprehensive Chat Management** - mute, archive, delete, restore functionality
- **Typing Indicators** for enhanced communication
- **Chat Categories** - organized into active, archived or deleted sections

### 🎵 Multimedia Integration
- **Smart Audio Player** with visualizations and audio management
- **Image Gallery** with comments, likes and privacy controls
- **Document Management** with visibility settings and sharing capabilities
- **Cross-user Media Sharing** with add audio to playlist
- **Media Statistics** - analytics on likes

### 🎮 Applications
- **Integrated Apps Platform** for future extensions and integrations
- **Built-in Smart Password Manager** for secure credential management
- **Expandable Ecosystem** - designed for additional applications

### 🔍 Additional Features
- **User Search** with instant results
- **News Section** with admin-published articles and engagement metrics
- **Visits System** - track who visited your profile and who you visited
- **Notifications Center** - comprehensive management of all alerts
- **Main Menu Indicators** - real-time notifications for new posts, messages, friend requests or profile visits

---

## 🏗️ Architecture & Tech Stack

### Backend Technologies
- **Django 5++** - Full-stack web framework with optimized performance
- **PostgreSQL 15+** - Production-grade relational database
- **Redis** - High-performance caching and message broker
- **Celery** - Distributed task query for asynchronous processing
- **WebSocket** - Real-time bidirectional communication
- **Django Channels** - WebSocket integration for real-time features

### Frontend Technologies
- **Responsive Design** - Mobile-first approach with cross-device compatibility
- **Dark Theme** - Modern UI/UX design throughout the application
- **JavaScript** - Dynamic client-side interactions
- **CSS3** - Advanced styling with animations and transitions
- **WebSocket Client** - Real-time frontend-backend communication

### Security Framework
- **Custom Two-Factor Authentication** - Proprietary implementation via Telegram
- **Custom Rate Limiting** - Comprehensive protection against abuse and spam
- **SQL Injection Protection** - Django ORM security with parameterized queries
- **CSRF Protection** - Cross-site request forgery prevention

---

## 🚀 Quick Start

### System Requirements

#### Recommended Development Environment
- **Operating System**: Arch Linux (recommended) or other Linux distributions
- **Python**: 3.10 or higher
- **Database**: PostgreSQL 15+
- **Cache/Broker**: Redis/Valkey
- **IDE**: PyCharm Professional (recommended) or Visual Studio Code

### Package Installation

#### Install Required Packages

**For Redis:**
```bash
sudo pacman -S redis
sudo systemctl start redis
sudo systemctl enable redis
```

**For Valkey (alternative):**
```bash
sudo systemctl start valkey
sudo systemctl enable valkey
```

### Database Setup

#### PostgreSQL Installation

```bash
# Install PostgreSQL
sudo pacman -S postgresql

# Initialize database cluster
sudo su - postgres -c "initdb --locale en_US.UTF-8 -D '/var/lib/postgres/data'"

# Start and enable PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Access PostgreSQL shell
sudo -u postgres psql
```

Execute the following SQL commands to create the database:
```sql
-- Create main database with proper encoding
CREATE DATABASE smart_social_network_db
    OWNER postgres
    ENCODING 'UTF-8'
    LC_COLLATE 'en_US.UTF-8'
    LC_CTYPE 'en_US.UTF-8'
    TEMPLATE template0;

-- Exit PostgreSQL
\q
```

### Project Installation

#### Clone and Setup Repository
```bash
# Clone the repository
git clone https://github.com/smartlegionlab/smart-social-network.git
cd smart-social-network

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Environment Configuration

Create a `.env` file in the project root directory with the following content:

```ini
# Core Settings
DJANGO_ENV=development
SECRET_KEY=your-generated-secret-key-here
DEBUG=True

# Database Configuration
DB_NAME=smart_social_network_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis/Celery Settings
REDIS_URL=redis://localhost:6379/1
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Development Tools
DEBUG_TOOLBAR_ENABLED=True
```

**Important**: Replace `your-generated-secret-key-here` with an actual secret key. You can generate one using:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Database Initialization

#### Apply Migrations and Load Data
```bash
# Apply database migrations
python manage.py migrate

# Load initial data fixtures
python manage.py loaddata data/fixtures/cities.json
python manage.py loaddata data/fixtures/emoji.json

# Create administrator account
python manage.py createsuperuser
```

### Running the Application

#### Development Mode
Start the application in development mode with these commands:

**Terminal 1 - Django Server:**
```bash
python manage.py runserver
```

**Terminal 2 - Celery Worker:**
```bash
celery -A smart_social_network worker --loglevel=info
```

**Terminal 3 - Celery Beat (optional):**
```bash
celery -A smart_social_network beat --loglevel=info
```

### PyCharm Configuration

For optimal development experience in PyCharm:
- **Database User**: `postgres`
- **Database Password**: `postgres`
- **Database Name**: `smart_social_network_db`
- **Host**: `localhost`
- **Port**: `5432`

### Access the Application

Once all services are running, access the application at:
**http://localhost:8000**

The admin interface will be available at:
**http://localhost:8000/admin**

---

## 🔐 Authentication & Security

### Custom Two-Factor Authentication System
- **Proprietary Implementation** - Unique authentication system developed from scratch
- **Telegram Bot Integration** - Secure code delivery through Telegram
- **Time-based Code Generation** - Custom algorithm implementation
- **Secure Session Management** - Comprehensive session tracking and control
- **Login History Tracking** - Detailed IP logging and device information

### Password Management
- **Built-in Password Generator** - Cryptographically secure password generation
- **Secure Password Reset** - Telegram-based verification system

### Privacy & Data Protection
- **Visit History Management** - Comprehensive tracking and control
- **Content Privacy Settings** - Flexible content visibility options

---

## 💬 Social Features

### User Interaction System
- **Advanced Friend System** - Mutual connections with request management
- **Profile Visits** - Tracking with timestamps
- **Post Interactions** - Likes and comments
- **Notification System** - Comprehensive activity notifications

### Content Management System
- **Rich Text Editor** - Advanced editing with emoji support
- **Post Management** - Create, edit, delete
- **Comment System** - Nested replies with moderation tools

### Discovery & Exploration
- **User Search** - Instant results with advanced filtering
- **Profile Discovery** - Multiple discovery channels and algorithms
- **Content Exploration**

---

## 📱 Real-Time Communication

### Chat & Messaging
- **Instant Messaging** - Real-time delivery with WebSocket integration
- **Group Chats** - Multi-participant conversations with management tools
- **Message Editing** - Live synchronization across all connected clients

### Notification System
- **Real-time Alerts** - Instant notifications for all interactions
- **Notification Center** - Centralized management and organization

### Live Updates
- **Online Status** - user presence indicators
- **Typing Indicators** - Live typing notifications in chats
- **Real-time Counters** - Live update of all statistics

---

## 🎵 Media Management

### Audio System
- **Smart Audio Player** - Advanced player with visualizations
- **Music sharing** - Music sharing
- **Audio Analytics** - Popularity tracking

### Image Management
- **Photo Uploads** - Optimized uploads with compression
- **Image Comments** - Interaction features
- **Privacy Controls** - Flexible visibility settings
- **Shareable Links** - External sharing capabilities

### Document Management
- **File Uploads** - Type validation and security checks
- **Document Sharing** - Permission-based sharing system

---

## ⚙️ Administration

- **Django and Custom Admin panel** protected from unauthorized access on request level

### Django Admin Interface
- **User Management** - Advanced user controls
- **Content Moderation** - Comprehensive content review tools
- **System Configuration** - Centralized configuration management

### Custom Admin Panel
- **Profile Management** - Detailed user profile views and controls
- **Login History** - IP analysis and security monitoring
- **Report System** - User complaint management and resolution

### Moderation Tools
- **User Reports** - Comprehensive report management system
- **Content Review** - Structured review workflow process
- **Ban Management**
- **Appeal Process** - User appeal and resolution system

### Global Settings
- **Application Configuration** - Site name, description, contact information
- **Telegram Bot Settings** - Token and URL configuration
- **System Information** - Real-time server monitoring and metrics

---

## 📊 System Monitoring

### Real-time System Information
```
System boot time: 17.09.2025 20:33:14
CPU number of physical cores: 6
CPU number of logical cores: 12
CPU load system wide: 13.2%
Memory (total): 15.5gb
Memory (available): 10.8gb
Memory (free): 5.6gb
Memory (in use): 4.2gb
Memory (percentage of load): 30.3%
Disk: Total: 145.5gb | Busy: 32.0gb | Available: 112.5gb | Utilization percentage: 22.2%
```

### Performance Optimization
- **Database Optimization** - N+1 query solutions and performance tuning
- **Caching Strategy** - Redis integration for optimal performance
- **Asset Optimization** - Fast loading and efficient resource usage
- **Code Refactoring** - Maintainable and optimized codebase

---

## ⚠️ Disclaimer

**Important Legal Notice:** This software is provided for educational and research purposes only. The Smart Social Network platform is currently in active development and is not intended for production use.

### Usage Restrictions:
- 🚫 **Not for Production Use** - This is a development version with potential security vulnerabilities
- 🚫 **No Warranty** - The software is provided "as is" without any guarantees
- 🚫 **Legal Compliance** - Users are solely responsible for ensuring compliance with all applicable laws and regulations
- 🚫 **Liability** - The author assumes no responsibility for any misuse or illegal activities conducted using this software

### User Responsibility:
By using this software, you acknowledge and agree that:
- You are solely responsible for any content posted or shared through the platform
- You will comply with all local, national, and international laws
- You understand this is experimental software and may contain bugs or security issues
- The author cannot be held liable for any damages or legal issues arising from use

### Security Notice:
While significant effort has been made to implement security measures, this software:
- Has not undergone formal security auditing
- May contain vulnerabilities
- Should not be used with sensitive or personal data
- Is intended for research and development purposes only

---

## 📜 License

BSD 3-Clause License

Copyright (c) 2025, Alexander Suvorov

```
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

---

## 🌟 Development Statistics

- **1000+ Commits** - Comprehensive development history
- **6+ Months** - Intensive active development period

> **Note**: This platform is still under active development. The system features a proprietary two-factor authentication system with Telegram integration. This list of features is not exhaustive - the platform includes many additional capabilities beyond those described here. The platform is designed for scalability, maintainability, and excellent user experience across all devices, but should be used responsibly and in accordance with all applicable laws.

---

**Created by Alexander Suvorov**

[![GitHub](https://img.shields.io/badge/GitHub-@smartlegionlab-blue?logo=github)](https://github.com/smartlegionlab)
[![Email](https://img.shields.io/badge/Email-smartlegiondev@gmail.com-blue?logo=mail.ru)](mailto:smartlegiondev@gmail.com)
