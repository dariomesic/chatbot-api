from flask import Flask, request, jsonify
from datetime import datetime
import psycopg2, json, requests, time
app = Flask(__name__)

# Database configuration
db_connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="3.75.212.152"
)

@app.route('/')
def hello():
    return 'Hello, Flask!'

@app.route('/getIntents', methods=['GET'])#, 'POST'])
def getIntents():
    if request.method == 'GET':
        try:
            cursor = db_connection.cursor()
            query = "SELECT * FROM intents"
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

            cursor = db_connection.cursor()
            query = f"INSERT INTO questions (question_id, question, intent_id) VALUES (DEFAULT, '{question}', {intent_id}) RETURNING question_id;"
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
        
@app.route('/addIntent', methods=['GET'])
def addIntent():
    if request.method == 'GET':
        try:
            cursor = db_connection.cursor()
            current_datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            query = f"INSERT INTO intents (intent_id, intent_name, last_edited, examples_count, steps_count) VALUES (DEFAULT, '', '{current_datetime}', 1, 0) RETURNING intent_id;"
            print(query)
            cursor.execute(query)
            db_connection.commit()

            # Fetch the inserted question_id
            intent_id = cursor.fetchone()[0]
        
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

            intent_id = request.args.get('intent_id')
            cursor = db_connection.cursor()
            query = f"DELETE FROM intents WHERE intent_id = '{intent_id}';"
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
            data = request.json
            intent_id = data.get("intent_id")
            step_dict = '[{"name":"Step 1","conditions":{},"assistant_answer":"","customer_response":"","continuation":"Završetak radnje"}]'

            cursor = db_connection.cursor()
            query = f"INSERT INTO steps (step_id, name_step, intent_id, step_dict) VALUES (DEFAULT, '1', {intent_id}, {step_dict});"
            cursor.execute(query)
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

            cursor = db_connection.cursor()
            query = f"UPDATE steps SET step_dict = '{json.dumps(new_step)}' WHERE intent_id = {intent_id};"
            cursor.execute(query)
            db_connection.commit()
            cursor.close()

            return jsonify("Step updated successfully!")

        except Exception as e:
            return jsonify(str(e))


#sending questions do machine learning   
@app.route('/sendQuestions', methods=['GET'])
def sendQuestions():
    if request.method == 'GET':
        try:

            cursor = db_connection.cursor()
            query = "SELECT * FROM questions"
            cursor.execute(query)
            items = cursor.fetchall()
            json_array = [{'question': item[1], 'intent_id': item[2]} for item in items]

            # Initialize an empty list to store the transformed data
            transformed_data = []

            # Iterate over each item in the database data
            for item in json_array:
                # Create a new dictionary in the desired format
                transformed_item = {
                    "IntentID": str(item["intent_id"]),  # Convert to string if needed
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
            question = data.get("question")

            transformed_question = {
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