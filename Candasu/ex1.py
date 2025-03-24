# poem='ಹೇಯಂಗಳ್ ಖಳಕರ್ಮಬಂಧನಕರ ಕ್ರೋಧಾದಿಗಳ್ ಮತ್ತುಪಾ ದೇಯಂಗಳ್ ದುರಿತೇಂಧನಾನಳಲಸದ್ರತ್ನತ್ರಯಂಗಳ್ ಸುಖೋ ಪಾಯಂಗಳ್ಗಡಿವೆಂದು ಭವ್ಯಜನಮಂ ಕಣ್ಣೂಱಿ ಕಲ್ಪಿಪ್ಪುಪಾ ಧ್ಯಾಯಜ್ರ್ಯೋತಿಸುಗೆಮ್ಮ ಚಿತ್ತಗೃಹದೊಳ್ರತ್ನತ್ರಯಜ್ಯೋತಿಯಂ'
# from  keras.models import load_model
# import numpy as np
# import tensorflow as tf
# model1 = load_model('model.h5')
# tokenizer = tf.keras.preprocessing.text.Tokenizer()
# import numpy as np
# import tensorflow as tf

# sentence='ಹೇಯಂಗಳ್ ಖಳಕರ್ಮಬಂಧನಕರ ಕ್ರೋಧಾದಿಗಳ್ ಮತ್ತುಪಾ ದೇಯಂಗಳ್ ದುರಿತೇಂಧನಾನಳಲಸದ್ರತ್ನತ್ರಯಂಗಳ್ ಸುಖೋ ಪಾಯಂಗಳ್ಗಡಿವೆಂದು ಭವ್ಯಜನಮಂ ಕಣ್ಣೂಱಿ ಕಲ್ಪಿಪ್ಪುಪಾ ಧ್ಯಾಯಜ್ರ್ಯೋತಿಸುಗೆಮ್ಮ ಚಿತ್ತಗೃಹದೊಳ್ರತ್ನತ್ರಯಜ್ಯೋತಿಯಂ'
# poem=sentence.strip().split()
# i=0
# while(i<len(poem)):
#     print(poem[i],len(poem[i]))
#     if(len(poem[i])<=2 and i+1<len(poem)):
#         poem[i+1]=poem[i]+poem[i+1]
#         poem.remove(poem[i])
#     else:
#         i+=1
# ans = ""
# for i in poem:
#     input_sequence = tokenizer.texts_to_sequences([i])
#     input_sequence_padded = tf.keras.preprocessing.sequence.pad_sequences(input_sequence, maxlen=8, padding='post')

#     # Predict
#     predicted_output_sequence = model1.predict(input_sequence_padded)[0]
#     predicted_word_indices = np.argmax(predicted_output_sequence, axis=-1)

#     # Convert predicted word indices to words
#     predicted_words = tokenizer.sequences_to_texts([predicted_word_indices])[0].strip()
#     print(predicted_words)
#     if(predicted_words==""):
#         ans+=i+" "
#     else:
#         ans+=predicted_words+" "

# print(ans)


import streamlit as st
import mysql.connector
import datetime
from streamlit import session_state as ss
# Connect to your MySQL database
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="root",
    database="onlinevotingdb"
)
cursor = conn.cursor()
if 'logged_in' not in ss:
    ss.logged_in = False


# Streamlit App
st.title("Online Voting System")

# Function to fetch district IDs from the database


def district_id_ui():
    # Fetch district IDs from the Address table
    cursor.execute("SELECT DistrictID, Locality FROM Address")
    districts = cursor.fetchall()

    # Create a list of district options for the selectbox
    district_options = [
        f"{district[0]} - {district[1]}" for district in districts]

    # Display the selectbox in Streamlit
    district_id = st.selectbox("Select District", district_options)

    # Extract the selected DistrictID from the option
    selected_district_id = int(district_id.split(" - ")[0])

    return selected_district_id


# Sign Up Section
st.subheader("Sign Up")
aadhaar = st.text_input("Aadhaar number:", key="aadhaar_input")
fname = st.text_input("First Name:", key="fname_input")
lname = st.text_input("Last Name:", key="lname_input")
mname = st.text_input("Mother Name:", key="mname_input")
fathername = st.text_input("Father Name:", key="fathername_input")
sex = st.selectbox("Gender", ["F", "M", "Other"], key="sex_selectbox")
age = st.number_input("Enter age", key="age_input")
Birthday = st.date_input("Enter birthday", key="birthday_input")
phone = st.text_input("Phone Number:", key="phone_input")
district_id_signup = district_id_ui()
# Add district UI to sign-up section

