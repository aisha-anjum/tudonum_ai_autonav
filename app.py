from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, render_template, render_template_string
from openai import OpenAI

# Load environment
load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ---------- GENERAL USER ROUTES ----------
general_user_routes = {
    "account creation": "/account",
    "task booking": "/task-booking",
    "food delivery": "/food-delivery",
    "taxi booking": "/taxi-booking",
    "grocery": "/grocery",
    "e-commerce": "/ecommerce",
    "wallet": "/wallet",
    "consultation booking": "/consultation-booking",
    "profile setting": "/profile-setting"
}

# ---------- SERVICE PROVIDER ROUTES ----------
service_provider_routes = {
    "profile completion": "/provider/profile-completion",
    "vendor profile": "/provider/vendor-profile",
    "food partner": "/provider/food-partner",
    "driver registration": "/provider/driver-registration",
    "e-commerce store setup": "/provider/store-setup",
    "marketplace": "/provider/marketplace",
    "classified vendors": "/provider/classified-vendors"
}

# Shared styling
base_style = """
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white; text-align: center;
            min-height: 100vh; display: flex;
            flex-direction: column; justify-content: center; align-items: center;
        }
        h1 { font-size: 40px; margin-bottom: 15px; }
        p { font-size: 18px; max-width: 650px; line-height: 1.6; }
        a {
            margin-top: 25px; display: inline-block;
            padding: 10px 25px; background: rgba(255,255,255,0.2);
            color: #fff; border-radius: 8px; text-decoration: none;
            transition: all 0.3s ease;
        }
        a:hover { background: #fff; color: #764ba2; }
    </style>
"""

# ---------- STATIC DEMO PAGES ----------
@app.route("/")
def home():
    return render_template("index.html")


# --- General User Pages ---
@app.route("/account")
def account(): return render_template_string(base_style + "<h1>Account Creation</h1><p>Create your Tudo Num account.</p>")

@app.route("/task-booking")
def task_booking(): return render_template_string(base_style + "<h1>Task Booking</h1><p>Book any home or professional service easily.</p>")

@app.route("/food-delivery")
def food_delivery(): return render_template_string(base_style + "<h1>Food Delivery</h1><p>Order meals from your favorite restaurants.</p>")

@app.route("/taxi-booking")
def taxi_booking(): return render_template_string(base_style + "<h1>Taxi Booking</h1><p>Book rides instantly via Tudo Num Transport.</p>")

@app.route("/grocery")
def grocery(): return render_template_string(base_style + "<h1>Grocery</h1><p>Shop groceries and essentials online.</p>")

@app.route("/ecommerce")
def ecommerce(): return render_template_string(base_style + "<h1>E-Commerce</h1><p>Shop electronics, fashion, and more.</p>")

@app.route("/wallet")
def wallet(): return render_template_string(base_style + "<h1>Wallet</h1><p>Track your balance and transactions.</p>")

@app.route("/consultation-booking")
def consultation_booking(): return render_template_string(base_style + "<h1>Consultation Booking</h1><p>Book health or professional consultations.</p>")

@app.route("/profile-setting")
def profile_setting(): return render_template_string(base_style + "<h1>Profile Settings</h1><p>Update your preferences and account info.</p>")

# --- Service Provider Pages ---
@app.route("/provider/profile-completion")
def profile_completion(): return render_template_string(base_style + "<h1>Profile Completion</h1><p>Complete your provider verification and details.</p>")

@app.route("/provider/vendor-profile")
def vendor_profile(): return render_template_string(base_style + "<h1>Vendor Profile</h1><p>Manage your vendor details and analytics.</p>")

@app.route("/provider/food-partner")
def food_partner(): return render_template_string(base_style + "<h1>Food Partner</h1><p>Register as a restaurant or food partner.</p>")

@app.route("/provider/driver-registration")
def driver_registration(): return render_template_string(base_style + "<h1>Driver & Vehicle Registration</h1><p>Register your vehicle and start earning.</p>")

@app.route("/provider/store-setup")
def store_setup(): return render_template_string(base_style + "<h1>E-Commerce Store Setup</h1><p>Set up your online store and upload products.</p>")

@app.route("/provider/marketplace")
def marketplace(): return render_template_string(base_style + "<h1>Marketplace</h1><p>List your services in the Tudo marketplace.</p>")

@app.route("/provider/classified-vendors")
def classified_vendors(): return render_template_string(base_style + "<h1>Classified Vendors</h1><p>Post items for sale like phones or laptops.</p>")

# ---------- AI Auto-Navigation ----------
@app.route("/api/ai-route", methods=["POST"])
def ai_route():
    data = request.get_json()
    user_query = data.get("userQuery", "")

    # Context-rich descriptions for semantic understanding
    general_user_info = """
    General user modules:
    1. Account creation – for users creating new accounts.
    2. Task booking – for users booking home or professional services (e.g., plumber, electrician).
    3. Food delivery – for ordering meals from restaurants, hotels, or cafes.
    4. Taxi booking – for booking rides, cars, or autos.
    5. Grocery – for buying daily essentials and grocery items online.
    6. E-commerce – for shopping online for electronics, clothing, or household items.
    7. Wallet – for viewing balance, payments, and transaction history.
    8. Consultation booking – for scheduling health or expert consultations.
    9. Profile setting – for changing user details and preferences.
    """

    service_provider_info = """
    Service provider modules:
    1. Profile completion – for providers completing verification and personal details.
    2. Vendor profile – for businesses or sellers managing their store profiles.
    3. Food partner – for restaurants, hotels, or cafes registering to deliver food.
    4. Driver registration – for drivers or riders registering their vehicles for rides or delivery.
    5. E-commerce store setup – for merchants or vendors creating an online store to sell products.
    6. Marketplace – for providers listing services on the Tudo marketplace.
    7. Classified vendors – for individuals selling used or personal items like phones or laptops.
    """

    prompt = f"""
    The user said: "{user_query}".
    You are Tudo Num's AI AutoNavigator. Your job is to understand the user's *intent* 
    and decide which module they want to access — even if they phrase it differently.

    Use common sense and semantic understanding.
    For example:
    - "I want to register my hotel" → Service Provider → Food Partner
    - "I want to open a restaurant" → Service Provider → Food Partner
    - "I want to register as a driver" → Service Provider → Driver Registration
    - "I want to sell clothes online" → Service Provider → E-commerce Store Setup
    - "I want to order food" → General User → Food Delivery
    - "I need a plumber" → General User → Task Booking
    - "I want to book a taxi" → General User → Taxi Booking

    {general_user_info}
    {service_provider_info}

    Reply *strictly* in JSON format:
    {{
        "role": "general_user" or "service_provider",
        "module": "<exact module name from above>"
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        import json
        ai_data = json.loads(response.choices[0].message.content)
        role = ai_data.get("role")
        module = ai_data.get("module", "").lower()

        if role == "general_user" and module in general_user_routes:
            return jsonify({"route": general_user_routes[module], "role": role})
        elif role == "service_provider" and module in service_provider_routes:
            return jsonify({"route": service_provider_routes[module], "role": role})
        else:
            return jsonify({
                "route": None,
                "message": "I couldn’t identify your module. Please mention if you are a general user or service provider."
            })

    except Exception as e:
        print("Error parsing AI response:", e)
        return jsonify({"route": None, "message": "Sorry, something went wrong understanding your intent."})


if __name__ == "__main__":
    app.run(debug=True)




