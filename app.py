import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

from ui_styles import apply_styles
from auth import login

load_dotenv()

st.set_page_config(
    page_title="Urban Travel Assistant",
    layout="wide"
)

apply_styles()

# SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "step" not in st.session_state:
    st.session_state.step = "start"


# LOGIN
if not st.session_state.logged_in:
    login()
    st.stop()


# SIDEBAR
with st.sidebar:

    st.title("Urban Travel Assistant")

    st.write("Navigation")

    if st.button("Start Over"):
        st.session_state.step = "start"
        st.rerun()

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()


# MAIN FLOW
import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

from ui_styles import apply_styles
from auth import login

load_dotenv()

st.set_page_config(
    page_title="Urban Travel Assistant",
    layout="wide"
)

apply_styles()

# SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "step" not in st.session_state:
    st.session_state.step = "start"


# LOGIN
if not st.session_state.logged_in:
    login()
    st.stop()


# SIDEBAR
with st.sidebar:

    st.title("Urban Travel Assistant")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()


# MAIN FLOW
if st.session_state.step == "start":

    st.subheader("Welcome to Urban Travel Assistant")

    choice = st.radio(
        "What would you like to do?",
        [
            "I already know my destination",
            "Get AI travel suggestions"
        ]
    )

# ---------- LOGIN SYSTEM ----------
API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:

    st.error("❌ GEMINI_API_KEY not found in .env")

    st.stop()


# ✅ NEW CLIENT (THIS IS THE FIX)

client = genai.Client(api_key=API_KEY)

def ai_list(prompt):

    response = ai_response(prompt)

    lines = [l.strip("-• ") for l in response.split("\n") if l.strip()]

    for item in lines:

        st.write("•", item)

@st.cache_data(show_spinner=False)

def cached_ai_response(prompt):

    return ai_response(prompt)


def ai_response(prompt: str) -> str:

    try:

        response = client.models.generate_content(

            model="models/gemini-flash-lite-latest",

            contents=prompt

        )

        return response.text

    except Exception as e:

        return "⚠️ AI service is temporarily unavailable. Please try again in a minute."

def smart_ai_section(prompt, fallback_type, destination):

    """

    fallback_type: attractions | food | clothing | tips | safety | culture

    """

    response = cached_ai_response(prompt)


    # ✅ AI worked

    if "⚠️" not in response:

        st.write(response)

        return


    # ⚠️ AI failed → show intelligent fallback

    st.info("AI is busy. Showing helpful suggestions instead 👇")


    fallback_data = {

        "attractions": f"""

        • Popular landmarks and historical sites in {destination}  

        • Museums or ancient monuments nearby  

        • Scenic viewpoints or riverfront areas  

        • Local temples or heritage places

        """,


        "food": f"""

        • Famous regional dishes of {destination}  

        • Popular street food  

        • Traditional sweets or snacks  

        • Locally famous vegetarian/non-vegetarian meals

        """,


        "clothing": f"""

        • Comfortable cotton clothes for daytime  

        • Light jacket for evenings  

        • Comfortable walking shoes  

        • Modest clothing for religious places

        """,


        "tips": f"""

        • Start sightseeing early  

        • Keep local transport options handy  

        • Stay hydrated  

        • Carry some cash for small shops

        """,


        "safety": f"""

        • Avoid isolated areas late at night  

        • Keep copies of ID  

        • Follow local rules  

        • Keep emergency contacts saved

        """,


        "culture": f"""

        • Dress modestly at temples  

        • Respect local customs  

        • Ask before taking photos  

        • Be polite with locals

        """

    }


    st.write(fallback_data.get(fallback_type, ""))


def nearby_experience_places(destination, experience):

    prompt = f"""

    The user is traveling to {destination} and wants a {experience} experience.


    Suggest 4–6 nearby or easily reachable places (within a few hours)

    that match this experience.


    Return ONLY a bullet list of place names with a short note in brackets.

    """

    return ai_response(prompt)

st.markdown('<p class="main-title">🧭 Urban Travel Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Plan your perfect trip with AI ✈️</p>', unsafe_allow_html=True)

# ---------- SESSION STATE ----------

# --- SESSION STATE INITIALIZATION ---

def get_ai_info(prompt):

    try:

        response = client.models.generate_content(

            model="models/gemini-flash-lite-latest",

            contents=prompt

        )

        return response.text

    except Exception as e:

        return "⚠️ AI service is temporarily unavailable. Please try again in a minute."

if "step" not in st.session_state:

    st.session_state.step = "start"


if "data" not in st.session_state:

    st.session_state.data = {}


# 🔑 PLACE YOUR NEW INITIALIZATIONS HERE:

if "tips_output" not in st.session_state:

    st.session_state.tips_output = None

if "culture_output" not in st.session_state:

    st.session_state.culture_output = None

if "safety_output" not in st.session_state:

    st.session_state.safety_output = None


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

# ---------- STEP 1: START ----------

if st.session_state.step == "start":

    st.subheader("👋 Welcome to Urban Travel Assistant!")

    st.markdown('<div class="box">', unsafe_allow_html=True)

choice = st.radio(
    "🌍 What would you like to do?",
    [
        "📍 I already know my destination",
        "✨ Get AI travel suggestions"
    ]
)



# =====================================================================
# 🔹 FLOW 1: USER WITH SPECIFIC PLACE
# =====================================================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


if st.session_state.step == "destination":

    st.subheader("📍 Enter Destination")

    dest = st.text_input("City / State / Country")


    if st.button("Next") and dest:

        st.session_state.data["destination"] = dest

        st.session_state.step = "experience"




if st.session_state.step == "experience":

    st.subheader("🎯 What kind of experience?")


    exp = st.selectbox(

        "Select experience type:",

        ["Adventure", "Devotional", "Nature", "Historical", "Leisure", "Beach"],

        key="experience_select"

    )


    if st.button("Next", key="next_experience"):

        st.session_state.data["experience"] = exp

        st.session_state.step = "travel_style"

        st.rerun()


