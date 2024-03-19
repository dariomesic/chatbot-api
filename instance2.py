from flask import Flask, request, jsonify
import re
from datetime import datetime, timedelta, timezone
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
    dbname="chatbot",
    user="moj_chatbot",
    password="61-eofP9dj0#",
    host="172.20.67.195"
)

# Latest table dates
chosen_table_dates = []

def get_chosen_table_dates():
    global chosen_table_dates
    chosen_table_dates = []
    cursor = db_connection.cursor()

    try:
        # Iterate over the fixed system IDs (1, 2, 3, 4)
        for system_id in [1, 2, 3, 4, 5]:
            # Write a query to get the latest table for the specific system
            query = f"""
                SELECT default_version from versions where system_id = {system_id}
            """
            cursor.execute(query)

            # Fetch the result
            result = cursor.fetchone()

            if result:
                # Extract the date from the table name
                chosen_table_dates.append(result[0])
        cursor.close()

    except Exception as e:
            return jsonify(str(e))  

# Call the function to get the latest table dates for each system
get_chosen_table_dates()

@app.route('/')
def hello():
    return 'Hello, Flask!'
        
                        
@app.route('/getRulesForIntent', methods=['GET'])
def getRulesForIntent():
    if request.method == 'GET':
        try:
            intent_id = request.args.get('intent_id')
            system_id = request.args.get('system_id')
            cursor = db_connection.cursor()
            query = f"SELECT * FROM steps_{system_id}_{chosen_table_dates[int(system_id) - 1]} WHERE intent_id = {intent_id}"
            cursor.execute(query)

            items = cursor.fetchall()

            # Extract the JSON string from the database result
            json_array = items[0][3]

            cursor.close()

            # Return the JSON string as a JSON response
            return jsonify(json_array)

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
            query = f"SELECT intent_name FROM intents_{system_id}_{chosen_table_dates[int(system_id) - 1]} WHERE intent_id = {intent_id}"
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
            query = f"SELECT intent_name FROM intents_{system_id}_{chosen_table_dates[int(system_id) - 1]} WHERE intent_id = {intent_id}"
            cursor.execute(query)
            items = cursor.fetchall()
            query = f"INSERT INTO conversations (uuid, time, system_id, intent_id, text, thumbs_up, thumbs_down, threshold, conversation_id, intent_name) VALUES ('{uuid}', '{current_datetime}', {system_id}, {intent_id}, '', 0, 1, '', DEFAULT, '{items[0][0]}');"
            cursor.execute(query)
            db_connection.commit()
            cursor.close()
            
            return jsonify("Thumbs down counter updated successfully")

        except Exception as e:
            return jsonify({"error": str(e)})
    
                
@app.route('/nextStep', methods=['POST'])
def nextStep():
    if request.method == 'POST':
        try:
            data = request.json
            response = data.get("response")
            conditions = data.get("conditions")
            system_id = request.args.get("system_id")
            cursor = db_connection.cursor()

            if conditions:
                query = f"SELECT * FROM steps_{system_id}_{chosen_table_dates[int(system_id) - 1]} WHERE intent_id = {response['intent_id']}"
                cursor.execute(query)
                items = cursor.fetchall()
                cursor.close()

                json_array = items[0][3]

                rule = find_matching_rule(json.loads(json_array), conditions, int(response['position']) + 1)
                return jsonify(rule)
            
            else:
                query = f"SELECT step_dict FROM steps_{system_id}_{chosen_table_dates[int(system_id) - 1]} WHERE intent_id = '{response['intent_id']}';"
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
            system_id = request.args.get("system_id")
            id = request.args.get('id')
            cursor = db_connection.cursor()
            query = f"SELECT step_dict FROM steps_{system_id}_{chosen_table_dates[int(system_id) - 1]} WHERE intent_id = '{intent_id}';"
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
        
