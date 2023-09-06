from flask import Flask, request, jsonify
import psycopg2, json
app = Flask(__name__)

# Database configuration
db_connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="3.75.190.103"
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
        
@app.route('/getSteps', methods=['GET'])
def getSteps():
    if request.method == 'GET':
        try:
            intent_id = request.args.get('intent_id')
            cursor = db_connection.cursor()
            query = f"SELECT * FROM steps WHERE intent_id = {intent_id}" #or query = "SELECT * FROM steps WHERE intent_id = {}".format(intent_id)
            cursor.execute(query)

            items = cursor.fetchall()
            json_array = [{'step_id': item[0], 'name_step': item[1], 'intent_id': item[2], 'step_dict': item[3]} for item in items]

            # Convert the list of dictionaries to a JSON string
            steps = json.dumps(json_array, ensure_ascii=False)

            cursor.close()

            return jsonify(steps)

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
            query = f"INSERT INTO questions (question_id, question, intent_id) VALUES (DEFAULT, '{question}', {intent_id}) RETURNING question_id;;"
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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

#first api /getAllIntents
#second api /getAllQuestion/question and #third api /getRules from intent from second api togehter
#fourth api /addQuestion with intent
            #/updateQuestion with intent
            #/deleteQuestion with intent
#fifth api /updateRule
#sixth api /sendQuestion from chatbot for intent
#seventh api /getResponse when user selects bots answer(this can be done with frontend)