if st.session_state.step == "travel_style":

    st.subheader("👥 Who are you traveling with?")


    style = st.selectbox(

        "Select travel style:",

        ["Solo", "Friends", "Family", "Couple"],

        key="travel_style_select"

    )


    if st.button("Next", key="next_travel_style"):

        st.session_state.data["travel_style"] = style

        st.session_state.step = "summary"

        st.rerun()

if st.session_state.step == "summary":

    st.subheader("🔎 Confirm Your Travel Preferences")

   

    with st.container(border=True):

        # Pull data safely using .get() to avoid errors

        dest = st.session_state.data.get('destination', 'AI Choice')

        exp = st.session_state.data.get('experience', 'Not Selected')

        style = st.session_state.data.get('travel_style', 'Not Selected')

       

        st.markdown(f"📍 **Destination:** {dest}")

        st.markdown(f"✨ **Experience:** {exp}")

        st.markdown(f"👥 **Travel Style:** {style}")

        if "duration" in st.session_state.data:

            st.markdown(f"📅 **Stay:** {st.session_state.data['duration']} Days")


    change = st.selectbox(

        "Is everything correct?",

        ["Yes, everything is perfect", "Change destination", "Change experience", "Change travel style"]

    )


    if st.button("Continue to Trip Planning"):

        if change == "Yes, everything is perfect":

            st.session_state.step = "overview"

        else:

            mapping = {"Change destination": "destination", "Change experience": "experience", "Change travel style": "travel_style"}

            st.session_state.step = mapping[change]

        st.rerun()


if st.session_state.step == "overview":

    # 🔑 ADD THESE TWO LINES TO PREVENT NAMEERROR

    destination = st.session_state.data.get("destination")

    experience = st.session_state.data.get("experience")


    st.subheader(f"🌟 {destination} – {experience} Experience")

    # ... rest of your code


    prompt = f"Give a short travel overview of {destination}."

    st.write(cached_ai_response(prompt))


    st.markdown(f"### 🧭 Nearby places for {experience} experience")


    # Now these variables exist and won't cause a NameError

    nearby_places = nearby_experience_places(destination, experience)

    st.write(nearby_places)


    if st.button("Continue", key="overview_continue"):

        st.session_state.step = "attractions"

        st.rerun()

# ---------- OPTIONAL SECTIONS ----------

def yes_no_step(title, yes_text, next_step):

    st.subheader(title)


    choice = st.radio(

        "Choose an option:",

        ["Yes", "No"],

        key=f"radio_{title}"   # 🔑 UNIQUE KEY

    )


    if st.button("Next", key=f"next_{title}"):

        if choice == "Yes":

            st.info(yes_text)

        st.session_state.step = next_step

        st.rerun()

if st.session_state.step == "attractions":

    destination = st.session_state.data["destination"]

    st.subheader(f"🌲 Top Attractions in {destination}")


    # 1. Initialize storage for attractions if not already there

    if "attractions_output" not in st.session_state:

        st.session_state.attractions_output = None


    choice = st.radio(

        "Would you like to explore famous tourist attractions here?",

        ["Yes", "No"],

        key="attractions_choice"

    )


    if st.button("Show Attractions", key="btn_show_attractions"):

        if choice == "Yes":

            prompt = f"""

List 5–6 MUST-VISIT tourist attractions in {destination}.

These places should be:

- Most visited by tourists

- Iconic and popular

- Cannot be missed when visiting {destination}


Return ONLY bullet points with short descriptions.

"""

            # Save the AI response to session state

            st.session_state.attractions_output = cached_ai_response(prompt)

        else:

            st.session_state.attractions_output = "Skipping attractions section."


    # 2. ALWAYS display the output if it exists in the memory

    if st.session_state.attractions_output:

        st.markdown(st.session_state.attractions_output)

       

        # 3. Only show the 'Continue' button AFTER the info is displayed

        if st.button("Continue to Food 🍽️", key="btn_goto_food"):

            st.session_state.attractions_output = None # Clear memory for next time

            st.session_state.step = "food"

            st.rerun()


if st.session_state.step == "food":

    st.subheader("🍽 Local Food")

   

    # Check if we already have the result in memory

    if "food_result" not in st.session_state:

        st.session_state.food_result = None


    choice = st.radio("Would you like local food suggestions?", ["Yes", "No"], key="food_radio")


    if st.button("Show Food Suggestions"):

        if choice == "Yes":

            prompt = f"List popular local foods in {st.session_state.data['destination']}."

            st.session_state.food_result = cached_ai_response(prompt)

        else:

            st.session_state.food_result = "Skipped food suggestions."


    # Always show the result if it exists in memory

    if st.session_state.food_result:

        st.write(st.session_state.food_result)

        if st.button("Continue to Clothing"):

            st.session_state.step = "clothing"

            st.rerun()


    # ✅ SHOW FOOD OUTPUT

if st.session_state.step == "clothing":

    # 🔑 Pull variable from state to prevent NameError

    destination = st.session_state.data.get("destination")


    st.subheader("👕 Clothing Suggestions")


    # Initialize storage in session state

    if "clothing_output" not in st.session_state:

        st.session_state.clothing_output = None


    choice = st.radio(

        "Would you like clothing suggestions based on the climate?",

        ["Yes", "No"],

        key="clothing_radio"

    )


    # Use a specific button to trigger the AI

    if st.button("Show Clothing Suggestions", key="btn_show_clothing"):

        if choice == "Yes":

            prompt = f"Suggest appropriate clothing for traveling to {destination} based on climate. Return ONLY bullet points."

            # Save response to memory

            st.session_state.clothing_output = cached_ai_response(prompt)

        else:

            st.session_state.clothing_output = "You chose to skip clothing suggestions."


    # ALWAYS display the stored response if it exists

    if st.session_state.clothing_output:

        st.info(f"👗 Recommended for {destination}:")

        st.write(st.session_state.clothing_output)

       

        # Only show the 'Continue' button AFTER suggestions appear

        if st.button("Continue to Travel Tips ✈️", key="btn_go_to_tips"):

            st.session_state.clothing_output = None # Clear for next run

            st.session_state.step = "tips"

            st.rerun()






