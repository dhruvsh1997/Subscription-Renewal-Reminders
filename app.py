# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import datetime
import random
import threading
import time
from flask_mail import Mail, Message

app = Flask(__name__)

# Email configuration (use your actual credentials in production)
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-password'
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@subscription-reminder.com'

mail = Mail(app)

# Simulated database
subscriptions = {
    "user123": {
        "service": "Netflix",
        "expiry": datetime.datetime.now() + datetime.timedelta(days=5),
        "email": "user@example.com",
        "status": "active"
    },
    "user456": {
        "service": "Spotify",
        "expiry": datetime.datetime.now() + datetime.timedelta(days=12),
        "email": "user2@example.com",
        "status": "active"
    },
    "user789": {
        "service": "Adobe Creative Cloud",
        "expiry": datetime.datetime.now() + datetime.timedelta(days=2),
        "email": "user3@example.com",
        "status": "active"
    }
}

# AI message generator
def generate_ai_message(service, days_left):
    templates = [
        f"Your {service} subscription expires in {days_left} days! Renew now to avoid interruption.",
        f"Only {days_left} days left on your {service} subscription. Don't lose access!",
        f"Heads up! Your {service} subscription ends in {days_left} days. Renew today!"
    ]
    return random.choice(templates)

# Send email with HTML template
def send_reminder_email(user_email, service, days_left, message):
    msg = Message(
        subject=f"Action Required: {service} Subscription Renewal",
        recipients=[user_email],
        html=render_template(
            'reminder_email.html',
            service=service,
            days_left=days_left,
            message=message,
            renewal_link="https://example.com/renew"
        )
    )
    mail.send(msg)

# Webhook endpoint
@app.route('/webhook/subscription', methods=['POST'])
def subscription_webhook():
    data = request.json
    user_id = data.get('user_id')
    
    if user_id not in subscriptions:
        return jsonify({"error": "User not found"}), 404
    
    sub = subscriptions[user_id]
    days_left = (sub['expiry'] - datetime.datetime.now()).days
    
    if days_left <= 7 and sub['status'] == 'active':  # Trigger condition
        message = generate_ai_message(sub['service'], days_left)
        send_reminder_email(sub['email'], sub['service'], days_left, message)
        print(f"Email sent to {sub['email']}: {message}")
        return jsonify({"status": "Reminder sent"}), 200
    
    return jsonify({"status": "No reminder needed"}), 200

# Simulate external system triggering webhook
def simulate_webhook():
    while True:
        time.sleep(86400)  # Daily check
        for user_id in subscriptions:
            # Simulate webhook call
            with app.test_client() as client:
                client.post('/webhook/subscription', json={"user_id": user_id})

# UI Routes
@app.route('/')
def dashboard():
    # Calculate days left for each subscription
    subs_data = []
    for user_id, sub in subscriptions.items():
        days_left = (sub['expiry'] - datetime.datetime.now()).days
        subs_data.append({
            'user_id': user_id,
            'service': sub['service'],
            'expiry': sub['expiry'].strftime('%Y-%m-%d'),
            'days_left': days_left,
            'email': sub['email'],
            'status': sub['status']
        })
    
    return render_template('dashboard.html', subscriptions=subs_data)

@app.route('/renew/<user_id>', methods=['POST'])
def renew_subscription(user_id):
    if user_id in subscriptions:
        subscriptions[user_id]['expiry'] = datetime.datetime.now() + datetime.timedelta(days=30)
        subscriptions[user_id]['status'] = 'active'
        return redirect(url_for('dashboard'))
    return "User not found", 404

@app.route('/cancel/<user_id>', methods=['POST'])
def cancel_subscription(user_id):
    if user_id in subscriptions:
        subscriptions[user_id]['status'] = 'cancelled'
        return redirect(url_for('dashboard'))
    return "User not found", 404

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    import os
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Start simulation in background
    threading.Thread(target=simulate_webhook, daemon=True).start()
    app.run(port=5000, debug=True)