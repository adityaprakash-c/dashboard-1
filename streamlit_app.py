import streamlit as st
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Railway Ticket Booking",
    layout="wide",
    page_icon="🚆",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
    }
    .main {
        background: linear-gradient(to right, #c6ffdd, #fbd786, #f7797d);
        padding: 2rem;
        border-radius: 10px;
    }
    .title {
        font-size: 3rem;
        font-weight: bold;
        color: #003366;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.5rem;
        color: #444444;
        margin-bottom: 2rem;
        text-align: center;
    }
    .passenger-box {
        background-color: #ffffffaa;
        padding: 15px 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 0 10px #aaa;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .train-card {
        background-color: #ffffffaa;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 0 10px #aaa;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .cancel-btn {
        background-color: #f44336 !important;
    }
    .cancel-btn:hover {
        background-color: #d32f2f !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main"><div class="title">🚆 Railway Ticket Booking System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Book your train tickets with ease</div>', unsafe_allow_html=True)

# Session state initialization
if 'passengers' not in st.session_state:
    st.session_state.passengers = []
if 'bookings' not in st.session_state:
    st.session_state.bookings = {}
if 'pnr_counter' not in st.session_state:
    st.session_state.pnr_counter = 1000

# Train Data with more details
trains = [
    {
        "train_no": 10101,
        "name": "Pune Express",
        "seats": 100,
        "source": "Mumbai",
        "destination": "Pune",
        "departure": "07:00",
        "arrival": "10:30",
        "days": "Daily",
        "type": "Express"
    },
    {
        "train_no": 10202,
        "name": "Delhi Shatabdi",
        "seats": 120,
        "source": "Delhi",
        "destination": "Jaipur",
        "departure": "06:00",
        "arrival": "10:15",
        "days": "Daily",
        "type": "Shatabdi"
    },
    {
        "train_no": 10303,
        "name": "Mumbai Rajdhani",
        "seats": 80,
        "source": "Mumbai",
        "destination": "Delhi",
        "departure": "16:00",
        "arrival": "08:30 (next day)",
        "days": "Daily",
        "type": "Rajdhani"
    },
    {
        "train_no": 10404,
        "name": "Chennai Mail",
        "seats": 150,
        "source": "Bangalore",
        "destination": "Chennai",
        "departure": "14:30",
        "arrival": "20:45",
        "days": "Daily",
        "type": "Mail"
    }
]

# Helper functions
def generate_pnr():
    st.session_state.pnr_counter += 1
    return st.session_state.pnr_counter

def get_train_by_number(train_no):
    for train in trains:
        if train["train_no"] == train_no:
            return train
    return None

def get_available_seats(train_no):
    booked = sum(1 for booking in st.session_state.bookings.values() 
                if booking['train_no'] == train_no and not booking['cancelled'])
    train = get_train_by_number(train_no)
    return train['seats'] - booked if train else 0

# Sidebar navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Select an option", 
                         ["Home", "Search Trains", "Book Ticket", "My Bookings", "Cancel Ticket", "About"])

# Home Page
if choice == "Home":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Welcome to Railway Ticket Booking")
        st.write("""
        Book your train tickets easily with our online booking system. 
        Find trains, check availability, and book tickets in just a few clicks.
        """)
        
        st.subheader("Why Choose Us?")
        st.markdown("""
        - 🚅 Fast and easy booking process
        - 🔍 Real-time train availability
        - 📱 Mobile-friendly interface
        - 💰 No hidden charges
        - 🎫 Instant PNR generation
        """)
        
    with col2:
        st.image("https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6a3?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60", 
                caption="Book your journey with us", use_column_width=True)
        
    st.subheader("Popular Trains")
    cols = st.columns(2)
    for i, train in enumerate(trains[:4]):
        with cols[i%2]:
            with st.container():
                st.markdown(f"""
                <div class="train-card">
                    <h3>{train['name']} ({train['train_no']})</h3>
                    <p><strong>Route:</strong> {train['source']} → {train['destination']}</p>
                    <p><strong>Timing:</strong> {train['departure']} - {train['arrival']}</p>
                    <p><strong>Type:</strong> {train['type']} | <strong>Runs:</strong> {train['days']}</p>
                    <p><strong>Seats Available:</strong> {get_available_seats(train['train_no'])}</p>
                </div>
                """, unsafe_allow_html=True)

# Search Trains
elif choice == "Search Trains":
    st.subheader("🔍 Search Trains")
    
    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("From", sorted(list(set(train['source'] for train in trains))))
    with col2:
        destination = st.selectbox("To", sorted(list(set(train['destination'] for train in trains))))
    
    date = st.date_input("Journey Date", min_value=datetime.today(), 
                         max_value=datetime.today() + timedelta(days=60))
    
    if st.button("Search Trains"):
        available_trains = [train for train in trains 
                          if train['source'] == source and train['destination'] == destination]
        
        if available_trains:
            st.success(f"Found {len(available_trains)} trains available")
            for train in available_trains:
                available_seats = get_available_seats(train['train_no'])
                
                with st.container():
                    st.markdown(f"""
                    <div class="train-card">
                        <div style="display: flex; justify-content: space-between;">
                            <h3>{train['name']} ({train['train_no']})</h3>
                            <span style="color: {'green' if available_seats > 10 else 'red'}; 
                                          font-weight: bold;">
                                {available_seats} seats available
                            </span>
                        </div>
                        <p><strong>Departure:</strong> {train['departure']} from {train['source']}</p>
                        <p><strong>Arrival:</strong> {train['arrival']} at {train['destination']}</p>
                        <p><strong>Duration:</strong> {train['type']} | Runs: {train['days']}</p>
                        <button onclick="window.location.href='#book-ticket-{train['train_no']}'" 
                                style="background-color: #4CAF50; color: white; padding: 8px 16px; 
                                       border: none; border-radius: 4px; cursor: pointer;">
                            Book Now
                        </button>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("No trains found for this route")

# Book Ticket
elif choice == "Book Ticket":
    st.subheader("🎟️ Book Ticket")
    
    train_no = st.selectbox("Select Train", 
                           [f"{train['train_no']} - {train['name']} ({train['source']} to {train['destination']})" 
                            for train in trains],
                           index=0)
    train_no = int(train_no.split(" - ")[0])
    train = get_train_by_number(train_no)
    
    if train:
        available_seats = get_available_seats(train_no)
        st.markdown(f"""
        <div class="info-box">
            <strong>{train['name']}</strong> ({train['type']})<br>
            <strong>Route:</strong> {train['source']} → {train['destination']}<br>
            <strong>Departure:</strong> {train['departure']} | <strong>Arrival:</strong> {train['arrival']}<br>
            <strong>Available Seats:</strong> {available_seats}
        </div>
        """, unsafe_allow_html=True)
        
        if available_seats <= 0:
            st.error("No seats available on this train. Please try another train.")
        else:
            with st.form("booking_form"):
                st.subheader("Passenger Details")
                name = st.text_input("Full Name*")
                age = st.number_input("Age*", min_value=1, max_value=100, value=25)
                gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
                berth = st.selectbox("Preferred Berth", ["No Preference", "Lower", "Middle", "Upper", "Side Lower", "Side Upper"])
                email = st.text_input("Email Address*")
                phone = st.text_input("Mobile Number*")
                
                st.subheader("Journey Details")
                journey_date = st.date_input("Date of Journey*", min_value=datetime.today())
                
                submitted = st.form_submit_button("Confirm Booking")
                
                if submitted:
                    if not all([name, email, phone]):
                        st.error("Please fill all required fields (*)")
                    else:
                        pnr = generate_pnr()
                        booking_details = {
                            "pnr": pnr,
                            "train_no": train_no,
                            "train_name": train['name'],
                            "passenger_name": name,
                            "age": age,
                            "gender": gender,
                            "berth": berth,
                            "email": email,
                            "phone": phone,
                            "journey_date": str(journey_date),
                            "booking_date": str(datetime.now().date()),
                            "status": "Confirmed",
                            "cancelled": False
                        }
                        
                        st.session_state.bookings[pnr] = booking_details
                        
                        st.markdown(f"""
                        <div class="success-box">
                            <h3>Booking Successful!</h3>
                            <p><strong>PNR Number:</strong> {pnr}</p>
                            <p><strong>Train:</strong> {train['name']} ({train['train_no']})</p>
                            <p><strong>Passenger:</strong> {name}</p>
                            <p><strong>Journey Date:</strong> {journey_date}</p>
                            <p>Your ticket has been booked successfully. Please note your PNR number for future reference.</p>
                        </div>
                        """, unsafe_allow_html=True)

# My Bookings
elif choice == "My Bookings":
    st.subheader("📋 My Bookings")
    
    search_option = st.radio("Search by", ["PNR Number", "Passenger Name"])
    
    if search_option == "PNR Number":
        pnr = st.number_input("Enter PNR Number", min_value=1001, step=1)
        if st.button("Search Booking"):
            if pnr in st.session_state.bookings:
                booking = st.session_state.bookings[pnr]
                status = "Cancelled" if booking['cancelled'] else "Confirmed"
                status_color = "red" if booking['cancelled'] else "green"
                
                st.markdown(f"""
                <div class="train-card">
                    <div style="display: flex; justify-content: space-between;">
                        <h3>PNR: {pnr}</h3>
                        <span style="color: {status_color}; font-weight: bold;">{status}</span>
                    </div>
                    <p><strong>Train:</strong> {booking['train_name']} ({booking['train_no']})</p>
                    <p><strong>Passenger:</strong> {booking['passenger_name']} ({booking['age']} years, {booking['gender']})</p>
                    <p><strong>Journey Date:</strong> {booking['journey_date']}</p>
                    <p><strong>Booking Date:</strong> {booking['booking_date']}</p>
                    <p><strong>Contact:</strong> {booking['email']} | {booking['phone']}</p>
                    <p><strong>Berth Preference:</strong> {booking['berth']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("No booking found with this PNR number")
    else:
        name = st.text_input("Enter Passenger Name")
        if st.button("Search Bookings"):
            found_bookings = [booking for booking in st.session_state.bookings.values() 
                            if name.lower() in booking['passenger_name'].lower()]
            
            if found_bookings:
                st.success(f"Found {len(found_bookings)} booking(s)")
                for booking in found_bookings:
                    status = "Cancelled" if booking['cancelled'] else "Confirmed"
                    status_color = "red" if booking['cancelled'] else "green"
                    
                    st.markdown(f"""
                    <div class="train-card">
                        <div style="display: flex; justify-content: space-between;">
                            <h3>PNR: {booking['pnr']}</h3>
                            <span style="color: {status_color}; font-weight: bold;">{status}</span>
                        </div>
                        <p><strong>Train:</strong> {booking['train_name']} ({booking['train_no']})</p>
                        <p><strong>Passenger:</strong> {booking['passenger_name']}</p>
                        <p><strong>Journey Date:</strong> {booking['journey_date']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("No bookings found for this passenger")

# Cancel Ticket
elif choice == "Cancel Ticket":
    st.subheader("❌ Cancel Ticket")
    
    pnr = st.number_input("Enter PNR Number to Cancel", min_value=1001, step=1)
    
    if st.button("Check Booking"):
        if pnr in st.session_state.bookings:
            booking = st.session_state.bookings[pnr]
            
            if booking['cancelled']:
                st.error("This ticket is already cancelled")
            else:
                st.markdown(f"""
                <div class="train-card">
                    <h3>Booking Details (PNR: {pnr})</h3>
                    <p><strong>Train:</strong> {booking['train_name']} ({booking['train_no']})</p>
                    <p><strong>Passenger:</strong> {booking['passenger_name']}</p>
                    <p><strong>Journey Date:</strong> {booking['journey_date']}</p>
                    <p><strong>Status:</strong> <span style="color: green; font-weight: bold;">Confirmed</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Confirm Cancellation", key="cancel_btn"):
                    st.session_state.bookings[pnr]['cancelled'] = True
                    st.session_state.bookings[pnr]['status'] = "Cancelled"
                    
                    st.markdown(f"""
                    <div class="info-box">
                        <h3>Cancellation Successful</h3>
                        <p>Ticket with PNR {pnr} has been cancelled.</p>
                        <p>A refund (if applicable) will be processed within 7 working days.</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("No booking found with this PNR number")

# About
elif choice == "About":
    st.subheader("📘 About This Project")
    
    st.markdown("""
    <div class="train-card">
        <h3>Railway Ticket Booking System</h3>
        <p>This is a comprehensive railway ticket booking simulation application built using Python and Streamlit.</p>
        
        <h4>Features:</h4>
        <ul>
            <li>🚆 Search trains by route and date</li>
            <li>🎟️ Book tickets with passenger details</li>
            <li>📋 View booking history by PNR or passenger name</li>
            <li>❌ Cancel tickets with refund information</li>
            <li>📱 Responsive design for all devices</li>
            <li>🔒 Secure booking process</li>
        </ul>
        
        <h4>Technology Stack:</h4>
        <ul>
            <li>Python 3</li>
            <li>Streamlit (Web Framework)</li>
            <li>HTML/CSS (UI Styling)</li>
        </ul>
        
        <h4>Developed By:</h4>
        <ul>
            <li>Aditya Prakash</li>
            <li>Vaibhav Shinde</li>
            <li>Swastik Singh</li>
        </ul>
        
        <p>This project is for educational purposes and demonstrates a complete ticket booking workflow.</p>
    </div>
    """, unsafe_allow_html=True)