if st.session_state.step == "tips":

    destination = st.session_state.data["destination"]


    st.subheader("✈️ Travel Tips")


    choice = st.radio(

        "Would you like travel tips for this destination?",

        ["Yes", "No"],

        key="tips_radio"

    )


    if st.button("Show Travel Tips"):

        if choice == "Yes":

            prompt = f"""

            Give 4–5 practical travel tips for visiting {destination}.

            Return ONLY bullet points.

            """

            st.session_state.tips_output = cached_ai_response(prompt)

        else:

            st.session_state.tips_output = "You chose to skip travel tips."


    if st.session_state.tips_output:

        st.markdown("### ✈️ Helpful Travel Tips")


        if "⚠️" in st.session_state.tips_output:

            smart_ai_section("", "tips", destination)

        else:

            st.write(st.session_state.tips_output)


        if st.button("Continue to Safety"):

            st.session_state.tips_output = None

            st.session_state.step = "safety"

            st.rerun()


if st.session_state.step == "safety":

    destination = st.session_state.data.get("destination") # Pull from state

    st.subheader("🛡️ Safety Tips")


    if "safety_output" not in st.session_state:

        st.session_state.safety_output = None


    choice = st.radio("Would you like safety tips?", ["Yes", "No"], key="safety_radio")


    if st.button("Show Safety Tips"):

        if choice == "Yes":

            prompt = f"List important safety tips for travelers visiting {destination}. Return ONLY bullet points."

            st.session_state.safety_output = cached_ai_response(prompt)

        else:

            st.session_state.safety_output = "Skipped safety tips."


    # Always display the result if it exists in memory

    if st.session_state.safety_output:

        st.write(st.session_state.safety_output)

        if st.button("Next to Cultural Etiquette"):

            st.session_state.step = "culture"

            st.rerun()


# Pull data from memory at the start of the block to prevent NameError

destination = st.session_state.data.get("destination")

experience = st.session_state.data.get("experience")

if st.session_state.step == "culture":

    # Pull data safely to prevent NameError

    destination = st.session_state.data.get("destination")

    st.subheader("🙏 Cultural Etiquette")


    # Initialize a specific key to store the culture output in memory

    if "culture_output" not in st.session_state:

        st.session_state.culture_output = None


    choice = st.radio(

        "Would you like to know cultural etiquette and local customs?",

        ["Yes", "No"],

        key="culture_radio"

    )


    # 1. Action Button: Show the info

    if st.button("Show Etiquette Tips", key="btn_show_culture"):

        if choice == "Yes":

            prompt = f"""

            Explain important cultural etiquette and local customs

            travelers should follow in {destination}.

            Return ONLY bullet points.

            """

            # Store the response so it persists through reruns

            st.session_state.culture_output = cached_ai_response(prompt)

        else:

            st.session_state.culture_output = "You chose to skip cultural etiquette."


    # 2. Display: Always show the info if it exists in session_state

    if st.session_state.culture_output:

        st.write(st.session_state.culture_output)

       

        # 3. Navigation: Only show 'Continue' AFTER the user has seen the info

        if st.button("Continue to Checklist 🧳", key="btn_culture_done"):

            st.session_state.culture_output = None # Clear memory for fresh start next time

            st.session_state.step = "checklist"

            st.rerun()




if st.session_state.step == "checklist":

    st.header("🧳 Your Ultimate Travel Essentials")

    st.write("Check off items as you pack. Your progress is saved automatically!")


    # Define Categories and Items

    categories = {

        "👕 Wardrobe & Linens": [

            "Apparel & Dresses", "Innerwear", "Soft Towels",

            "Traditional Chunnis", "Travel Blankets", "Napkins/Handkerchiefs"

        ],

        "🧼 Personal Care & Toiletries": [

            "Dental Kit (Paste/Brush/Tongue Cleaner)", "Hand Sanitizer & Hand Wash",

            "Body Soap", "Pooja Essentials (Turmeric/Kumkum/Kumkum Paste)",

            "Soft Tissue Papers", "Moisturizer/Face Cream", "Face Powder & Puff"

        ],

        "✨ Grooming & Accessories": [

            "Bangles & Earrings", "Hair Clips & Safety Pins",

            "Bindi/Stickers", "Combs & Hairbrushes"

        ],

        "💊 Health & Wellness": [

            "Prescribed Tablets", "Zandu Balm/Pain Relief",

            "First Aid Cotton", "Sanitary Essentials"

        ],

        "🔌 Electronics & Gadgets": [

            "Smartphones", "High-Speed Phone Chargers",

            "Travel Hair Dryer", "Electric Kettle",

            "Power Bank (Added Essential 🔋)", "Universal Adapter (Added Essential 🔌)"

        ],

        "🍎 Pantry & Food Supplies": [

            "Biscuits & Travel Snacks", "Daniyalu (Coriander Seeds)",

            "Eco-friendly Paper Plates", "Disposable Spoons"

        ],

        "📄 Critical Documents": [

            "Original Aadhaar Cards", "Xerox Copies of ID Proofs",

            "Confirmed Travel Tickets", "Hotel Booking Vouchers (Added Essential 🏨)"

        ],

        "🎒 Misc. Comfort Items": [

            "Ergonomic Car Pillows", "Empty Storage Boxes & Covers",

            "Travel Handbags", "Small Coconut Oil", "Refreshing Body Spray",

            "Reusable Drinking Glass"

        ]

    }


    # Interactive UI

    for category, items in categories.items():

        with st.expander(category, expanded=True):

            for item in items:

                st.checkbox(item, key=f"check_{item}")


    # Add Custom Item Logic

    st.divider()

    st.subheader("➕ Add Personal Items")

    new_item = st.text_input("Need to pack something else?", placeholder="e.g., Camera, Sunglasses...")

   

    if st.button("Add to My List") and new_item:

        # Assuming you have a list in session_state for custom items

        if "custom_list" not in st.session_state:

            st.session_state.custom_list = []

        st.session_state.custom_list.append(new_item)

        st.rerun()


    # Display Custom Items

    if "custom_list" in st.session_state:

        for c_item in st.session_state.custom_list:

            st.checkbox(c_item, key=f"custom_{c_item}", value=True)


    if st.button("Finalize & Continue", type="primary"):

        st.session_state.step = "open_chat"

        st.rerun()