@app.route('/getInitialChat', methods=['GET'])  
def getInitialChat():
    if request.method == 'GET':
        try:
            system_id = request.args.get('system_id')
            cursor = db_connection.cursor()
            query = f"SELECT * FROM initials_{system_id}_{chosen_table_dates[int(system_id) - 1]};"
            cursor.execute(query)
            items = cursor.fetchall()
            json_array = [{'system_initial': item[2], 'system_name': item[3]} for item in items]
            cursor.close()

            return jsonify(json_array)

        except Exception as e:
            return jsonify(str(e))
        
@app.route('/getThemes', methods=['GET'])  
def getThemes():
    if request.method == 'GET':
        try:
            system_id = request.args.get('system_id')
            cursor = db_connection.cursor()
            query = f"SELECT * FROM themes_{system_id}_{chosen_table_dates[int(system_id) - 1]}"
            cursor.execute(query)
            items = cursor.fetchall()
            json_array = [{'intents': item[1]} for item in items]
            cursor.close()

            return jsonify(json_array)

        except Exception as e:
            return jsonify(str(e))


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
                updateConversation(session_id, systemID, response['intent_id'], "KORISNIK ŠALJE MAIL: " + mail_data, '', 0)

            # Set up the SMTP server
            smtp_server = '10.1.193.99'
            smtp_port = 25

            # Create the MIME object
            mail_options = response['mail_options']
            msg = MIMEMultipart()
            msg['From'] = 'MPU_projekt@pravosudje.hr <no-reply@pravosudje.hr>'
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


            query = f"SELECT * FROM steps_{systemID}_{chosen_table_dates[int(systemID)- 1]} WHERE intent_id = {response['intent_id']}"
            cursor.execute(query)
            items = cursor.fetchall()
            cursor.close()

            json_array = items[0][3]

            rule = find_matching_rule(json.loads(json_array), conditions, int(response['position']) + 1)
            return jsonify(rule)

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
        

@app.route('/searchDocuments', methods=['POST'])
def searchDocuments():
    if request.method == 'POST':
        try:
            data = request.json
            text = data.get("text")
            systemID = data.get("systemID")

            transformed_question = {
                "QuestionText": text,
                "SystemID": systemID
            }
            json_question = json.dumps(transformed_question)

            response_backend = requests.post('http://172.20.67.124:9876/search/query', data=json_question, headers={'Content-Type': 'application/json'})

            # Check the response_backend status code and handle accordingly
            if response_backend.status_code == 200:
                response = response_backend.json()
                cursor = db_connection.cursor()

                query = f"SELECT title from documents WHERE id_doc = {response['SearchResult']['AnswerTexts'][0]['DocumentID']};"
                cursor.execute(query)
                items = cursor.fetchall()
                name = items[0][0]

                query_threshold = f"SELECT percentage_document from thresholds WHERE system_id = {systemID}"
                cursor.execute(query_threshold)
                items = cursor.fetchall()
                threshold = items[0][0]

                document = {
                    'text': response['SearchResult']['AnswerTexts'][0]['Text'],
                    'document_title': name,
                    'document_page': response['SearchResult']['AnswerTexts'][0]['Page'],
                    'score': response['SearchResult']['AnswerTexts'][0]['Score'],
                    'threshold': threshold
                }
                return jsonify(document)
            
            else:
                # Handle error cases
                return {'error': 'Failed to retrieve data from the other backend'}


        except Exception as e:
            return jsonify(str(e))

    
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

            updateConversation(uuid, systemID, intent_id, "KORISNIK: " + question, threshold, 0)
            updateConversation(uuid, systemID, intent_id, "CHATBOT: " + response['assistant_answer'], '', 1)

            return jsonify({"status": "success"})

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    

