import streamlit as st
import pymongo
from pymongo.errors import ServerSelectionTimeoutError
from datetime import datetime

st.title("Hjertekramper 🫀💢")

# Load secrets or configuration
mongo_config = {
    "uri": st.secrets["mongo"]["uri"]
}

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource()
def init_connection():
    try:
        client = pymongo.MongoClient(mongo_config["uri"])
        client.server_info()  # Check if the client can connect to the server
        return client
    except ServerSelectionTimeoutError as err:
        st.error(f"Failed to connect to MongoDB: {err}")
        return None

client = init_connection()

if client:
    # Function to insert a new heart cramp event
    def insert_heart_cramp():
        db = client.get_database("mydb")
        collection = db.get_collection("heart_cramps")
        current_time = datetime.now()
        collection.insert_one({"timestamp": current_time})
        st.success("Hjertekrampe registrert.")

    # Display UI to insert a new heart cramp event
    if st.button("Jeg har hjertekrampe nå"):
        insert_heart_cramp()

    # Display all recorded heart cramp events
    st.subheader("Registrerte hjertekramper:")
    db = client.get_database("mydb")
    collection = db.get_collection("heart_cramps")
    events = collection.find()

    for event in events:
        time = event['timestamp']
        formatted_time = time.strftime("%d.%m.%y – %H:%M")
        st.write(f"- Tidspunkt: {formatted_time}")

else:
    st.error("Could not establish a connection to MongoDB.")