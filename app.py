from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

#Chatbot trả lời đơn giản
def chatbot_response(message):
    message = message.lower()

    if "stress" in message:
        return "Stress can be reduced by resting, exercising, and talking to someone you trust. Do you understand, you dog?"

    elif "depression" in message:
        return "Depression symptoms include sadness, loss of interest, and fatigue. Consider seeking professional help."

    elif "anxiety" in message:
        return "Anxiety often involves excessive worry. Breathing exercises and relaxation techniques may help."

    elif "hello" in message:
        return "Hi dog, how can I help you with your mental health today?"

    else:
        return "I recommend talking with a mental health professional if you are experiencing serious symptoms."

def get_disorders():
    return [
        {
            "id": 1,
            "name": "Anxiety Disorder",
            "description": "A condition characterized by excessive worry and fear.",
            "symptoms": "Restlessness, rapid heartbeat."
        },
        {
            "id": 2,
            "name": "Bipolar Disorder",
            "description": "A disorder associated with episodes of mood swings.",
            "symptoms": "Insomnia, rapid speed, overcondifidence during mania, exhaustion, low self-esteem during depression."
        },
        {
            "id": 3,
            "name": "Avoidant personality disorder (AvPD)",
            "description": "A condition characterized by social inhibition, extreme low self-esteem and excessive sensitivity to critism and rejection.",
            "symptoms": "Avoiding social activities, fear of rejection/ mockery."
        },
        {
            "id": 4,
            "name": "Borderline personality disorder (BPD)",
            "description": "A characterized by instability in emotions, self-image and behavior, along with sharky relationships.",
            "symtoms": "Extreme fear of abandonment, impulsive behavior, rapid mood swings, self-harm/ suicidal behavior and persistent feelings of emptiness."
        },
        {
            "id": 5,
            "name": "Obsessive-compulsive disorder (OCD)",
            "description": "Persistent, obsessive thoughts that cause anxiety and repetitive, compulsive behaviors to alleviate that anxiety.",
            "symptoms": "Repetitive throughts, repetitive behaviors."
        }
    ]

@app.route("/chatbot", methods=["GET","POST"])
def chatbot():

    reply = None

    if request.method == "POST":

        message = request.form["message"]
        reply = chatbot_response(message)

    return render_template("chatbot.html", reply=reply)

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/diseases")
def disease_list():
    return render_template("diseases.html")

@app.route("/disorders")
def disorder_list():
    disorders = get_disorders()
    return render_template("disorders.html", disorders=disorders)

@app.route("/disorder/<int:id>")
def disorder_detail(id):
    disorder = next((d for d in get_disorders() if d["id"] == id), None)
    return render_template("disorders_detail.html", disorder=disorder)

@app.route("/test/Anxiety Disorder", methods=["GET","POST"])
def anxiety_disorder_test():
    result = None
    if request.method == "POST":
        score = 0
        for i in range(1, 21):
            score += int(request.form.get(f"q{i}", 0))
        if score <= 10:
            result = "Minimal or no anxiety"
        elif 11 <= score <= 20:
            result = "Mild anxiety"
        elif 21 <= score <= 35:
            result = "Moderate anxiety (pay attention)"
        elif 36 <= score <= 50:
            result = "High anxiety (should take action)"
        elif 51 <= score <= 60:
            result = "Very high anxiety (consider professional help)"
        return render_template("anxiety_result.html", result = result, score = score)
    return render_template("anxiety_test.html", result = result)

@app.route("/test/AvPD", methods=["GET","POST"])
def AvPD_test():
    result = None
    if request.method == "POST":
        score = 0
        for i in range(1, 21):
            score += int(request.form.get(f"q{i}", 0))
        if score <= 10:
            result = "Minimal avoidant traits"
        elif 11 <= score <= 20:
            result = "Mild avoidant tendencies"
        elif 21 <= score <= 35:
            result = "Moderate avoidant traits (worth reflecting on)"
        elif 36 <= score <= 50:
            result = "High avoidant traits (may impact life significantly)"
        elif 51 <= score <= 60:
            result = "Very high avoidant traits (consider professional evaluation)"
        return render_template("AvPD_result.html", result = result, score = score)
    return render_template("AvPD_test.html", result = result)

@app.route("/test/OCD", methods=["GET","POST"])
def OCD_test():
    result = None
    if request.method == "POST":
        score = 0
        for i in range(1, 19):
            score += int(request.form.get(f"q{i}", 0))
        if score <= 12:
            result = "Minimal symptoms"
        elif 13 <= score <= 24:
            result = "Mild OCD symptoms"
        elif 25 <= score <= 40:
            result = "Moderate symtoms (worth monitoring)"
        elif 41 <= score <= 60:
            result = "High symptoms (likely impacting daily life)"
        elif 61 <= score <= 72:
            result = "Very high symptoms (consider professional help)"
        return render_template("OCD_result.html", result = result, score = score)
    return render_template("OCD_test.html", result = result)

@app.route("/test/BPD", methods=["GET","POST"])
def BPD_test():
    result = None
    if request.method == "POST":
        score = 0
        for i in range(1, 11):
            score += int(request.form.get(f"q{i}", 0))
        if score <= 3:
            result = "Low likelihood of BPD traits"
        elif 4 <= score <= 6:
            result = "Moderate traits (worth paying attention)"
        elif 7 <= score <= 10:
            result = "High likelihood of BPD traits (consider professional evaluation)"
        return render_template("BPD_result.html", result = result, score = score)
    return render_template("BPD_test.html", result = result)

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS messages(name TEXT, message TEXT)")
        c.execute("INSERT INTO messages VALUES (?,?)",(name,message))

        conn.commit()
        conn.close()

        return "Your message has been saved."

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)