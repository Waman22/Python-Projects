
import random

from flask import Flask, render_template, request, flash, session, redirect, url_for

'''This code creates a simple web application that generates a One-Time Password (OTP) and allows users to verify it.
OTP Generation: The generate_otp function creates a random numeric OTP of a specified length (default is 6 digits).'''

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def generate_otp(length=6):
    """Generate a random numeric OTP of the specified length."""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


@app.route('/')
def generate_otp_route():
    otp = generate_otp()  # Call the OTP function
    session['otp'] = otp  # Store the OTP in the session
    flash(f'Your OTP is: {otp}', 'info')  # Display the OTP (for demo purposes)
    return render_template('verify_otp.html')  # Render a template for OTP verification

@app.route('/verify_otp', methods=['POST'])
def verify_otp_route():
    entered_otp = request.form.get('otp')  # Get OTP from form input
    if 'otp' in session and entered_otp == session['otp']:
        flash('OTP verified successfully!', 'success')
        session.pop('otp', None)  # Clear OTP from the session
        return redirect(url_for('dashboard'))  # Redirect to another page (e.g., dashboard)
    else:
        flash('Invalid OTP. Please try again.', 'danger')
        return render_template('verify_otp.html')  # Re-render the OTP verification page

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')  # Re-render the OTP verification page


if __name__ == '__main__':
    app.run(debug=True) 
