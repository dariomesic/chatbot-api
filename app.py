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
            json_array = [{'id': item[0], 'name': item[1]} for item in items]   #for now this is okay however in future this should have another get for each intent too see how many steps and questions and edit time are there

            # Convert the list of dictionaries to a JSON string
            intents = json.dumps(json_array, ensure_ascii=False)

            print(intents)

            cursor.close()

            return jsonify({"intents": intents})

        except Exception as e:
            return jsonify({"error": str(e)})
        
@app.route('/getSteps', methods=['GET'])#, 'POST'])
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

            return jsonify({"steps": steps})

        except Exception as e:
            return jsonify({"error": str(e)})
        

@app.route('/postQuestion', methods=['POST'])
def postQuestion():
    if request.method == 'POST':
        try:
             data = request.json
             question = data.get("question")
             intent_id = data.get("intent_id")

             cursor = db_connection.cursor()
             query = f"INSERT INTO questions (question_id, question, intent_id) VALUES (DEFAULT, {question}, {intent_id});"
             cursor.execute(query)
             db_connection.commit()
             cursor.close()

             return jsonify({"message": "Question added successfully!"})

        except Exception as e:
            return jsonify({"error": str(e)})



if __name__ == '__main__':
    app.run(debug=True)

#first api /getAllIntents
#second api /getAllQuestion/question and #third api /getRules from intent from second api togehter
#fourth api /addQuestion with intent
#fifth api /updateRule 