def updateConversation(uuid, systemID, intent_id, text, threshold, delay):
    # Calculate the timestamp with a timezone offset of +2 hours
    current_datetime = (datetime.utcnow() + timedelta(hours=2, seconds = delay)).strftime('%Y-%m-%d %H:%M:%S')

    cursor = db_connection.cursor()
    # Find intent_name from id only if intent_id is not -1 or -2
    if intent_id != -1 and intent_id != -2:
        query = f"SELECT intent_name FROM intents WHERE intent_id = {intent_id}"
        cursor.execute(query)
        items = cursor.fetchall()
        intent_name = items[0][0]
    elif intent_id == -1:
    	# If intent_id is -1, set intent_name to 'nedefinirano
        intent_name = 'nedefinirano'
    else:
        intent_name = 'baza znanja'
    # Insert a new intent into the database using parameterized query
    query = "INSERT INTO conversations (uuid, time, system_id, intent_id, text, threshold, thumbs_up, thumbs_down, conversation_id, intent_name) VALUES (%s, %s, %s, %s, %s, %s, 0, 0, DEFAULT, %s);"
    values = (uuid, current_datetime, systemID, intent_id, text, threshold, intent_name)
    cursor.execute(query, values)
    db_connection.commit()
    cursor.close()




@app.route('/checkForPreviousVersion', methods=['GET'])  
def checkForPreviousVersion():
    if request.method == 'GET':
        systemID = request.args.get('system_id')
        try:
            cursor = db_connection.cursor()
            query = f"SELECT previous_version from versions WHERE system_id = {systemID}"
            cursor.execute(query)
            previous_version = cursor.fetchone()

            return jsonify({"previous_version": previous_version})
            cursor.close()


        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

@app.route('/versioningBySystemId', methods=['GET'])  
def versioningBySystemId():
    if request.method == 'GET':
        systemID = request.args.get('system_id')
        try:
            cursor = db_connection.cursor()
            # Format the time in the desired format
            formatted_time = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=1))).strftime('%Y_%m_%dt%H_%M_%S_%f')[:-3] + 'Z'

            existing_tables = ['intents', 'questions', 'steps', 'synonyms', 'thresholds', 'initials', 'pages', 'themes']
            new_tables = ['intents_' + str(systemID) + "_" + formatted_time, 'questions_' + str(systemID) + "_" + formatted_time, 'steps_' + str(systemID) + "_" + formatted_time, 'synonyms_' + str(systemID) + "_" + formatted_time, 'thresholds_' + str(systemID) + "_" + formatted_time, 'initials_' + str(systemID) + "_" + formatted_time, 'pages_' + str(systemID) + "_" + formatted_time, 'themes_' + str(systemID) + "_" + formatted_time]

            for existing_table, new_table in zip(existing_tables, new_tables):
                # Step 1: Create a new table with the same structure as the existing table
                create_table_query = f"""
                    CREATE TABLE {new_table} AS
                    SELECT * FROM {existing_table} WHERE 1 = 0;
                """
                cursor.execute(create_table_query)

                # Step 2: Copy data from the existing table to the new table using COPY
                copy_data_query = f"""
                    INSERT INTO {new_table}
                    SELECT * FROM {existing_table}
                """
                # Conditionally add WHERE clause for system_id except for 'steps' table
                if existing_table != 'steps':
                    copy_data_query += f" WHERE system_id = {str(systemID)}"
                print(copy_data_query)
                cursor.execute(copy_data_query)


            # Stanje na admin
            cursor.execute(f"SELECT * FROM questions WHERE system_id = {systemID}")
            current_state = cursor.fetchall()

            # Get the previous state from the database
            cursor.execute(f"SELECT * FROM questions_{systemID}_{chosen_table_dates[int(systemID) - 1]}")
            previous_state = cursor.fetchall()
            # Find differences and learn on them
            transformed_data = get_diff(systemID, list(previous_state), list(current_state))

            json_data = json.dumps(transformed_data)
            print(json_data)
            # Define the URL of the other backend API
            first_backend_url = 'http://172.20.67.22:9876/chatbot/train'
            second_backend_url = 'http://172.20.67.23:9876/chatbot/train'
            
            # Make a POST request with JSON data
            headers = {'Content-Type': 'application/json'}  # Set the content type to JSON
            response_first = requests.post(first_backend_url, data=json_data, headers=headers)
            response_second = requests.post(second_backend_url, data=json_data, headers=headers)

            # Send document learning for systemID IF PAGES ARE NOT EMPTY!!!
            # Fetch number of documents from pages
            query_num = f"SELECT COUNT(*) FROM pages WHERE system_id = {systemID}"
            cursor.execute(query_num)
            count = cursor.fetchone()[0]
            if count > 0:
                parameters = {
                    "SystemID": str(systemID)
                }
                json_parameter = json.dumps(parameters)

                requests.post('http://172.20.67.22:9877/search/train', data=json_parameter, headers={'Content-Type': 'application/json'})
                requests.post('http://172.20.67.23:9877/search/train', data=json_parameter, headers={'Content-Type': 'application/json'})

            # Updating versions table
            versions_query = f"SELECT default_version from versions WHERE system_id = {systemID}"
            cursor.execute(versions_query)
            default_version = cursor.fetchone()[0]
            insert_versions_query = f"UPDATE versions SET previous_version= '{default_version}', default_version = '{formatted_time}' WHERE system_id = {systemID};"
            cursor.execute(insert_versions_query)
            print(default_version, formatted_time)

            db_connection.commit()
            cursor.close()

            get_chosen_table_dates()
            
            # Check the response status code and handle accordingly
            if response_first.status_code == 200 and response_second.status_code == 200:
                return {'success': 'Uspješno spremljene promjene u sustav!'}
            else:
                # Handle error cases
                return {'error': 'Sustav je trenutno već u procesu učenja. Molim Vas pokušajte ponovno'}
        except Exception:
            return {'error': 'Sustav je trenutno već u procesu učenja. Molim Vas pokušajte ponovno'}
        