if st.session_state.step == "open_chat":
    st.subheader("💬 Chat with AI")
    
    # 1. Render history correctly from tuples
    for role, msg in st.session_state.chat_history:
        with st.chat_message("user" if role == "You" else "assistant"):
            st.write(msg)

    # 2. Chat Input
    if q := st.chat_input("Ask me anything about your trip...", key="chat_input_unique"):
        dest = st.session_state.data.get("destination")
        ans = get_ai_info(f"As a travel bot for {dest}, answer: {q}")
        st.session_state.chat_history.append(("You", q))
        st.session_state.chat_history.append(("Bot", ans))
        st.rerun()

    st.write("---")

# --- FIXED EXIT LOGIC ---

# =====================================================================
# 🔹 FLOW 2: USER WITHOUT SPECIFIC PLACE
# =====================================================================
if st.session_state.step == "scope":
    st.subheader("🌍 Travel Scope")
    scope = st.selectbox("Where would you like to travel?", ["National", "International", "Anywhere"], key="scope_sel")
    
    # 🔑 FIX: Added unique key 'btn_scope_next'
    if st.button("Next", key="btn_scope_next"):
        st.session_state.data["scope"] = scope
        st.session_state.step = "exp2"
        st.rerun() # 🔑 FIX: Clears the screen to move to next step

if st.session_state.step == "exp2":
    st.subheader("🎯 Type of Experience")
    exp = st.selectbox("What kind of experience?", ["Adventure", "Devotional", "Nature", "Historical", "Leisure", "Beach"], key="exp2_sel")
    
    # 🔑 FIX: Added unique key 'btn_exp_next'
    if st.button("Next", key="btn_exp_next"):
        st.session_state.data["experience"] = exp
        st.session_state.step = "style2"
        st.rerun()
        
if st.session_state.step == "style2":
    st.subheader("👥 Travel Style")
    # 🔑 FIX: Ensure this value is saved to session_state.data
    style = st.selectbox("Who are you traveling with?", ["Solo", "Friends", "Family", "Couple", "Day Trip"], key="style2_sel")
    
    if st.button("Next", key="btn_style2_next"):
        # 🔑 SAVE THE DATA HERE to prevent KeyError
        st.session_state.data["travel_style"] = style 
        st.session_state.step = "budget_duration"
        st.rerun()

       

# Ensure this block is visible and reachable

if st.session_state.step == "budget_duration":

    st.subheader("⏰ Duration & 💰 Budget")

   

    col1, col2 = st.columns(2)

    with col1:

        days = st.number_input("How many days?", min_value=1, max_value=30, value=4)

    with col2:

        budget = st.selectbox("Budget Range", ["Economy", "Mid-range", "Luxury", "Skip"])


    if st.button("Generate Recommendations"):

        st.session_state.data["duration"] = days

        st.session_state.data["budget"] = budget

        st.session_state.step = "suggest"

        st.rerun()

if st.session_state.step == "suggest":
    st.subheader("✨ Suggested Destinations")

    # Safe data retrieval using .get() to prevent crashes
    scope = st.session_state.data.get("scope", "National")
    experience = st.session_state.data.get("experience", "Adventure")
    style = st.session_state.data.get("travel_style", "Solo")

    prompt = f"Suggest all {scope} destinations for a {experience} and a {style} trip with details (Best time, Duration). Return as a list."
    response = ai_response(prompt) 

    # 🔑 FIX: Prevent selectbox crash if AI returns an error
    if "⚠️" in response:
        st.error("AI is temporarily busy. Please type a destination below manually.")
        places = []
    else:
        places = [p.strip("-• ") for p in response.split("\n") if p.strip()]

    selected_place = st.selectbox("Choose a destination", places if places else ["Type manually..."], key="suggest_place_f2")
    manual_place = st.text_input("Or enter destination manually:", key="manual_dest_f2")

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Explore", key="btn_explore_f2"):
            st.session_state.data["destination"] = manual_place if manual_place else selected_place
            st.session_state.step = "overview"
            st.rerun()
    with col2:
        if st.button("Exit App", key="btn_exit_suggest_f2"):
            st.session_state.clear()
            st.rerun()
if st.session_state.step == "open_chat":
    st.subheader("💬 Chat with AI")
    dest = st.session_state.data.get("destination", "your destination")
    
    # 1. Existing loop to show chat history
    for role, msg in st.session_state.chat_history:
        with st.chat_message("user" if role == "You" else "assistant"):
            st.write(msg)

    # 2. Existing chat input logic
    if q := st.chat_input("Ask me anything about your trip...", key="chat_input_final"):
        ans = get_ai_info(f"As a travel bot for {dest}, answer: {q}")
        st.session_state.chat_history.append(("You", q))
        st.session_state.chat_history.append(("Bot", ans))
        st.rerun() # 🔑 Refreshes screen to show new messages

    # --- 🚩 ADD THE NEW CODE BELOW THIS LINE ---
    st.write("---") # Visual separator

    col1, col2 = st.columns([2, 1])
    with col1:
        # This button moves the user to the 'final_page' step
        if st.button("Finish Conversation & Move to Next Step ➡️", key="btn_goto_final"):
            st.session_state.step = "final_page"
            st.rerun() # 🔑 Forces the app to switch screens
    with col2:
        # Unique key prevents DuplicateElementId error
        if st.button("Exit App", key="btn_exit_from_chat"):
            st.session_state.clear() # Clears session memory
            st.rerun()
