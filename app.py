from flask import Flask, request, jsonify
import re
from datetime import datetime, timedelta
import psycopg2, json, requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from flask_cors import CORS  # Add this import
app = Flask(__name__)
CORS(app)

# Database configuration
db_connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="TWbyVdR1rt%+",
    host="3.75.212.152"
)

@app.route('/')
def hello():
    return 'Hello, Flask!'

@app.route('/getSystems', methods=['GET'])#, 'POST'])
def getSystems():
    if request.method == 'GET':
        try:
            cursor = db_connection.cursor()
            query = "SELECT * FROM systems"
            cursor.execute(query)
            items = cursor.fetchall()
            json_array = [{'id': item[0], 'name': item[1], 'intents_count': item[2]} for item in items]
            
            # Convert the list of dictionaries to a objects
            systems = json.dumps(json_array, indent=4, sort_keys=True, default=str) #fixing datetime bug on json parse

            cursor.close()

            return systems

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/getNameForSystem', methods=['GET'])
def getNameForSystem():
    if request.method == 'GET':
        try:
            system_id = request.args.get('system_id')
            cursor = db_connection.cursor()
            query = f"SELECT system_name FROM systems WHERE system_id = {system_id}"
            cursor.execute(query)
            items = cursor.fetchall()

            cursor.close()

            return jsonify(items[0][0])

        except Exception as e:
            return jsonify(str(e))

@app.route('/getIntentsForSystem', methods=['GET'])#, 'POST'])
def getIntentsForSystem():
    if request.method == 'GET':
        try:
            system_id = request.args.get('system_id')
            cursor = db_connection.cursor()
            query = f"SELECT * FROM intents WHERE system_id = {system_id}"
            cursor.execute(query)
            items = cursor.fetchall()
            json_array = [{'id': item[0], 'name': item[1], 'last_edited': item[2], 'examples_count': item[3], 'steps_count': item[4]} for item in items]
            
            # Convert the list of dictionaries to a objects
            intents = json.dumps(json_array, indent=4, sort_keys=True, default=str) #fixing datetime bug on json parse

            cursor.close()

            return intents

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/getConversationsForSystem', methods=['GET'])
def getConversationsForSystem():
    if request.method == 'GET':
        try:
            system_id = request.args.get('system_id')
            cursor = db_connection.cursor()
            query = f"SELECT * FROM conversations WHERE system_id = {system_id}"
            cursor.execute(query)
        
            items = cursor.fetchall()
            json_array = [{'conversation_id': item[0], 'session_id': item[1], 'time': item[2], 'system_id': item[3], 'intent_id': item[4], 'text': item[5], 'thumbs_up': item[6], 'thumbs_down': item[7], 'threshold': item[8], 'intent_name': item[9]} for item in items]

            # Convert the list of dictionaries to a objects
            conversations = json.dumps(json_array, indent=8, sort_keys=True, default=str) #fixing datetime bug on json parse

            cursor.close()

            return conversations

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/getNameForIntent', methods=['GET'])
def getNameForIntent():
    if request.method == 'GET':
        try:
            intent_id = request.args.get('intent_id')
            cursor = db_connection.cursor()
            query = f"SELECT intent_name FROM intents WHERE intent_id = {intent_id}"
            cursor.execute(query)
            items = cursor.fetchall()

            cursor.close()

            return jsonify(items[0][0])

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/getQuestionsForIntent', methods=['GET'])
def getQuestionsForIntent():
    if request.method == 'GET':
        try:
            intent_id = request.args.get('intent_id')
            cursor = db_connection.cursor()
            query = f"SELECT * FROM questions WHERE intent_id = {intent_id}"
            cursor.execute(query)
            items = cursor.fetchall()
            json_array = [{'question_id': item[0], 'question': item[1]} for item in items]
            
            # Convert the list of dictionaries to a objects
            questions = json.dumps(json_array, ensure_ascii=False)

            cursor.close()

            return questions

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/getRulesForIntent', methods=['GET'])
def getRulesForIntent():
    if request.method == 'GET':
        try:
            intent_id = request.args.get('intent_id')
            cursor = db_connection.cursor()
            query = f"SELECT * FROM steps WHERE intent_id = {intent_id}"
            cursor.execute(query)

            items = cursor.fetchall()

            # Extract the JSON string from the database result
            json_array = items[0][3]

            cursor.close()

            # Return the JSON string as a JSON response
            return jsonify(json_array)

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/getThresholdsBySystemId', methods=['GET'])
def getThresholdsBySystemId():
    if request.method == 'GET':
        try:
            system_id = request.args.get('system_id')
            cursor = db_connection.cursor()
            query = f"SELECT * FROM thresholds WHERE system_id = {system_id}"
            cursor.execute(query)

            items = cursor.fetchall()
            json_array = [{'percentage_upper': item[2], 'percentage_lower': item[3]} for item in items]
            
            # Convert the list of dictionaries to a objects
            intents = json.dumps(json_array, indent=2, sort_keys=True, default=str) #fixing datetime bug on json parse

            cursor.close()

            return intents

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/updateThresholdsBySystemId', methods=['GET'])
def updateThresholdsBySystemId():
    if request.method == 'GET':
        try:
            system_id = request.args.get('system_id')
            percentage_upper = request.args.get('percentage_upper')
            percentage_lower = request.args.get('percentage_lower')
            cursor = db_connection.cursor()
            query = f"UPDATE thresholds SET percentage_upper = {percentage_upper}, percentage_lower = {percentage_lower} WHERE system_id = {system_id}"
            cursor.execute(query)

            db_connection.commit()

            cursor.close()

            # Return the JSON string as a JSON response
            return jsonify("Thresholds updated successfully!")

        except Exception as e:
            return jsonify(str(e))
        