# Handle Sign Up button click
if st.button("Sign Up"):
    try:
        # Convert the Streamlit date input to a string
        birthday_str = Birthday.strftime("%Y-%m-%d")

        # Insert data into the database
        cursor.execute("""
            INSERT INTO Voter_Table (AADHAAR, FirstName, LastName, MotherName, Birthday, FatherName, Sex, Age, DistrictID, Phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (aadhaar, fname, lname, mname, birthday_str, fathername, sex, age, district_id_signup, phone))
        conn.commit()

        st.success("Signup successful!")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    except ValueError:
        st.error("Error: Invalid date format.")
    finally:
        cursor.close()

# Login Section
st.subheader("Login")
aadhaar_login = st.text_input("Aadhaar number:")

# Handle Login button click
if st.button("Login"):
    try:
        # Check if the entered Aadhaar number matches the records in the database
        cursor.execute(
            "SELECT * FROM Voter_Table WHERE AADHAAR = %s", (aadhaar_login,))
        user = cursor.fetchone()

        if user:
            st.success("Login successful!")
            ss.logged_in = True
        else:
            st.error("Invalid Aadhaar number. Please try again.")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    # finally:
    #     cursor.close()

# If logged in, proceed to Election Type or Candidate Type
if ss.logged_in:
    # Election Type Section
    st.subheader("Select Election Type")
    cursor.execute("SELECT ElectionID, ElectionType FROM Election_Table")
    elections = cursor.fetchall()
    election_options = [
        f"{election[0]} - {election[1]}" for election in elections]
    selected_election = st.selectbox("Select Election", election_options)

    # Candidate Type Section
    st.subheader("Select Candidate Type")
    cursor.execute("SELECT CandidateTypeID, CandidateType FROM Candidate_Type")
    candidate_types = cursor.fetchall()
    candidate_type_options = [
        f"{c_type[0]} - {c_type[1]}" for c_type in candidate_types]
    selected_candidate_type = st.selectbox(
        "Select Candidate Type", candidate_type_options)

    # Voting Section
    st.subheader("Vote for a Candidate")
    cursor.execute("SELECT CandidateID, AADHAAR, PartyID, ElectionID, DistrictID FROM Candidate_Table WHERE CandidateTypeID = %s",
                   (selected_candidate_type.split(" - ")[0],))
    candidates = cursor.fetchall()
    candidate_options = [
        f"{candidate[0]} - {candidate[1]}" for candidate in candidates]
    selected_candidate = st.selectbox("Select Candidate", candidate_options)

    # Handle Vote button click
if st.button("Vote"):

    # Check if the user has already voted for this candidate
    cursor.execute("SELECT * FROM Result WHERE CandidateID = %s AND DistrictID = %s",
                   (selected_candidate.split(" - ")[0], candidates[0][4]))
    existing_vote = cursor.fetchone()

    if existing_vote:
        # If the user has already voted, update the existing row to increment the vote count
        cursor.execute("""
                UPDATE Result
                SET Vote_Count = Vote_Count + 1
                WHERE CandidateID = %s AND DistrictID = %s
            """, (selected_candidate.split(" - ")[0], candidates[0][4]))
    else:
        # If the user hasn't voted yet, insert a new row
        cursor.execute("""
                INSERT INTO Result (CandidateID, PartyID, DistrictID, Vote_Count)
                VALUES (%s, %s, %s, %s)
            """, (selected_candidate.split(" - ")[0], candidates[0][2], candidates[0][4], 1))  # Assuming vote count starts at 1
    conn.commit()

    st.success("Vote recorded successfully!")
st.header("Aggregative Query")

# Get the total number of votes for each candidate
cursor.execute("""
    SELECT CandidateID, COUNT(*) as TotalVotes
    FROM Result
    GROUP BY CandidateID
""")
vote_counts = cursor.fetchall()

# Display the results
st.subheader("Total Votes for Each Candidate")
for vote_count in vote_counts:
    st.write(f"Candidate ID: {vote_count[0]}, Total Votes: {vote_count[1]}")

# Section for Nested Query
st.header("Nested Query")

# Get the details of the candidates who received the maximum votes in each district
cursor.execute("""
    SELECT r.CandidateID, r.DistrictID, r.Vote_Count, c.AADHAAR, c.PartyID
    FROM Result r
    INNER JOIN (
        SELECT DistrictID, MAX(Vote_Count) as MaxVotes
        FROM Result
        GROUP BY DistrictID
    ) max_votes ON r.DistrictID = max_votes.DistrictID AND r.Vote_Count = max_votes.MaxVotes
    INNER JOIN Candidate_Table c ON r.CandidateID = c.CandidateID
""")
max_votes_details = cursor.fetchall()

# Display the results
st.subheader("Candidates with Maximum Votes in Each District")
for details in max_votes_details:
    st.write(
        f"Candidate ID: {details[0]}, District ID: {details[1]}, Vote Count: {details[2]}, AADHAAR: {details[3]}, Party ID: {details[4]}")

# Close the database connection
conn.close()