# --- STEP 19: FINAL NAVIGATION (Dropdown logic from your request) ---
if st.session_state.step == "final_page":
    st.subheader("🧭 Urban Travel Assistant")
    st.write("### What would you like to do next?")
    
    action = st.selectbox(
        "Choose an option:", 
        ["Select...", "Explore another suggested place", "Start a new trip", "Exit App"], 
        key="final_nav_dropdown_shared"
    )
    
    if st.button("Confirm Action", key="btn_confirm_final_shared"):
        if action == "Start a new trip":
            st.session_state.clear() # Resets the entire app
            st.rerun()
        elif action == "Explore another suggested place":
            st.session_state.step = "suggest" # Jumps back to Flow 2 suggestions
            st.rerun()
        elif action == "Exit App":
            st.balloons()
            st.success("Thank you for using Urban Travel Assistant! Safe travels! 🧭")
            st.stop() # Terminates the app session

# ---------- LOGIN SYSTEM ----------
API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:

    st.error("❌ GEMINI_API_KEY not found in .env")

    st.stop()


# ✅ NEW CLIENT (THIS IS THE FIX)

client = genai.Client(api_key=API_KEY)

@st.cache_data(show_spinner=False)

def cached_ai_response(prompt):

    return ai_response(prompt)


def ai_response(prompt: str) -> str:

    try:

        response = client.models.generate_content(

            model="models/gemini-flash-lite-latest",

            contents=prompt

        )

        return response.text

    except Exception as e:

        return "⚠️ AI service is temporarily unavailable. Please try again in a minute."

def smart_ai_section(prompt, fallback_type, destination):

    """

    fallback_type: attractions | food | clothing | tips | safety | culture

    """

    response = cached_ai_response(prompt)


    # ✅ AI worked

    if "⚠️" not in response:

        st.write(response)

        return


    # ⚠️ AI failed → show intelligent fallback

    st.info("AI is busy. Showing helpful suggestions instead 👇")


    fallback_data = {

        "attractions": f"""

        • Popular landmarks and historical sites in {destination}  

        • Museums or ancient monuments nearby  

        • Scenic viewpoints or riverfront areas  

        • Local temples or heritage places

        """,


        "food": f"""

        • Famous regional dishes of {destination}  

        • Popular street food  

        • Traditional sweets or snacks  

        • Locally famous vegetarian/non-vegetarian meals

        """,


        "clothing": f"""

        • Comfortable cotton clothes for daytime  

        • Light jacket for evenings  

        • Comfortable walking shoes  

        • Modest clothing for religious places

        """,


        "tips": f"""

        • Start sightseeing early  

        • Keep local transport options handy  

        • Stay hydrated  

        • Carry some cash for small shops

        """,


        "safety": f"""

        • Avoid isolated areas late at night  

        • Keep copies of ID  

        • Follow local rules  

        • Keep emergency contacts saved

        """,


        "culture": f"""

        • Dress modestly at temples  

        • Respect local customs  

        • Ask before taking photos  

        • Be polite with locals

        """

    }


    st.write(fallback_data.get(fallback_type, ""))


def nearby_experience_places(destination, experience):

    prompt = f"""

    The user is traveling to {destination} and wants a {experience} experience.


    Suggest 4–6 nearby or easily reachable places (within a few hours)

    that match this experience.


    Return ONLY a bullet list of place names with a short note in brackets.

    """

    return ai_response(prompt)

st.markdown('<p class="main-title">🧭 Urban Travel Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Plan your perfect trip with AI ✈️</p>', unsafe_allow_html=True)

# ---------- SESSION STATE ----------

# --- SESSION STATE INITIALIZATION ---

def get_ai_info(prompt):

    try:

        response = client.models.generate_content(

            model="models/gemini-flash-lite-latest",

            contents=prompt

        )

        return response.text

    except Exception as e:

        return "⚠️ AI service is temporarily unavailable. Please try again in a minute."
if "data" not in st.session_state:

    st.session_state.data = {}


# 🔑 PLACE YOUR NEW INITIALIZATIONS HERE:

if "tips_output" not in st.session_state:

    st.session_state.tips_output = None

if "culture_output" not in st.session_state:

    st.session_state.culture_output = None

if "safety_output" not in st.session_state:

    st.session_state.safety_output = None


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

# ---------- STEP 1: START ----------

if st.session_state.step == "start":

    st.subheader("👋 Welcome to Urban Travel Assistant!")

    st.markdown('<div class="box">', unsafe_allow_html=True)

choice = st.radio(
    "🌍 What would you like to do?",
    [
        "📍 I already know my destination",
        "✨ Get AI travel suggestions"
    ]
)



# =====================================================================
# 🔹 FLOW 1: USER WITH SPECIFIC PLACE
# =====================================================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


if st.session_state.step == "destination":

    st.subheader("📍 Enter Destination")

    dest = st.text_input("City / State / Country")


    if st.button("Next") and dest:

        st.session_state.data["destination"] = dest

        st.session_state.step = "experience"




if st.session_state.step == "experience":

    st.subheader("🎯 What kind of experience?")


    exp = st.selectbox(

        "Select experience type:",

        ["Adventure", "Devotional", "Nature", "Historical", "Leisure", "Beach"],

        key="experience_select"

    )


    if st.button("Next", key="next_experience"):

        st.session_state.data["experience"] = exp

        st.session_state.step = "travel_style"

        st.rerun()


if st.session_state.step == "travel_style":

    st.subheader("👥 Who are you traveling with?")


    style = st.selectbox(

        "Select travel style:",

        ["Solo", "Friends", "Family", "Couple"],

        key="travel_style_select"

    )


    if st.button("Next", key="next_travel_style"):

        st.session_state.data["travel_style"] = style

        st.session_state.step = "summary"

        st.rerun()