@app.route('/postQuestion', methods=['POST'])
def postQuestion():
    if request.method == 'POST':
        try:
            data = request.json
            question = data.get("question")
            intent_id = data.get("intent_id")
            system_id = data.get("system_id")

            cursor = db_connection.cursor()
            
            # Use parameterized query to avoid SQL injection
            query = "INSERT INTO questions (question_id, question, intent_id, system_id) VALUES (DEFAULT, %s, %s, %s) RETURNING question_id;"
            cursor.execute(query, (question, intent_id, system_id))
            
            db_connection.commit()

            # Fetch the inserted question_id
            question_id = cursor.fetchone()[0]
        
            cursor.close()

            response = {
                "message": "Question added successfully!",
                "question_id": question_id
            }

            return jsonify(response)

        except Exception as e:
            return jsonify(str(e))

@app.route('/deleteQuestion', methods=['DELETE'])
def deleteQuestion():
    if request.method == 'DELETE':
        try:

            question_id = request.args.get('question_id')
            cursor = db_connection.cursor()
            query = f"DELETE FROM questions WHERE question_id = '{question_id}';"
            cursor.execute(query)
            db_connection.commit()
            cursor.close()

            return jsonify("Question deleted successfully!")

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/deleteQuestionsById', methods=['DELETE'])
def deleteQuestionsById():
    if request.method == 'DELETE':
        try:

            intent_id = request.args.get('intent_id')
            cursor = db_connection.cursor()
            query = f"DELETE FROM questions WHERE intent_id = '{intent_id}';"
            cursor.execute(query)
            db_connection.commit()
            cursor.close()

            return jsonify("Questions deleted successfully!")

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/addIntentForSystem', methods=['GET'])
def addIntentForSystem():
    if request.method == 'GET':
        try:
            system_id = request.args.get("system_id")
            cursor = db_connection.cursor()

            # Calculate the timestamp with a timezone offset of +2 hours
            current_datetime = (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')

            # Insert a new intent into the database
            query = f"INSERT INTO intents (intent_id, intent_name, last_edited, examples_count, steps_count, system_id) VALUES (DEFAULT, '', '{current_datetime}', 0, 1, {system_id}) RETURNING intent_id;"
            cursor.execute(query)
            intent_id = cursor.fetchone()[0]

            # Count the number of intents for the given system_id
            query = f"SELECT COUNT(*) FROM intents WHERE system_id = {system_id};"
            cursor.execute(query)
            count = cursor.fetchone()[0]

            # Update the intents_count in the systems table
            query = f"UPDATE systems SET intents_count = {count} WHERE system_id = {system_id};"
            cursor.execute(query)

            db_connection.commit()
            cursor.close()

            response = {
                "message": "Intent added successfully!",
                "intent_id": intent_id
            }

            return jsonify(response)

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/deleteIntent', methods=['DELETE'])
def deleteIntent():
    if request.method == 'DELETE':
        try:
            system_id = request.args.get("system_id")
            intent_id = request.args.get('intent_id')
            cursor = db_connection.cursor()
            # Delete intent from the database
            query = f"DELETE FROM intents WHERE intent_id = '{intent_id}';"
            cursor.execute(query)

            # Count the number of intents for the given system_id
            query = f"SELECT COUNT(*) FROM intents WHERE system_id = {system_id};"
            cursor.execute(query)
            count = cursor.fetchone()[0]

            # Update the intents_count in the systems table
            query = f"UPDATE systems SET intents_count = {count} WHERE system_id = {system_id};"
            cursor.execute(query)
            db_connection.commit()
            cursor.close()

            return jsonify("Intent deleted successfully!")

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/updateIntent', methods=['PUT'])
def updateIntent():
    if request.method == 'PUT':
        try:
            data = request.json
            intent_id = data.get("intent_id")
            new_intent = data.get("new_intent")

            cursor = db_connection.cursor()
            query = f"UPDATE intents SET intent_name = '{new_intent}' WHERE intent_id = {intent_id};"
            cursor.execute(query)
            db_connection.commit()
            cursor.close()

            return jsonify("Intent updated successfully!")

        except Exception as e:
            return jsonify(str(e))   

        
@app.route('/thumbsUp', methods=['GET'])
def thumbsUp():
    if request.method == 'GET':
        try:
            cursor = db_connection.cursor()
            uuid = request.args.get("uuid")
            intent_id = request.args.get("intent_id")
            system_id = request.args.get("system_id")

            current_datetime = (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
            # Find intent_name from id
            query = f"SELECT intent_name FROM intents WHERE intent_id = {intent_id}"
            cursor.execute(query)
            items = cursor.fetchall()
            query = f"INSERT INTO conversations (uuid, time, system_id, intent_id, text, thumbs_up, thumbs_down, threshold, conversation_id, intent_name) VALUES ('{uuid}', '{current_datetime}', {system_id}, {intent_id}, '', 1, 0, '', DEFAULT, '{items[0][0]}');"
            cursor.execute(query)
            db_connection.commit()
            cursor.close()
            
            return jsonify("Thumbs up counter updated successfully")

        except Exception as e:
            return jsonify({"error": str(e)})
        
@app.route('/thumbsDown', methods=['GET'])
def thumbsDown():
    if request.method == 'GET':
        try:
            cursor = db_connection.cursor()
            uuid = request.args.get("uuid")
            intent_id = request.args.get("intent_id")
            system_id = request.args.get("system_id")

            current_datetime = (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
            # Find intent_name from id
            query = f"SELECT intent_name FROM intents WHERE intent_id = {intent_id}"
            cursor.execute(query)
            items = cursor.fetchall()
            query = f"INSERT INTO conversations (uuid, time, system_id, intent_id, text, thumbs_up, thumbs_down, threshold, conversation_id, intent_name) VALUES ('{uuid}', '{current_datetime}', {system_id}, {intent_id}, '', 0, 1, '', DEFAULT, '{items[0][0]}');"
            cursor.execute(query)
            db_connection.commit()
            cursor.close()
            
            return jsonify("Thumbs down counter updated successfully")

        except Exception as e:
            return jsonify({"error": str(e)})
    

        
@app.route('/updateQuestion', methods=['PUT'])
def updateQuestion():
    if request.method == 'PUT':
        try:
            data = request.json
            question_id = data.get("question_id")
            new_question = data.get("new_question")

            cursor = db_connection.cursor()

            # Use parameterized query to avoid SQL injection
            query = "UPDATE questions SET question = %s WHERE question_id = %s;"
            cursor.execute(query, (new_question, question_id))
            
            db_connection.commit()
            cursor.close()

            return jsonify("Question updated successfully!")

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/addRuleForIntent', methods=['GET'])
def addRuleForIntent():
    if request.method == 'GET':
        try:
            intent_id = request.args.get('intent_id')
            step_dict = '[{"id":1,"conditions":{},"assistant_answer":"","customer_response":"","continuation":"Završetak radnje"}]'

            cursor = db_connection.cursor()
            query = "INSERT INTO steps (step_id, name_step, intent_id, step_dict) VALUES (DEFAULT, '1', %s, %s);"
            cursor.execute(query, (intent_id, step_dict))
            db_connection.commit()
            cursor.close()

            return jsonify("Step addeed successfully!")

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/updateStep', methods=['PUT'])
def updatestep():
    if request.method == 'PUT':
        try:
            data = request.json
            intent_id = data.get("intent_id")
            new_step = data.get("new_step")
            # Calculate the timestamp with a timezone offset of +2 hours
            current_datetime = (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')

            cursor = db_connection.cursor()

            # Use parameterized query to avoid SQL injection
            query_steps = "UPDATE steps SET step_dict = %s WHERE intent_id = %s;"
            cursor.execute(query_steps, (json.dumps(new_step), intent_id))

            query_intents = "UPDATE intents SET steps_count = %s, last_edited = %s WHERE intent_id = %s;"
            cursor.execute(query_intents, (len(new_step), current_datetime, intent_id))

            db_connection.commit()
            cursor.close()

            return jsonify("Step updated successfully!")

        except Exception as e:
            return jsonify(str(e))


@app.route('/deleteStep', methods=['DELETE'])
def deleteStep():
    if request.method == 'DELETE':
        try:

            intent_id = request.args.get('intent_id')
            cursor = db_connection.cursor()
            query = f"DELETE FROM steps WHERE intent_id = '{intent_id}';"
            cursor.execute(query)
            db_connection.commit()
            cursor.close()

            return jsonify("Step deleted successfully!")

        except Exception as e:
            return jsonify(str(e))

@app.route('/nextStep', methods=['POST'])
def nextStep():
    if request.method == 'POST':
        try:
            data = request.json
            response = data.get("response")
            conditions = data.get("conditions")
            cursor = db_connection.cursor()

            if conditions:
                query = f"SELECT * FROM steps WHERE intent_id = {response['intent_id']}"
                cursor.execute(query)
                items = cursor.fetchall()
                cursor.close()

                json_array = items[0][3]

                rule = find_matching_rule(json.loads(json_array), conditions, int(response['position']) + 1)
                return jsonify(rule)
            
            else:
                query = f"SELECT step_dict FROM steps WHERE intent_id = '{response['intent_id']}';"
                cursor.execute(query)
                item = cursor.fetchone()  # Use fetchone to get a single row
                cursor.close()

                if item:
                    response_data = json.loads(item[0])  # Access the first column from the tuple
                    result = response_data[int(response['position']) + 1]
                    result['position'] = int(response['position']) + 1
                    return jsonify(result)
                else:
                    return jsonify({"error": "No matching record found"})
                
        except Exception as e:
            return jsonify(str(e))


@app.route('/goToStep', methods=['GET'])  
def goToStep():
    if request.method == 'GET':
        try:
            intent_id = request.args.get('intent_id')
            id = request.args.get('id')
            cursor = db_connection.cursor()
            query = f"SELECT step_dict FROM steps WHERE intent_id = '{intent_id}';"
            cursor.execute(query)
            item = cursor.fetchone()  # Use fetchone to get a single row
            cursor.close()
            if item:
                response_data = json.loads(item[0])  # Access the first column from the tuple
                result = response_data[int(id) - 1]
                result['position'] = int(id) - 1
                return jsonify(result)
            else:
                return jsonify({"error": "No matching record found"})

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/getSynonyms', methods=['GET'])  
def getSynonyms():
    if request.method == 'GET':
        try:
            system_id = request.args.get('system_id')
            cursor = db_connection.cursor()
            query = f"SELECT * FROM synonyms WHERE system_id = '{system_id}';"
            cursor.execute(query)
            items = cursor.fetchall()
            json_array = [{'synonym_id': item[0], 'old_value': item[2], 'new_value': item[3]} for item in items]
            cursor.close()

            return jsonify(json_array)

        except Exception as e:
            return jsonify(str(e))


@app.route('/updateSynonyms', methods=['POST'])
def updateSynonyms():
    if request.method == 'POST':
        try:
            data = request.json
            systemID = data.get("system_id")
            synonyms = data.get("synonyms")

            cursor = db_connection.cursor()
            query = f"DELETE FROM synonyms WHERE system_id = '{systemID}'"
            cursor.execute(query)

            for key, values in synonyms.items():
                for value in values:
                    query = f"INSERT INTO synonyms (synonym_id, old_value, new_value, system_id) VALUES (DEFAULT, %s, %s, %s);"
                    cursor.execute(query, (value, key, systemID))
            db_connection.commit()
            cursor.close()

            return jsonify({"status": "success"})

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
        

@app.route('/sendMail', methods=['POST'])
def sendMail():
    if request.method == 'POST':
        try:
            data = request.json
            response = data.get("response")
            session_id = data.get("session_id")
            mail_data = data.get("data")
            conditions = data.get("conditions")
            systemID = data.get("systemID")

            if response:
                updateConversation(session_id, systemID, response['intent_id'], "KORISNIK ŠALJE MAIL: " + mail_data, '')

            # Set up the SMTP server
            smtp_server = '172.31.0.21'
            smtp_port = 25

            # Create the MIME object
            mail_options = response['mail_options']
            msg = MIMEMultipart()
            msg['From'] = 'MPU_projekt@pravosudje.hr'
            # Handle multiple recipients in 'To' field
            msg['To'] = ', '.join(mail_options.get('Prima', '').split(','))
            msg['Subject'] = mail_options['Naslov']
            msg['Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Check if 'Kopija' field is present and handle multiple recipients
            if 'Kopija' in mail_options:
                msg['Copy'] = ','.join(mail_options['Kopija'].split(','))
            
            mail_options_start = mail_options['Početak maila']
            mail_data_text = mail_data
            mail_options_end = mail_options['Kraj maila']
            # Concatenate the parts with line breaks
            email_body = f"{mail_options_start}\n{mail_data_text}\n{mail_options_end}"
            # Attach the email body
            msg.attach(MIMEText(email_body, 'plain'))


            # Add attachment if provided
            cursor = db_connection.cursor()
            if mail_options['Privitak']:
                query = f"SELECT text FROM conversations WHERE uuid = '{session_id}'"
                cursor.execute(query)
                items = cursor.fetchall()

                # Extract the values from the result set
                column_values = [item[0] for item in items]  # Adjust the index based on your database structure

                # Concatenate the values into a single string with HTML line breaks
                concatenated_text = "<br>".join(column_values)

                # Save the concatenated text to an HTML file
                attachment_filename = "attachment.html"
                with open(attachment_filename, "w", encoding="utf-8") as attachment_file:
                    attachment_file.write(concatenated_text)

                # Attach the file to the email
                with open(attachment_filename, "rb") as attachment:
                    part = MIMEApplication(attachment.read(), Name=attachment_filename)
                part['Content-Disposition'] = f'attachment; filename="{attachment_filename}"'
                msg.attach(part)
            
            # Connect to the SMTP server using SSL/TLS
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                # Combine 'To' and 'Copy' recipients
                recipients = [msg['To']]
                if 'Copy' in msg:
                    recipients += [msg['Copy']]
                # Send the email to both 'To' and 'Copy' recipients
                server.sendmail(msg['From'], recipients, msg.as_string())


            query = f"SELECT * FROM steps WHERE intent_id = {response['intent_id']}"
            cursor.execute(query)
            items = cursor.fetchall()
            cursor.close()

            json_array = items[0][3]

            rule = find_matching_rule(json.loads(json_array), conditions, int(response['position']) + 1)
            return jsonify(rule)

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})



#sending questions do machine learning   
@app.route('/sendQuestions', methods=['GET'])
def sendQuestions():
    if request.method == 'GET':
        try:
            intent_id = request.args.get('intent_id')
            system_id = request.args.get('system_id')
            questions_len = request.args.get('questions')
            # Calculate the timestamp with a timezone offset of +2 hours
            current_datetime = (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')

            cursor = db_connection.cursor()

            query_intents = f"UPDATE intents SET examples_count = '{questions_len}', last_edited = '{current_datetime}' WHERE intent_id = {intent_id};"
            cursor.execute(query_intents)

            query = f"SELECT * FROM questions WHERE system_id = '{system_id}'"
            cursor.execute(query)
            items = cursor.fetchall()
            json_array = [{'question': item[1], 'intent_id': item[2]} for item in items]

            # Initialize a dictionary to store the transformed data
            transformed_data = {}

            # Iterate over each item in the database data
            for item in json_array:
                intent_id = str(item["intent_id"])
                question_text = item["question"]

                # If the intent_id is not in the dictionary, add it
                if intent_id not in transformed_data:
                    transformed_data[intent_id] = {
                        "IntentID": intent_id,
                        "SystemID": system_id,
                        "Questions": []
                    }

                # Append the question text to the Questions list
                transformed_data[intent_id]["Questions"].append({
                    "QuestionText": question_text
                })

            # Convert the values of the dictionary to a list
            transformed_data_list = list(transformed_data.values())

            db_connection.commit()
            cursor.close()

            json_data = json.dumps(transformed_data_list)

            response_from_other_backend = send_data_to_machine_learning(json_data, 'train')
            return jsonify(response_from_other_backend)

        except Exception as e:
            return jsonify(str(e))

#reloading questions from machine learning   
@app.route('/reloadQuestions', methods=['GET'])
def reloadQuestions():
    if request.method == 'GET':
        try:
            system_id = request.args.get('system_id')

            cursor = db_connection.cursor()
            query = f"SELECT * FROM questions WHERE system_id = '{system_id}'"
            cursor.execute(query)
            items = cursor.fetchall()
            json_array = [{'question': item[1], 'intent_id': item[2]} for item in items]

            # Initialize a dictionary to store the transformed data
            transformed_data = {}

            # Iterate over each item in the database data
            for item in json_array:
                intent_id = str(item["intent_id"])
                question_text = item["question"]

                # If the intent_id is not in the dictionary, add it
                if intent_id not in transformed_data:
                    transformed_data[intent_id] = {
                        "IntentID": intent_id,
                        "SystemID": system_id,
                        "Questions": []
                    }

                # Append the question text to the Questions list
                transformed_data[intent_id]["Questions"].append({
                    "QuestionText": question_text
                })

            # Convert the values of the dictionary to a list
            transformed_data_list = list(transformed_data.values())

            db_connection.commit()
            cursor.close()

            json_data = json.dumps(transformed_data_list)
            response_from_other_backend = send_data_to_machine_learning(json_data, 'train')
            return jsonify(response_from_other_backend)

        except Exception as e:
            return jsonify(str(e))

        
def send_data_to_machine_learning(data, type):
    # Define the URL of the other backend API
    other_backend_url = 'http://18.158.244.150:7000/chatbot/' + type

     # Make a POST request with JSON data
    headers = {'Content-Type': 'application/json'}  # Set the content type to JSON
    response = requests.post(other_backend_url, data=data, headers=headers)

    # Check the response status code and handle accordingly
    if response.status_code == 200:
        return response.json()  # Assuming the response is JSON
    else:
        # Handle error cases
        return {'error': 'Failed to retrieve data from the other backend'}
    
@app.route('/updateConversationTmp', methods=['POST'])
def updateConversationTmp():
    if request.method == 'POST':
        try:
            data = request.json
            uuid = data.get("uuid")
            systemID = data.get("system_id")
            intent_id = data.get("intent_id")
            question = data.get("question")
            threshold = data.get("threshold")
            response = data.get("response")

            updateConversation(uuid, systemID, intent_id, "KORISNIK: " + question, threshold)
            updateConversation(uuid, systemID, intent_id, "CHATBOT: " + response['assistant_answer'], '')

            return jsonify({"status": "success"})

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    

def updateConversation(uuid, systemID, intent_id, text, threshold):
    # Calculate the timestamp with a timezone offset of +2 hours
    current_datetime = (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')

    cursor = db_connection.cursor()

    # Find intent_name from id only if intent_id is not -1
    if intent_id != -1:
        query = f"SELECT intent_name FROM intents WHERE intent_id = {intent_id}"
        cursor.execute(query)
        items = cursor.fetchall()
        intent_name = items[0][0]
    else:
        # If intent_id is -1, set intent_name to 'nedefinirano'
        intent_name = 'nedefinirano'

    # Insert a new intent into the database using parameterized query
    query = "INSERT INTO conversations (uuid, time, system_id, intent_id, text, threshold, thumbs_up, thumbs_down, conversation_id, intent_name) VALUES (%s, %s, %s, %s, %s, %s, 0, 0, DEFAULT, %s);"
    values = (uuid, current_datetime, systemID, intent_id, text, threshold, intent_name)
    cursor.execute(query, values)
    db_connection.commit()
    cursor.close()

@app.route('/chatbotSentMessage', methods=['POST'])
def chatbotSentMessage():
    if request.method == 'POST':
        try:
            data = request.json
            systemID = data.get("systemID")
            question = data.get("question").capitalize()    #first letter uppercase
            uuid = data.get("uuid")

            # Open a cursor
            cursor = db_connection.cursor()

            # Replace synonyms in the question
            replaced_question = replace_synonyms(question, cursor, systemID)

            transformed_question = {
                "SessionID": uuid,
                "SystemID": systemID,
                "QuestionText": replaced_question
            }
            json_question = json.dumps(transformed_question)

            query = f"SELECT percentage_upper, percentage_lower FROM thresholds WHERE system_id = {systemID}"
            cursor.execute(query)
            thresholds = cursor.fetchall()[0]
            response_from_other_backend = send_data_to_machine_learning(json_question, 'query')
            if response_from_other_backend['PredictedIntent']['Confidence'] < (thresholds[0]/100) and  response_from_other_backend['PredictedIntent']['Confidence'] > (thresholds[1]/100):
                result = []  # Store intent objects with both name and id
                predicted_intents = send_data_to_machine_learning(json_question, 'query/8')
                for predicted_intent in predicted_intents:
                    intent_id = predicted_intent['PredictedIntent']['IntentID']
                    query = f"SELECT intent_name FROM intents WHERE intent_id = {intent_id}"
                    cursor.execute(query)
                    intent_name = cursor.fetchall()

                    confidence = predicted_intent['PredictedIntent'].get('Confidence', 0.0)

                    intent_object = {
                        'intent_name': intent_name[0][0],
                        'intent_id': intent_id,
                        'question': question,
                        'threshold': confidence,
                    }
                    result.append(intent_object)

            elif response_from_other_backend['PredictedIntent']['Confidence'] >= (thresholds[0]/100):
                predicted_intents = send_data_to_machine_learning(json_question, 'query/8')
                first_object = predicted_intents[0]

                # Filter objects with the same Confidence as the first object
                filtered_objects = [obj for obj in predicted_intents if obj['PredictedIntent']['Confidence'] == first_object['PredictedIntent']['Confidence']]

                if len(filtered_objects) > 1:
                    # Check if there are more than one object with different IntentID
                    intent_ids = set(obj['PredictedIntent']['IntentID'] for obj in filtered_objects)

                    if len(intent_ids) > 1:
                        result = []  # Store intent objects with both name and id
                        for predicted_intent in filtered_objects:
                            intent_id = predicted_intent['PredictedIntent']['IntentID']
                            query = f"SELECT intent_name FROM intents WHERE intent_id = {intent_id}"
                            cursor.execute(query)
                            intent_name = cursor.fetchall()

                            confidence = predicted_intent['PredictedIntent'].get('Confidence', 0.0)

                            intent_object = {
                                'intent_name': intent_name[0][0],
                                'intent_id': intent_id,
                                'question': question,
                                'threshold': confidence,
                            }
                            result.append(intent_object)
                    # Else return that one different IntentID
                    else:
                        intent_id = response_from_other_backend['PredictedIntent']['IntentID']
                        cursor = db_connection.cursor()
                        query = f"SELECT * FROM steps WHERE intent_id = {intent_id}"
                        cursor.execute(query)

                        items = cursor.fetchall()

                        # Extract the JSON string from the database result
                        json_array = items[0][3]
                        result = json.loads(json_array)[0]
                        result['intent_id'] = intent_id
                        result['position'] = 0
                        updateConversation(uuid, systemID, intent_id, "KORISNIK: " + question, response_from_other_backend['PredictedIntent']['Confidence'])
                        updateConversation(uuid, systemID, intent_id, "CHATBOT: " + result['assistant_answer'], '')
            
            else:
                updateConversation(uuid, systemID, -1, "KORISNIK: " + question, response_from_other_backend['PredictedIntent']['Confidence'])
                result = "Možda mogu ponuditi bolji odgovor ako preformulirate Vaše pitanje."
            cursor.close()

            # Return the JSON string as a JSON response
            return jsonify(result)

        except Exception:
            return jsonify("Sustav je trenutno u procesu učenja. Molim Vas pokušajte ponovno kasnije.")
        

def replace_synonyms(question, cursor, system_id):
    # Fetch all synonyms from the database
    cursor.execute("SELECT old_value, new_value FROM synonyms WHERE system_id = %s", system_id)
    synonym_pairs = cursor.fetchall()

    # If synonym_pairs is empty, return the original question
    if not synonym_pairs:
        return question

    # Create a dictionary for quick lookup
    synonyms_dict = {old: new for old, new in synonym_pairs}

    # Replace old values with new values in the question
    replaced_question = re.sub(r'\b(' + '|'.join(re.escape(key) for key in synonyms_dict.keys()) + r')\b',
                               lambda x: synonyms_dict[x.group()], question, flags=re.IGNORECASE)

    return replaced_question



@app.route('/chatbotUserResponse', methods=['POST'])
def chatbotUserResponse():
    if request.method == 'POST':
        try:
            data = request.json
            conditions = data.get("conditions")
            intentID = data.get("intent_id")
            id = data.get("id")
            uuid = data.get("uuid")
            systemID = data.get("systemID")
            answer = data.get("answer")

            updateConversation(uuid, systemID, intentID, "KORISNIK: " + answer, '')

            cursor = db_connection.cursor()
            query = f"SELECT * FROM steps WHERE intent_id = {intentID}"
            cursor.execute(query)
            items = cursor.fetchall()
            cursor.close()

            json_array = items[0][3]

            rule = find_matching_rule(json.loads(json_array), conditions, int(id) + 1)
            updateConversation(uuid, systemID, intentID, "CHATBOT: " + rule['assistant_answer'], '')

            return jsonify(rule)

        except Exception as e:
            return jsonify(str(e))
        

def find_matching_rule(rules, conditions, id):
    for index in range(id, len(rules)):
        # Check if the "conditions" key is empty
        if not rules[index].get("conditions", {}).get("conditionsList"):
            rules[index]['position'] = index
            return rules[index]

        # Check if all conditions must be true or only one condition must be true
        if rules[index].get("conditions", {}).get("allConditionsMustBeTrue", False):
            # Check if all conditions in conditionsList match any condition in the list
            conditions_list = rules[index].get("conditions", {}).get("conditionsList", [])
            if all(
                any(
                    (
                        c.get("answer").replace("&nbsp;", "\xa0") == condition.get("subject")
                        and c.get("predicate") == condition.get("predicate")
                        and c.get("object") == condition.get("object")
                    )
                    for condition in conditions
                )
                for c in conditions_list
            ):
                rules[index]['position'] = index
                return rules[index]
        else:
            # Check if at least one condition in conditionsList matches any condition in the list
            conditions_list = rules[index].get("conditions", {}).get("conditionsList", [])
            if any(
                any(
                    (
                        c.get("answer").replace("&nbsp;", "\xa0") == condition.get("subject")
                        and c.get("predicate") == condition.get("predicate")
                        and c.get("object") == condition.get("object")
                    )
                    for condition in conditions
                )
                for c in conditions_list
            ):
                rules[index]['position'] = index
                return rules[index]
    return None  # No matching rule found




'''
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get the uploaded file
        file = request.files['file']
        
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file)

        cursor = db_connection.cursor()

        # Iterate through rows and insert data into the database
        print(df.iterrows())
        for index, row in df.iterrows():
            value1 = row['question']
            value2 = row['intent_id']
            value3 = row['system_id']

            # Adjust the SQL query based on your table structure
            cursor.execute("INSERT INTO questions (question_id, question, intent_id, system_id) VALUES (DEFAULT, %s, %s, %s);", (value1, value2, value3))

        # Commit the transaction
        db_connection.commit()

        # Close the cursor and db_connection
        cursor.close()
        db_connection.close()

        return jsonify({"message": "Data inserted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})

'''


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)