# --------------------------
# Café knowledge base
# --------------------------

HOURS = {
    "monday": "8:00 AM – 8:00 PM",
    "tuesday": "8:00 AM – 8:00 PM",
    "wednesday": "8:00 AM – 8:00 PM",
    "thursday": "8:00 AM – 8:00 PM",
    "friday": "8:00 AM – 9:00 PM",
    "saturday": "8:00 AM – 9:00 PM",
    "sunday": "9:00 AM – 5:00 PM"
}

FAQS = [
    {
        "question": "Do you provide free Wi-Fi?",
        "answer": "Yes, Wi-Fi is free for all customers. Ask staff for the password."
    },
    {
        "question": "Do you have vegan options?",
        "answer": "Yes, we have vegan options available on our menu."
    },
    {
        "question": "What payment methods do you accept?",
        "answer": "We accept cash, UPI, credit cards, and debit cards."
    },
    {
        "question": "How long does food preparation take?",
        "answer": "Average preparation time is 5–7 minutes for drinks and 8–12 minutes for food items."
    },
    {
        "question": "Do I need a reservation?",
        "answer": "Reservations are not required for small groups, but we recommend booking in advance for parties of 6 or more."
    },
    {
        "question": "Can I order takeaway or delivery?",
        "answer": "Yes, we provide takeaway and delivery options for most menu items."
    },
    {
        "question": "Is the café pet-friendly?",
        "answer": "Yes, pets are welcome in our outdoor seating area."
    },

    {
        "question": "Do you offer student discounts?",
        "answer": "Yes, students get a 10% discount with a valid student ID."
    },
    {
        "question": "Is parking available at the café?",
        "answer": "Yes, parking is available for both two-wheelers and cars near the café."
    }
]

MENU = [
    # name, price (INR), tags, description
    ("Paneer Tikka", 180, ["vegetarian", "spicy", "high-protein"], "Grilled paneer cubes with spices"),
    ("Veg Biryani", 200, ["vegetarian", "spicy"], "Rice with veggies and Indian spices"),
    ("Chicken Wings", 220, ["non-veg", "spicy"], "Hot and crispy wings"),
    ("Spicy Veg Wrap", 150, ["vegetarian", "spicy"], "Veg wrap with chili sauce"),
    ("Masala Chai", 120, ["vegetarian","hot","sweet"], "Spiced Indian tea with milk and sugar."),
    ("Cold Brew Coffee", 180, ["vegetarian","cold","caffeine"], "Slow‑brewed, smooth and bold."),
    ("Veg Sandwich", 150, ["vegetarian"], "Lettuce, tomato, cucumber, cheese in brown bread."),
    ("Paneer Tikka Bowl", 260, ["vegetarian","high-protein","spicy"], "Grilled paneer with veggies and mint yogurt."),
    ("Chicken Wrap", 220, ["non-veg","high-protein","spicy"], "Grilled chicken, lettuce, onions, tangy sauce."),
    ("Caesar Salad", 210, ["non-veg"], "Crisp lettuce, dressing, chicken, croutons."),
    ("Fruit Smoothie", 160, ["vegetarian","cold","sweet"], "Banana, berries, yogurt; no added sugar."),
    ("Espresso", 140, ["vegetarian","hot","caffeine"], "Classic single shot."),
    ("Iced Latte", 190, ["vegetarian","cold","caffeine"], "Milk + espresso over ice."),
    ("Chocolate Brownie", 130, ["vegetarian","sweet","dessert"], "Rich, fudgy chocolate square."),
    # Veg items
    ("Margherita Pizza", 250, ["vegetarian"], "Classic cheese pizza"),
    ("Paneer Butter Masala", 220, ["vegetarian"], "Paneer in creamy tomato gravy"),
    ("Veggie Burger", 180, ["vegetarian", "high-protein"], "Loaded veg burger"),
    ("Spicy Veg Wrap", 150, ["vegetarian", "spicy"], "Veg wrap with chili sauce"),
    ("Brownie", 120, ["vegetarian", "sweet", "dessert"], "Chocolate brownie"),
    
    # Non-veg items
    ("Chicken Biryani", 280, ["non-veg", "spicy"], "Hyderabadi chicken biryani"),
    ("Grilled Chicken Sandwich", 200, ["non-veg"], "Chicken sandwich with veggies"),
    ("Fish Fry", 260, ["non-veg", "spicy"], "Crispy fried fish"),
    
    # Beverages
    ("Iced Latte", 190, ["cold", "caffeine"], "Chilled coffee with milk"),
    ("Green Tea", 120, ["caffeine-free"], "Refreshing herbal tea"),
    ("Mango Smoothie", 150, ["cold", "vegetarian", "sweet"], "Fresh mango smoothie"),
]

# Build plain-text docs for embedding / retrieval
def build_documents():
    docs = []
    # Hours
    docs.append({
        "id": "hours",
        "text": "Our café hours are: " + ", ".join(f"{d.title()}: {t}" for d,t in HOURS.items())
    })
    # Menu
    for name, price, tags, desc in MENU:
        docs.append({
            "id": f"menu::{name}",
            "text": f"{name} — ₹{price}. {desc} Tags: {', '.join(tags)}."
        })
    # FAQs
    for i, f in enumerate(FAQS):
        docs.append({
             "id": f"faq::{i}",
             "text": f"Q: {f['question']} A: {f['answer']}"
        })
    return docs

DOCUMENTS = build_documents()