@app.route('/goToPreviousVersion', methods=['GET'])  
def goToPreviousVersion():
    if request.method == 'GET':
        systemID = request.args.get('system_id')
        try:
            cursor = db_connection.cursor()

            # Updating previous version with null and default with previous
            versions_query = f"SELECT previous_version, default_version from versions WHERE system_id = {systemID}"
            cursor.execute(versions_query)
            items = cursor.fetchone()
            previous_version, default_version = items


            # State which is being replaced
            cursor.execute(f"SELECT * FROM questions_{systemID}_{default_version}")
            previous_state = cursor.fetchall()

            # New state
            cursor.execute(f"SELECT * FROM questions_{systemID}_{previous_version}")
            new_state = cursor.fetchall()

            transformed_data = get_diff(systemID, list(previous_state), list(new_state))

            json_data = json.dumps(transformed_data)
            print(json_data)
            # Define the URL of the other backend API
            first_backend_url = 'http://172.20.67.22:9876/chatbot/train'
            second_backend_url = 'http://172.20.67.23:9876/chatbot/train'

            # Make a POST request with JSON data
            headers = {'Content-Type': 'application/json'}  # Set the content type to JSON
            response_first = requests.post(first_backend_url, data=json_data, headers=headers)
            response_second = requests.post(second_backend_url, data=json_data, headers=headers)

            # Send document learning for systemID IF PAGES ARE NOT EMPTY!!!
            # Fetch number of documents from pages
            query_num = f"SELECT COUNT(*) FROM pages WHERE system_id = {systemID}"
            cursor.execute(query_num)
            count = cursor.fetchone()[0]
            
            if count > 0:
                parameters = {
                    "SystemID": str(systemID)
                }
                json_parameter = json.dumps(parameters)

                requests.post('http://172.20.67.22:9877/search/train', data=json_parameter, headers={'Content-Type': 'application/json'})
                requests.post('http://172.20.67.23:9877/search/train', data=json_parameter, headers={'Content-Type': 'application/json'})

            update_default_version = f"UPDATE versions SET previous_version = '{''}', default_version = '{previous_version}' WHERE system_id = {systemID};"
            cursor.execute(update_default_version)

            db_connection.commit()
            cursor.close()

            get_chosen_table_dates()          

            # Check the response status code and handle accordingly
            if response_first.status_code == 200 and response_second.status_code == 200:
                return {'success': 'Uspješno spremljene promjene u sustav!'}
            else:
                # Handle error cases
                return {'error': 'Sustav je trenutno već u procesu učenja. Molim Vas pokušajte ponovno'}

        except Exception:
            return {'error': 'Sustav je trenutno već u procesu učenja. Molim Vas pokušajte ponovno'}