if st.session_state.step == "summary":

    st.subheader("🔎 Confirm Your Travel Preferences")

   

    with st.container(border=True):

        # Pull data safely using .get() to avoid errors

        dest = st.session_state.data.get('destination', 'AI Choice')

        exp = st.session_state.data.get('experience', 'Not Selected')

        style = st.session_state.data.get('travel_style', 'Not Selected')

       

        st.markdown(f"📍 **Destination:** {dest}")

        st.markdown(f"✨ **Experience:** {exp}")

        st.markdown(f"👥 **Travel Style:** {style}")

        if "duration" in st.session_state.data:

            st.markdown(f"📅 **Stay:** {st.session_state.data['duration']} Days")


    change = st.selectbox(

        "Is everything correct?",

        ["Yes, everything is perfect", "Change destination", "Change experience", "Change travel style"]

    )


    if st.button("Continue to Trip Planning"):

        if change == "Yes, everything is perfect":

            st.session_state.step = "overview"

        else:

            mapping = {"Change destination": "destination", "Change experience": "experience", "Change travel style": "travel_style"}

            st.session_state.step = mapping[change]

        st.rerun()


if st.session_state.step == "overview":

    # 🔑 ADD THESE TWO LINES TO PREVENT NAMEERROR

    destination = st.session_state.data.get("destination")

    experience = st.session_state.data.get("experience")


    st.subheader(f"🌟 {destination} – {experience} Experience")

    # ... rest of your code


    prompt = f"Give a short travel overview of {destination}."

    st.write(cached_ai_response(prompt))


    st.markdown(f"### 🧭 Nearby places for {experience} experience")


    # Now these variables exist and won't cause a NameError

    nearby_places = nearby_experience_places(destination, experience)

    st.write(nearby_places)


    if st.button("Continue", key="overview_continue"):

        st.session_state.step = "attractions"

        st.rerun()

# ---------- OPTIONAL SECTIONS ----------

def yes_no_step(title, yes_text, next_step):

    st.subheader(title)


    choice = st.radio(

        "Choose an option:",

        ["Yes", "No"],

        key=f"radio_{title}"   # 🔑 UNIQUE KEY

    )


    if st.button("Next", key=f"next_{title}"):

        if choice == "Yes":

            st.info(yes_text)

        st.session_state.step = next_step

        st.rerun()

if st.session_state.step == "attractions":

    destination = st.session_state.data["destination"]

    st.subheader(f"🌲 Top Attractions in {destination}")


    # 1. Initialize storage for attractions if not already there

    if "attractions_output" not in st.session_state:

        st.session_state.attractions_output = None


    choice = st.radio(

        "Would you like to explore famous tourist attractions here?",

        ["Yes", "No"],

        key="attractions_choice"

    )


    if st.button("Show Attractions", key="btn_show_attractions"):

        if choice == "Yes":

            prompt = f"""

List 5–6 MUST-VISIT tourist attractions in {destination}.

These places should be:

- Most visited by tourists

- Iconic and popular

- Cannot be missed when visiting {destination}


Return ONLY bullet points with short descriptions.

"""

            # Save the AI response to session state

            st.session_state.attractions_output = cached_ai_response(prompt)

        else:

            st.session_state.attractions_output = "Skipping attractions section."


    # 2. ALWAYS display the output if it exists in the memory

    if st.session_state.attractions_output:

        st.markdown(st.session_state.attractions_output)

       

        # 3. Only show the 'Continue' button AFTER the info is displayed

        if st.button("Continue to Food 🍽️", key="btn_goto_food"):

            st.session_state.attractions_output = None # Clear memory for next time

            st.session_state.step = "food"

            st.rerun()


if st.session_state.step == "food":

    st.subheader("🍽 Local Food")

   

    # Check if we already have the result in memory

    if "food_result" not in st.session_state:

        st.session_state.food_result = None


    choice = st.radio("Would you like local food suggestions?", ["Yes", "No"], key="food_radio")


    if st.button("Show Food Suggestions"):

        if choice == "Yes":

            prompt = f"List popular local foods in {st.session_state.data['destination']}."

            st.session_state.food_result = cached_ai_response(prompt)

        else:

            st.session_state.food_result = "Skipped food suggestions."


    # Always show the result if it exists in memory

    if st.session_state.food_result:

        st.write(st.session_state.food_result)

        if st.button("Continue to Clothing"):

            st.session_state.step = "clothing"

            st.rerun()


    # ✅ SHOW FOOD OUTPUT

if st.session_state.step == "clothing":

    # 🔑 Pull variable from state to prevent NameError

    destination = st.session_state.data.get("destination")


    st.subheader("👕 Clothing Suggestions")


    # Initialize storage in session state

    if "clothing_output" not in st.session_state:

        st.session_state.clothing_output = None


    choice = st.radio(

        "Would you like clothing suggestions based on the climate?",

        ["Yes", "No"],

        key="clothing_radio"

    )


    # Use a specific button to trigger the AI

    if st.button("Show Clothing Suggestions", key="btn_show_clothing"):

        if choice == "Yes":

            prompt = f"Suggest appropriate clothing for traveling to {destination} based on climate. Return ONLY bullet points."

            # Save response to memory

            st.session_state.clothing_output = cached_ai_response(prompt)

        else:

            st.session_state.clothing_output = "You chose to skip clothing suggestions."


    # ALWAYS display the stored response if it exists

    if st.session_state.clothing_output:

        st.info(f"👗 Recommended for {destination}:")

        st.write(st.session_state.clothing_output)

       

        # Only show the 'Continue' button AFTER suggestions appear

        if st.button("Continue to Travel Tips ✈️", key="btn_go_to_tips"):

            st.session_state.clothing_output = None # Clear for next run

            st.session_state.step = "tips"

            st.rerun()






if st.session_state.step == "tips":

    destination = st.session_state.data["destination"]


    st.subheader("✈️ Travel Tips")


    choice = st.radio(

        "Would you like travel tips for this destination?",

        ["Yes", "No"],

        key="tips_radio"

    )


    if st.button("Show Travel Tips"):

        if choice == "Yes":

            prompt = f"""

            Give 4–5 practical travel tips for visiting {destination}.

            Return ONLY bullet points.

            """

            st.session_state.tips_output = cached_ai_response(prompt)

        else:

            st.session_state.tips_output = "You chose to skip travel tips."


    if st.session_state.tips_output:

        st.markdown("### ✈️ Helpful Travel Tips")


        if "⚠️" in st.session_state.tips_output:

            smart_ai_section("", "tips", destination)

        else:

            st.write(st.session_state.tips_output)


        if st.button("Continue to Safety"):

            st.session_state.tips_output = None

            st.session_state.step = "safety"

            st.rerun()


