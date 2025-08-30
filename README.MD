# 🔔 Subscription Renewal Reminders

A Flask-based web application that demonstrates **webhook implementation** for automated subscription renewal notifications. This project showcases how webhooks can be used to create real-time, event-driven communication between systems for subscription management.

## 📋 Table of Contents

- [What are Webhooks?](#what-are-webhooks)
- [Project Overview](#project-overview)
- [Architecture & Flow](#architecture--flow)
- [Features](#features)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)

## 🎯 What are Webhooks?

**Webhooks** are HTTP callbacks that enable real-time communication between different systems. Instead of constantly polling for updates (which wastes resources), webhooks allow one system to automatically notify another when specific events occur.

### Key Benefits:
- **Real-time notifications**: Instant event-driven communication
- **Resource efficient**: No need for constant polling
- **Scalable**: Handles multiple events simultaneously
- **Decoupled architecture**: Systems remain independent

### How Webhooks Work:

```
┌─────────────┐    Event Occurs    ┌─────────────┐
│   System A  │ ──────────────────→ │   System B  │
│ (Publisher) │                    │ (Subscriber)│
└─────────────┘                    └─────────────┘
                                           │
                                           ▼
                                   HTTP POST Request
                                   (with event data)
```

## 🚀 Project Overview

This application simulates a subscription management system where:

1. **External systems** (subscription services) send webhook notifications when subscriptions are about to expire
2. **Our Flask app** receives these webhooks and processes renewal reminders
3. **Email notifications** with AI-generated messages are sent to users
4. **Dashboard interface** provides visual subscription management

## 🏗️ Architecture & Flow

```
┌─────────────────┐    Webhook POST     ┌─────────────────┐
│  Subscription   │ ─────────────────→  │   Flask App     │
│   Service       │  /webhook/sub...    │  (This Project) │
│ (Netflix, etc.) │                     └─────────────────┘
└─────────────────┘                              │
                                                 ▼
                                    ┌─────────────────┐
                                    │  Email Service  │
                                    │  (Flask-Mail)   │
                                    └─────────────────┘
                                                 │
                                                 ▼
                                    ┌─────────────────┐
                                    │  User's Email   │
                                    │   📧 Reminder   │
                                    └─────────────────┘
```

### Detailed Flow Diagram:

```
📱 External System          🌐 Flask App          📧 Email System          👤 User
      │                         │                      │                     │
      │ 1. Subscription Event   │                      │                     │
      │────────────────────────→│                      │                     │
      │                         │ 2. Process Webhook   │                     │
      │                         │────────────────────→ │                     │
      │                         │                      │ 3. Generate AI Msg │
      │                         │                      │──────────────────→ │
      │                         │                      │                     │
      │                         │                      │ 4. Send Email      │
      │                         │                      │──────────────────→ │
      │                         │ 5. Return Response   │                     │
      │←────────────────────────│                      │                     │
```

## ✨ Features

### Core Webhook Functionality
- **RESTful webhook endpoint** (`/webhook/subscription`) for receiving subscription events
- **Event processing** with subscription validation and expiry checking
- **Automated email notifications** with HTML templates
- **AI-powered message generation** for personalized reminders

### User Interface
- **Modern dashboard** with subscription overview
- **Real-time updates** with auto-refresh functionality
- **Interactive management** (renew/cancel subscriptions)
- **Responsive design** using Bootstrap 5

### Email System
- **HTML email templates** with professional styling
- **Dynamic content** based on subscription status
- **Visual indicators** for urgency levels
- **Call-to-action buttons** for easy renewal

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Virtual environment (recommended)
- SMTP server access for email functionality

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd SubscriptionRenewalReminders
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv envSubscripNotifWH
   
   # On Windows
   envSubscripNotifWH\Scripts\activate
   
   # On macOS/Linux
   source envSubscripNotifWH/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure email settings**
   Create a `.env` file with your email configuration:
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=noreply@yourdomain.com
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the dashboard**
   Open your browser and navigate to `http://localhost:5000`

### Docker Setup

1. **Build the Docker image**
   ```bash
   docker build -t subscription-reminders .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 subscription-reminders
   ```

## 📊 Usage

### Dashboard Interface
- View all active subscriptions with expiry dates
- Monitor days remaining for each subscription
- Renew or cancel subscriptions with one click
- Visual indicators for urgent renewals

### Webhook Testing
Use tools like **Postman** or **curl** to test the webhook endpoint:

```bash
curl -X POST http://localhost:5000/webhook/subscription \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'
```

### Expected Response:
```json
{
  "status": "Reminder sent"
}
```

## 🔌 API Endpoints

### Webhook Endpoint
- **URL**: `/webhook/subscription`
- **Method**: `POST`
- **Content-Type**: `application/json`

**Request Body:**
```json
{
  "user_id": "string"
}
```

**Responses:**
- `200`: Reminder sent successfully
- `404`: User not found
- `400`: Invalid request format

### Web Interface Endpoints
- **GET** `/` - Dashboard view
- **POST** `/renew/<user_id>` - Renew subscription
- **POST** `/cancel/<user_id>` - Cancel subscription

## 📁 Project Structure

```
SubscriptionRenewalReminders/
├── main.py                     # Flask application entry point
├── templates/
│   ├── dashboard.html          # Main dashboard interface
│   └── reminder_email.html     # Email notification template
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── .gitignore                  # Git ignore patterns
├── .github/
│   └── workflows/
│       └── ci_cd_workflow.yml  # GitHub Actions CI/CD
└── README.md                   # Project documentation
```

## 🔧 Technologies Used

### Backend
- **Flask**: Lightweight web framework for Python
- **Flask-Mail**: Email sending capabilities
- **Threading**: Background webhook simulation
- **DateTime**: Subscription expiry management

### Frontend
- **Bootstrap 5**: Modern responsive CSS framework
- **Bootstrap Icons**: Comprehensive icon library
- **Jinja2**: Template engine for dynamic content
- **Custom CSS**: Enhanced styling and animations

### DevOps & Deployment
- **Docker**: Containerization for consistent deployment
- **GitHub Actions**: Automated CI/CD pipeline
- **Gunicorn**: Production WSGI servers

## 🎨 Key Code Concepts

### Webhook Implementation
The core webhook functionality demonstrates several important concepts:

**Event-Driven Architecture**: The application responds to external events rather than polling for changes.

```python
@app.route('/webhook/subscription', methods=['POST'])
def subscription_webhook():
    data = request.json
    user_id = data.get('user_id')
    # Process the webhook event...
```

**Conditional Logic**: Only sends reminders when specific conditions are met (≤ 7 days remaining).

**Error Handling**: Proper HTTP status codes and error responses for robust communication.

### AI Message Generation
The application includes a simple AI message generator that creates personalized reminder messages:

```python
def generate_ai_message(service, days_left):
    templates = [
        f"Your {service} subscription expires in {days_left} days! Renew now to avoid interruption.",
        f"Only {days_left} days left on your {service} subscription. Don't lose access!",
        f"Heads up! Your {service} subscription ends in {days_left} days. Renew today!"
    ]
    return random.choice(templates)
```

### Email Integration
The application demonstrates how to integrate email functionality with webhook processing:

- **HTML email templates** for professional appearance
- **Dynamic content injection** based on subscription data
- **Error handling** for email delivery failures

## 🔄 Webhook Workflow

1. **Event Trigger**: External subscription service detects upcoming expiry
2. **Webhook Call**: Service sends HTTP POST to `/webhook/subscription`
3. **Data Validation**: Flask app validates user and subscription data
4. **Condition Check**: Verifies if reminder is needed (≤ 7 days)
5. **Message Generation**: Creates personalized AI reminder message
6. **Email Delivery**: Sends HTML email notification to user
7. **Response**: Returns success/failure status to calling service

## 🚦 Running in Production

### Environment Variables
Set up the following environment variables for production:

```env
FLASK_ENV=production
MAIL_SERVER=your-smtp-server
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@domain.com
MAIL_PASSWORD=your-secure-password
SECRET_KEY=your-secret-key-here
```

### Security Considerations
- Use environment variables for sensitive configuration
- Implement webhook signature verification in production
- Add rate limiting for webhook endpoints
- Use HTTPS for all webhook communications
- Validate and sanitize all incoming webhook data

## 🧪 Testing Webhooks

### Manual Testing
1. Start the Flask application
2. Use curl or Postman to send webhook requests
3. Monitor console output for email confirmations
4. Check dashboard for subscription updates

### Automated Testing
The project includes GitHub Actions workflow for:
- **Unit testing** with pytest
- **Code quality** checks with flake8
- **Security scanning** with bandit
- **Dependency vulnerability** checks with safety

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Future Enhancements

- **Database integration** (PostgreSQL/MySQL) for persistent storage
- **Webhook signature verification** for enhanced security
- **User authentication** and session management
- **Multiple notification channels** (SMS, Slack, Discord)
- **Advanced AI messaging** with machine learning
- **Subscription analytics** and reporting
- **Mobile app integration**
- **Payment gateway integration** for automatic renewals

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page for existing solutions
2. Create a new issue with detailed information
3. Contact the development team

---

**Built with ❤️ for learning webhook implementations and subscription management**