def get_diff(system_id, previous_state, new_state):
    try:
        # Create a JSON object with differences
        diff_json = {
            'SystemID': str(system_id),
            'added_items': [],
            'deleted_items': [],
            'edited_items': []
        }

       # Identify added items
        added_items = [
            {
                'IntentID': item[0],
                'QuestionID': item[1],
                'QuestionText': item[2]
            }
            for item in new_state
            if item[0] not in [prev[0] for prev in previous_state]
        ]
        diff_json['added_items'] = added_items
        # Identify deleted items
        deleted_items = [
            {
                'IntentID': item[0],
                'QuestionID': item[1],
                'QuestionText': item[2]
            }
            for item in previous_state
            if item[0] not in [prev[0] for prev in new_state]
        ]
        diff_json['deleted_items'] = deleted_items
        # Identify edited items
        edited_items = [
            {
                'IntentID': curr[0],
                'QuestionID': curr[1],
                'QuestionText': curr[2]
            }
            for curr in new_state
            if any(curr[0] == prev[0] and curr[1] != prev[1] for prev in previous_state)
        ]
        diff_json['edited_items'] = edited_items
        return diff_json

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/chatbotSentMessage', methods=['POST'])
def chatbotSentMessage():
    if request.method == 'POST':
        try:
            data = request.json
            systemID = data.get("systemID")
            question = data.get("question").capitalize()  # First letter uppercase
            uuid = data.get("uuid")

            cursor = db_connection.cursor()
            
            # Replace synonyms in the question
            replaced_question = replace_synonyms(question, cursor, systemID)

            transformed_question = {
                "SessionID": uuid,
                "SystemID": systemID,
                "QuestionText": replaced_question
            }
            json_question = json.dumps(transformed_question)

            query = f"SELECT percentage_upper, percentage_lower FROM thresholds_{systemID}_{chosen_table_dates[int(systemID) - 1]}"
            cursor.execute(query)
            thresholds = cursor.fetchone()

            upper_threshold, lower_threshold = thresholds

            # Fetch number of documents from pages
            query = f"SELECT COUNT(*) FROM pages_{systemID}_{chosen_table_dates[int(systemID) - 1]}"
            cursor.execute(query)
            count = cursor.fetchone()[0]

            response_from_other_backend = send_data_to_machine_learning(json_question, 'query')
            
            if lower_threshold / 100 <= response_from_other_backend['PredictedIntent']['Confidence'] < upper_threshold / 100:
                result = process_predicted_intents(send_data_to_machine_learning(json_question, 'query/6'), cursor, question, systemID)
                if count > 0:
                    result.append({'intent_name': 'PRETRAŽI BAZU ZNANJA', 'intent_id': -2, 'question': question, 'threshold': response_from_other_backend['PredictedIntent']['Confidence']})
            
            elif response_from_other_backend['PredictedIntent']['Confidence'] >= upper_threshold / 100:
                predicted_intents = send_data_to_machine_learning(json_question, 'query/6')
                first_object = predicted_intents[0]
                
                # Filter objects with the same Confidence as the first object
                filtered_objects = [obj for obj in predicted_intents if obj['PredictedIntent']['Confidence'] == first_object['PredictedIntent']['Confidence']]
                
                if len(filtered_objects) > 1:
                    result = process_predicted_intents(filtered_objects, cursor, question, systemID)
                
                # Else return that one different IntentID
                elif len(filtered_objects) == 1:
                    intent_id = response_from_other_backend['PredictedIntent']['IntentID']
                    query = f"SELECT * FROM steps_{systemID}_{chosen_table_dates[int(systemID)- 1]} WHERE intent_id = {intent_id}"
                    cursor.execute(query)
                    
                    items = cursor.fetchall()
                    
                    # Extract the JSON string from the database result
                    json_array = items[0][3]
                    result = json.loads(json_array)[0]
                    result['intent_id'] = intent_id
                    result['position'] = 0
                    updateConversation(uuid, systemID, intent_id, "KORISNIK: " + question, response_from_other_backend['PredictedIntent']['Confidence'], 0)
                    updateConversation(uuid, systemID, intent_id, "CHATBOT: " + result['assistant_answer'], '', 1)
            
            else:
                result = process_predicted_intents(send_data_to_machine_learning(json_question, 'query/6'), cursor, question, systemID)
                if count > 0:
                    result.append({'intent_name': 'PRETRAŽI BAZU ZNANJA', 'intent_id': -2, 'question': question, 'threshold': response_from_other_backend['PredictedIntent']['Confidence']})
                result.append({'intent_name': 'PREFORMULIRAT ĆU PITANJE', 'intent_id': -1, 'question': question, 'threshold': response_from_other_backend['PredictedIntent']['Confidence']})

            # Return the JSON string as a JSON response
            return jsonify(result)

        except Exception:
            return jsonify("Sustav je trenutno u procesu učenja. Molim Vas pokušajte ponovno kasnije.")