if st.session_state.step == "safety":

    destination = st.session_state.data.get("destination") # Pull from state

    st.subheader("🛡️ Safety Tips")


    if "safety_output" not in st.session_state:

        st.session_state.safety_output = None


    choice = st.radio("Would you like safety tips?", ["Yes", "No"], key="safety_radio")


    if st.button("Show Safety Tips"):

        if choice == "Yes":

            prompt = f"List important safety tips for travelers visiting {destination}. Return ONLY bullet points."

            st.session_state.safety_output = cached_ai_response(prompt)

        else:

            st.session_state.safety_output = "Skipped safety tips."


    # Always display the result if it exists in memory

    if st.session_state.safety_output:

        st.write(st.session_state.safety_output)

        if st.button("Next to Cultural Etiquette"):

            st.session_state.step = "culture"

            st.rerun()


# Pull data from memory at the start of the block to prevent NameError

destination = st.session_state.data.get("destination")

experience = st.session_state.data.get("experience")

if st.session_state.step == "culture":

    # Pull data safely to prevent NameError

    destination = st.session_state.data.get("destination")

    st.subheader("🙏 Cultural Etiquette")


    # Initialize a specific key to store the culture output in memory

    if "culture_output" not in st.session_state:

        st.session_state.culture_output = None


    choice = st.radio(

        "Would you like to know cultural etiquette and local customs?",

        ["Yes", "No"],

        key="culture_radio"

    )


    # 1. Action Button: Show the info

    if st.button("Show Etiquette Tips", key="btn_show_culture"):

        if choice == "Yes":

            prompt = f"""

            Explain important cultural etiquette and local customs

            travelers should follow in {destination}.

            Return ONLY bullet points.

            """

            # Store the response so it persists through reruns

            st.session_state.culture_output = cached_ai_response(prompt)

        else:

            st.session_state.culture_output = "You chose to skip cultural etiquette."


    # 2. Display: Always show the info if it exists in session_state

    if st.session_state.culture_output:

        st.write(st.session_state.culture_output)

       

        # 3. Navigation: Only show 'Continue' AFTER the user has seen the info

        if st.button("Continue to Checklist 🧳", key="btn_culture_done"):

            st.session_state.culture_output = None # Clear memory for fresh start next time

            st.session_state.step = "checklist"

            st.rerun()




if st.session_state.step == "checklist":

    st.header("🧳 Your Ultimate Travel Essentials")

    st.write("Check off items as you pack. Your progress is saved automatically!")


    # Define Categories and Items

    categories = {

        "👕 Wardrobe & Linens": [

            "Apparel & Dresses", "Innerwear", "Soft Towels",

            "Traditional Chunnis", "Travel Blankets", "Napkins/Handkerchiefs"

        ],

        "🧼 Personal Care & Toiletries": [

            "Dental Kit (Paste/Brush/Tongue Cleaner)", "Hand Sanitizer & Hand Wash",

            "Body Soap", "Pooja Essentials (Turmeric/Kumkum/Kumkum Paste)",

            "Soft Tissue Papers", "Moisturizer/Face Cream", "Face Powder & Puff"

        ],

        "✨ Grooming & Accessories": [

            "Bangles & Earrings", "Hair Clips & Safety Pins",

            "Bindi/Stickers", "Combs & Hairbrushes"

        ],

        "💊 Health & Wellness": [

            "Prescribed Tablets", "Zandu Balm/Pain Relief",

            "First Aid Cotton", "Sanitary Essentials"

        ],

        "🔌 Electronics & Gadgets": [

            "Smartphones", "High-Speed Phone Chargers",

            "Travel Hair Dryer", "Electric Kettle",

            "Power Bank (Added Essential 🔋)", "Universal Adapter (Added Essential 🔌)"

        ],

        "🍎 Pantry & Food Supplies": [

            "Biscuits & Travel Snacks", "Daniyalu (Coriander Seeds)",

            "Eco-friendly Paper Plates", "Disposable Spoons"

        ],

        "📄 Critical Documents": [

            "Original Aadhaar Cards", "Xerox Copies of ID Proofs",

            "Confirmed Travel Tickets", "Hotel Booking Vouchers (Added Essential 🏨)"

        ],

        "🎒 Misc. Comfort Items": [

            "Ergonomic Car Pillows", "Empty Storage Boxes & Covers",

            "Travel Handbags", "Small Coconut Oil", "Refreshing Body Spray",

            "Reusable Drinking Glass"

        ]

    }


    # Interactive UI

    for category, items in categories.items():

        with st.expander(category, expanded=True):

            for item in items:

                st.checkbox(item, key=f"check_{item}")


    # Add Custom Item Logic

    st.divider()

    st.subheader("➕ Add Personal Items")

    new_item = st.text_input("Need to pack something else?", placeholder="e.g., Camera, Sunglasses...")

   

    if st.button("Add to My List") and new_item:

        # Assuming you have a list in session_state for custom items

        if "custom_list" not in st.session_state:

            st.session_state.custom_list = []

        st.session_state.custom_list.append(new_item)

        st.rerun()


    # Display Custom Items

    if "custom_list" in st.session_state:

        for c_item in st.session_state.custom_list:

            st.checkbox(c_item, key=f"custom_{c_item}", value=True)


    if st.button("Finalize & Continue", type="primary"):

        st.session_state.step = "open_chat"

        st.rerun()
if st.session_state.step == "open_chat":
    st.subheader("💬 Chat with AI")
    
    # 1. Render history correctly from tuples
    for role, msg in st.session_state.chat_history:
        with st.chat_message("user" if role == "You" else "assistant"):
            st.write(msg)

    # 2. Chat Input
    if q := st.chat_input("Ask me anything about your trip...", key="chat_input_unique"):
        dest = st.session_state.data.get("destination")
        ans = get_ai_info(f"As a travel bot for {dest}, answer: {q}")
        st.session_state.chat_history.append(("You", q))
        st.session_state.chat_history.append(("Bot", ans))
        st.rerun()

    st.write("---")

