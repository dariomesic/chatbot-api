from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import psycopg2, json, requests, uuid
app = Flask(__name__)

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
        

@app.route('/postQuestion', methods=['POST'])
def postQuestion():
    if request.method == 'POST':
        try:
            data = request.json
            question = data.get("question")
            intent_id = data.get("intent_id")
            system_id = data.get("system_id")

            cursor = db_connection.cursor()
            query = f"INSERT INTO questions (question_id, question, intent_id, system_id) VALUES (DEFAULT, '{question}', {intent_id}, {system_id}) RETURNING question_id;"
            cursor.execute(query)
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
            query = f"INSERT INTO intents (intent_id, intent_name, last_edited, examples_count, steps_count, thumbs_up, thumbs_down, system_id) VALUES (DEFAULT, '', '{current_datetime}', 0, 1, 0, 0, {system_id}) RETURNING intent_id;"
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
            intent_id = request.args.get('intent_id')
            cursor = db_connection.cursor()
            # Retrieve the current value of the counter
            query = f"SELECT thumbs_up FROM intents WHERE intent_id = {intent_id};"
            cursor.execute(query)
            current_value = cursor.fetchone()[0]
            
            # Increment the counter
            new_value = current_value + 1
            
            # Update the counter in the database
            query = f"UPDATE intents SET thumbs_up = {new_value} WHERE intent_id = {intent_id};"
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
            intent_id = request.args.get('intent_id')
            cursor = db_connection.cursor()
            # Retrieve the current value of the counter
            query = f"SELECT thumbs_down FROM intents WHERE intent_id = {intent_id};"
            cursor.execute(query)
            current_value = cursor.fetchone()[0]
            
            # Increment the counter
            new_value = current_value + 1
            
            # Update the counter in the database
            query = f"UPDATE intents SET thumbs_down = {new_value} WHERE intent_id = {intent_id};"
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
            query = f"UPDATE questions SET question = '{new_question}' WHERE question_id = {question_id};"
            cursor.execute(query)
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
            step_dict = '[{"id":1,"conditions":{},"assistant_answer":"","customer_response":"","continuation":"ZavrÃ…Â¡etak radnje"}]'

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

            query_steps = f"UPDATE steps SET step_dict = '{json.dumps(new_step)}' WHERE intent_id = {intent_id};"
            cursor.execute(query_steps)

            query_intents = f"UPDATE intents SET steps_count = '{len(new_step)}', last_edited = '{current_datetime}' WHERE intent_id = {intent_id};"
            cursor.execute(query_intents)

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
            cursor = db_connection.cursor()
            query = f"SELECT step_dict FROM steps WHERE intent_id = '{response['intent_id']}';"
            cursor.execute(query)
            item = cursor.fetchone()  # Use fetchone to get a single row
            cursor.close()

            if item:
                response_data = json.loads(item[0])  # Access the first column from the tuple
                return jsonify(response_data[response['id']])
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
                return jsonify(response_data[int(id) - 1])
            else:
                return jsonify({"error": "No matching record found"})

        except Exception as e:
            return jsonify(str(e))
        



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

            query = f"SELECT * FROM questions WHERE system_id = '{system_id}'"   #promijeniti kasnije
            cursor.execute(query)
            items = cursor.fetchall()
            json_array = [{'question': item[1], 'intent_id': item[2]} for item in items]

            # Initialize an empty list to store the transformed data
            transformed_data = []

            # Iterate over each item in the database data
            for item in json_array:
                # Create a new dictionary in the desired format
                transformed_item = {
                    "IntentID": str(item["intent_id"]),
                    "SystemID": system_id,
                    "Questions": [
                        {
                            "QuestionText": item["question"]
                        }
                    ]
                }
                # Append the transformed item to the result list
                transformed_data.append(transformed_item)

            db_connection.commit()
            cursor.close()

            json_data = json.dumps(transformed_data)

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
    



@app.route('/chatbotSentMessage', methods=['POST'])
def chatbotSentMessage():
    if request.method == 'POST':
        try:
            data = request.json
            systemID = data.get("systemID")
            question = data.get("question")
             
            # Generate a unique UUID
            sessionID = str(uuid.uuid4())

            transformed_question = {
                "SessionID": sessionID,
                "SystemID": systemID,
                "QuestionText": question
            }

            json_question = json.dumps(transformed_question)
            
            response_from_other_backend = send_data_to_machine_learning(json_question, 'query')
            intent_id = response_from_other_backend['PredictedIntent']['IntentID']

            cursor = db_connection.cursor()
            query = f"SELECT * FROM steps WHERE intent_id = {intent_id}"
            cursor.execute(query)

            items = cursor.fetchall()

            # Extract the JSON string from the database result
            json_array = items[0][3]
            cursor.close()

            result = json.loads(json_array)[0]

            result['intent_id'] = intent_id

            # Return the JSON string as a JSON response
            return jsonify(result)

        except Exception as e:
            return jsonify(str(e))


@app.route('/chatbotUserResponse', methods=['POST'])
def chatbotUserResponse():
    if request.method == 'POST':
        try:
            data = request.json
            conditions = data.get("conditions")
            intent_id = data.get("intent_id")

            cursor = db_connection.cursor()
            query = f"SELECT * FROM steps WHERE intent_id = {intent_id}"
            cursor.execute(query)
            items = cursor.fetchall()
            cursor.close()

            json_array = items[0][3]

            rule = find_matching_rule(json.loads(json_array), conditions)

            return jsonify(rule)

        except Exception as e:
            return jsonify(str(e))
        

def find_matching_rule(rules, conditions):
    # Replace "subject" with the corresponding rule ID
    for condition in conditions:
        for rule in rules:
            if condition["subject"] == rule["assistant_answer"]:
                condition["subject"] = rule["id"]
    
    for rule in rules:
        # Check if all conditions must be true or only one condition must be true
        if rule.get("conditions", {}).get("allConditionsMustBeTrue", False):
            # Check if all conditions in conditionsList match any condition in the list
            conditions_list = rule.get("conditions", {}).get("conditionsList", [])
            if all(
                any(
                    (
                        c.get("subject") == condition.get("subject")
                        and c.get("predicate") == condition.get("predicate")
                        and c.get("object") == condition.get("object")
                    )
                    for condition in conditions
                )
                for c in conditions_list
            ):
                return rule
        else:
            # Check if at least one condition in conditionsList matches any condition in the list
            conditions_list = rule.get("conditions", {}).get("conditionsList", [])
            if any(
                any(
                    (
                        c.get("subject") == condition.get("subject")
                        and c.get("predicate") == condition.get("predicate")
                        and c.get("object") == condition.get("object")
                    )
                    for condition in conditions
                )
                for c in conditions_list
            ):
                return rule
    return None  # No matching rule found


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)