def process_predicted_intents(predicted_intents, cursor, question, systemID):
    result = []
    greetings = ['Dobar dan', 'Dobar dan, kako si', 'Bok', 'Doviđenja']
    for predicted_intent in predicted_intents:
        intent_id = predicted_intent['PredictedIntent']['IntentID']
        query = f"SELECT intent_name FROM intents_{systemID}_{chosen_table_dates[int(systemID)- 1]} WHERE intent_id = {intent_id}"
        cursor.execute(query)
        intent_name = cursor.fetchall()
        intent_name_str = intent_name[0][0]

        confidence = predicted_intent['PredictedIntent'].get('Confidence', 0.0)

        # Check if intent_name is in greetings list
        if intent_name_str not in greetings:
            intent_object = {
                'intent_name': intent_name_str,
                'intent_id': intent_id,
                'question': question,
                'threshold': confidence,
            }
            result.append(intent_object)
    return result
      
def send_data_to_machine_learning(data, type):
    # Define the URL of the other backend API
    other_backend_url = 'http://172.20.67.124:9876/chatbot/' + type

     # Make a POST request with JSON data
    headers = {'Content-Type': 'application/json'}  # Set the content type to JSON
    response = requests.post(other_backend_url, data=data, headers=headers)

    # Check the response status code and handle accordingly
    if response.status_code == 200:
        return response.json()  # Assuming the response is JSON
    else:
        # Handle error cases
        return {'error': 'Failed to retrieve data from the other backend'}


def replace_synonyms(question, cursor, system_id):
    # Fetch all synonyms from the database
    query = f"SELECT old_value, new_value FROM synonyms_{system_id}_{chosen_table_dates[int(system_id) - 1]}"
    cursor.execute(query)
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

            updateConversation(uuid, systemID, intentID, "KORISNIK: " + answer, '', 0)

            cursor = db_connection.cursor()
            query = f"SELECT * FROM steps_{systemID}_{chosen_table_dates[int(systemID)- 1]} WHERE intent_id = {intentID}"
            cursor.execute(query)
            items = cursor.fetchall()
            cursor.close()

            json_array = items[0][3]

            rule = find_matching_rule(json.loads(json_array), conditions, int(id) + 1)
            updateConversation(uuid, systemID, intentID, "CHATBOT: " + rule['assistant_answer'], '', 1)

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