# --- FIXED EXIT LOGIC ---

# =====================================================================
# 🔹 FLOW 2: USER WITHOUT SPECIFIC PLACE
# =====================================================================
if st.session_state.step == "scope":
    st.subheader("🌍 Travel Scope")
    scope = st.selectbox("Where would you like to travel?", ["National", "International", "Anywhere"], key="scope_sel")
    
    # 🔑 FIX: Added unique key 'btn_scope_next'
    if st.button("Next", key="btn_scope_next"):
        st.session_state.data["scope"] = scope
        st.session_state.step = "exp2"
        st.rerun() # 🔑 FIX: Clears the screen to move to next step

if st.session_state.step == "exp2":
    st.subheader("🎯 Type of Experience")
    exp = st.selectbox("What kind of experience?", ["Adventure", "Devotional", "Nature", "Historical", "Leisure", "Beach"], key="exp2_sel")
    
    # 🔑 FIX: Added unique key 'btn_exp_next'
    if st.button("Next", key="btn_exp_next"):
        st.session_state.data["experience"] = exp
        st.session_state.step = "style2"
        st.rerun()
        
if st.session_state.step == "style2":
    st.subheader("👥 Travel Style")
    # 🔑 FIX: Ensure this value is saved to session_state.data
    style = st.selectbox("Who are you traveling with?", ["Solo", "Friends", "Family", "Couple", "Day Trip"], key="style2_sel")
    
    if st.button("Next", key="btn_style2_next"):
        # 🔑 SAVE THE DATA HERE to prevent KeyError
        st.session_state.data["travel_style"] = style 
        st.session_state.step = "budget_duration"
        st.rerun()

       

# Ensure this block is visible and reachable

if st.session_state.step == "budget_duration":

    st.subheader("⏰ Duration & 💰 Budget")

   

    col1, col2 = st.columns(2)

    with col1:

        days = st.number_input("How many days?", min_value=1, max_value=30, value=4)

    with col2:

        budget = st.selectbox("Budget Range", ["Economy", "Mid-range", "Luxury", "Skip"])


    if st.button("Generate Recommendations"):

        st.session_state.data["duration"] = days

        st.session_state.data["budget"] = budget

        st.session_state.step = "suggest"

        st.rerun()

if st.session_state.step == "suggest":
    st.subheader("✨ Suggested Destinations")

    # Safe data retrieval using .get() to prevent crashes
    scope = st.session_state.data.get("scope", "National")
    experience = st.session_state.data.get("experience", "Adventure")
    style = st.session_state.data.get("travel_style", "Solo")

    prompt = f"Suggest all {scope} destinations for a {experience} and a {style} trip with details (Best time, Duration). Return as a list."
    response = ai_response(prompt) 

    # 🔑 FIX: Prevent selectbox crash if AI returns an error
    if "⚠️" in response:
        st.error("AI is temporarily busy. Please type a destination below manually.")
        places = []
    else:
        places = [p.strip("-• ") for p in response.split("\n") if p.strip()]

    selected_place = st.selectbox("Choose a destination", places if places else ["Type manually..."], key="suggest_place_f2")
    manual_place = st.text_input("Or enter destination manually:", key="manual_dest_f2")

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Explore", key="btn_explore_f2"):
            st.session_state.data["destination"] = manual_place if manual_place else selected_place
            st.session_state.step = "overview"
            st.rerun()
    with col2:
        if st.button("Exit App", key="btn_exit_suggest_f2"):
            st.session_state.clear()
            st.rerun()
if st.session_state.step == "open_chat":
    st.subheader("💬 Chat with AI")
    dest = st.session_state.data.get("destination", "your destination")
    
    # 1. Existing loop to show chat history
    for role, msg in st.session_state.chat_history:
        with st.chat_message("user" if role == "You" else "assistant"):
            st.write(msg)

    # 2. Existing chat input logic
    if q := st.chat_input("Ask me anything about your trip...", key="chat_input_final"):
        ans = get_ai_info(f"As a travel bot for {dest}, answer: {q}")
        st.session_state.chat_history.append(("You", q))
        st.session_state.chat_history.append(("Bot", ans))
        st.rerun() # 🔑 Refreshes screen to show new messages

    # --- 🚩 ADD THE NEW CODE BELOW THIS LINE ---
    st.write("---") # Visual separator

    col1, col2 = st.columns([2, 1])
    with col1:
        # This button moves the user to the 'final_page' step
        if st.button("Finish Conversation & Move to Next Step ➡️", key="btn_goto_final"):
            st.session_state.step = "final_page"
            st.rerun() # 🔑 Forces the app to switch screens
    with col2:
        # Unique key prevents DuplicateElementId error
        if st.button("Exit App", key="btn_exit_from_chat"):
            st.session_state.clear() # Clears session memory
            st.rerun()
# --- STEP 19: FINAL NAVIGATION (Dropdown logic from your request) ---
if st.session_state.step == "final_page":
    st.subheader("🧭 Urban Travel Assistant")
    st.write("### What would you like to do next?")
    
    action = st.selectbox(
        "Choose an option:", 
        ["Select...", "Explore another suggested place", "Start a new trip", "Exit App"], 
        key="final_nav_dropdown_shared"
    )
    
    if st.button("Confirm Action", key="btn_confirm_final_shared"):
        if action == "Start a new trip":
            st.session_state.clear() # Resets the entire app
            st.rerun()
        elif action == "Explore another suggested place":
            st.session_state.step = "suggest" # Jumps back to Flow 2 suggestions
            st.rerun()
        elif action == "Exit App":
            st.balloons()
            st.success("Thank you for using Urban Travel Assistant! Safe travels! 🧭")
            st.stop() # Terminates the app session