@app.route('/bigBang', methods=['GET'])
def bigBang():
    if request.method == 'GET':
        '''
        ml_questions = []

        # Iterate over each system ID (1 to 5)
        for system_id in range(1, 6):
            cursor = db_connection.cursor()
            query = f"SELECT * FROM questions WHERE system_id = {system_id}"
            cursor.execute(query)
            questions_for_system = cursor.fetchall()

            # Populate addedItems array with the questions
            added_items = [
                {
                    'IntentID': str(question[2]),  # Assuming intent_id is in the third column
                    'QuestionID': str({question[0]}),  # Assuming question_id is in the first column
                    'QuestionText': question[1]  # Assuming question is in the second column
                }
                for question in questions_for_system
            ]

            # Create the ml_questions object for the current system ID
            system_ml_questions = {
                'SystemID': str(system_id),
                'AddedItems': added_items,
                'EditedItems': [],
                'DeletedItems': []
            }

            # Add the ml_questions object to the array
            ml_questions.append(system_ml_questions)
            
        json_data = json.dumps(ml_questions)

        other_backend_url = 'http://172.20.67.22:9876/chatbot/train'
        # Make a POST request with JSON data
        headers = {'Content-Type': 'application/json'}  # Set the content type to JSON
        response = requests.post(other_backend_url, data=json_data, headers=headers)
        print(response)
        
        other_backend_url = 'http://172.20.67.23:9876/chatbot/train'
        response = requests.post(other_backend_url, data=json_data, headers=headers)
        print(response)
        '''
        # Format the time in the desired format
        formatted_time = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=1))).strftime('%Y_%m_%dT%H_%M_%S_%f')[:-3] + 'Z'
        for system_id in range(1, 6):
            '''
            # Send document learning for systemID IF PAGES ARE NOT EMPTY!!!
            # Fetch number of documents from pages
            query_num = f"SELECT COUNT(*) FROM pages WHERE system_id = {system_id}"
            cursor.execute(query_num)
            count = cursor.fetchone()[0]
            if count > 0:
                parameters = {
                    "SystemID": str(system_id)
                }
                json_parameter = json.dumps(parameters)

                requests.post('http://172.20.67.22:9877/search/train', data=json_parameter, headers={'Content-Type': 'application/json'})
                requests.post('http://172.20.67.23:9877/search/train', data=json_parameter, headers={'Content-Type': 'application/json'})

            '''
            existing_tables = ['intents', 'questions', 'steps', 'synonyms', 'thresholds', 'initials', 'pages', 'themes']
            new_tables = ['intents_' + str(system_id) + "_" + formatted_time, 'questions_' + str(system_id) + "_" + formatted_time, 'steps_' + str(system_id) + "_" + formatted_time, 'synonyms_' + str(system_id) + "_" + formatted_time, 'thresholds_' + str(system_id) + "_" + formatted_time, 'initials_' + str(system_id) + "_" + formatted_time, 'pages_' + str(system_id) + "_" + formatted_time, 'themes_' + str(system_id) + "_" + formatted_time]
            cursor = db_connection.cursor()

            for existing_table, new_table in zip(existing_tables, new_tables):
                # Step 1: Create a new table with the same structure as the existing table
                create_table_query = f"""
                    CREATE TABLE {new_table} AS
                    SELECT * FROM {existing_table} WHERE 1 = 0;
                """
                cursor.execute(create_table_query)

                # Step 2: Copy data from the existing table to the new table using COPY
                copy_data_query = f"""
                    INSERT INTO {new_table}
                    SELECT * FROM {existing_table}
                """
                # Conditionally add WHERE clause for system_id except for 'steps' table
                if existing_table != 'steps':
                    copy_data_query += f" WHERE system_id = {str(system_id)}"
                cursor.execute(copy_data_query)

            get_chosen_table_dates()

        db_connection.commit()
        cursor.close()
        return {'success': 'success'}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081)