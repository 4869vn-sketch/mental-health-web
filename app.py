from flask import Flask, render_template, request, url_for
import sqlite3
import requests

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

    elif "hello" or "hi" in message:
        return "Hi dog, how can I help you with your mental health today?"
    
    elif "What should I do?" or "advice" in message:
        return "Hello, what problem are you facing?"

    else:
        return "I recommend talking with a mental health professional if you are experiencing serious symptoms." or "How do you feel?"

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
        },
        {
            "id": 6,
            "name": "Schizophrenia",
            "description": "A severe, chronic mental disorder characterized by dissonance in thinking, emotions and behavior, often including paranoia and hallucinations.",
            "symptoms": "Delusions, hallucinations, throught/ language disorders, bizarre/ disorganized behavior, negative symptoms",
            "note": "Some people are aware of their mental illness, while others with mental illness are not. It is often assumed that all people with mental illess have cognitive impairment." f"<a href='https://www.nimh.nih.gov/news/science-updates/2024/life-with-schizoaffective-disorder'target='_blank'style='color: red;'>Newspaper NIMH</a>" f"<a href='https://bachmai.gov.vn/bai-viet/sinh-hoat-cau-lac-bo-nguoi-nha-nguoi-benh-mac-benh-tam-than-phan-liet?id=c4613e80-0173-b558-e1c5-4a9f21b4014d'target='_blank'style='color: blue;'>Newspaper Bach Mai</a>"
        },
        {
            "id": 7,
            "name": "Anorexia Nervosa",
            "description": "Patients starve themselves due to an overwhelming fear of gaining weight and becoming disfigured. This disease is more common in female.",
            "symptoms": "Severe weight loss, fatigue, insomnia, changes in skin and hair, poor tolerance, endocrine disorders (in women). Extreme dieting, food obsession, lying about eating habis. Extreme fear of weight gain, irritability."
        }
    ]

@app.route("/chatbot", methods=["GET","POST"])
def chatbot():

    reply = None

    if request.method == "POST":

        message = requests.form["message"]
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

@app.route("/test/Bipolar Disorder", methods=["GET","POST"])
def bipolar_disorder_test():
    if request.method == "POST":
        score = 0
        for i in range(1, 20):
            score += int(request.form.get(f"q{i}", 0))
        #Nhóm 1: Manic / Hypomanic Symptoms
        manic_score = 0
        for i in range(1, 8):
            manic_score += int(request.form.get(f"q{i}", 0))
        manic_pct = int((manic_score / 35)*100)

        #Nhóm 2: Depressive Symptoms
        depressive_score = 0
        for i in range(8, 15):
            depressive_score += int(request.form.get(f"q{i}", 0))
        depressive_pct = int((depressive_score / 35)*100)

        #Nhóm 3: Mixed Symptoms
        mixed_score = 0
        for i in range(15, 20):
            mixed_score += int(request.form.get(f"q{i}", 0))
        mixed_pct = int((mixed_score / 25)*100)

        #Trả về trang kết quả với các % tương ứng
        return render_template("Bipolar_result.html", manic_pct=manic_pct, depressive_pct=depressive_pct, mixed_pct=mixed_pct, score=score)
    #Nếu chưa submit thì hiện trang làm bài test
    return render_template("Bipolar_test.html")

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
    if request.method == "POST":
        score = 0
        for i in range(1, 20):
            score += int(request.form.get(f"q{i}", 0))
        #Nhóm 1: Washing
        washing_score = 0
        for i in range(1, 4):
            washing_score += int(request.form.get(f"q{i}", 0))
        washing_pct = int((washing_score / 12)*100)

        #Nhóm 2: Checking
        checking_score = 0
        for i in range(4, 7):
            checking_score += int(request.form.get(f"q{i}", 0))
        checking_pct = int((checking_score / 12)*100)

        #Nhóm 3: Ordering/Symmetry
        ordering_score = 0
        for i in range(7, 10):
            ordering_score += int(request.form.get(f"q{i}", 0))
        ordering_pct = int((ordering_score / 12)*100)

        #Nhóm 4: Obsessing
        obsessing_score = 0
        for i in range(10, 13):
            obsessing_score += int(request.form.get(f"q{i}", 0))
        obsessing_pct = int((obsessing_score / 12)*100)

        #Nhóm 5: Hoarding
        hoarding_score = 0
        for i in range(13, 16):
            hoarding_score += int(request.form.get(f"q{i}", 0))
        hoarding_pct = int((hoarding_score / 12)*100)

        #Nhóm 6: Neutralizing
        neutralizing_score = 0
        for i in range(16, 19):
            neutralizing_score += int(request.form.get(f"q{i}", 0))
        neutralizing_pct = int((neutralizing_score / 12)*100)

        #Trả về trang kết quả với các % tương ứng
        return render_template("OCD_result.html", washing_pct=washing_pct, checking_pct=checking_pct, ordering_pct=ordering_pct, obsessing_pct=obsessing_pct, hoarding_pct=hoarding_pct, neutralizing_pct=neutralizing_pct, score=score)
    #Nếu chưa submit thì hiện trang làm bài test
    return render_template("OCD_test.html")

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

@app.route("/test/Schizophrenia", methods=["GET","POST"])
def schizophrenia_test():
    result = None
    if request.method == "POST":
        score = 0
        for i in range(1, 17):
            score += int(request.form.get(f"q{i}", 0))
        if score <= 8:
            result = "Minimal symtoms"
        elif 9 <= score <= 16:
            result = "Mild symptoms"
        elif 17 <= score <= 28:
            result = "Moderate symptoms (monitor closely)"
        elif 29 <= score <= 40:
            result = "High symptoms (consider professional evaluation)"
        elif 41 <= score <= 48:
            result = "Very high symptoms (strongly recommended to seek help)"
        return render_template("Schizophrenia_result.html", result = result, score = score)
    return render_template("Schizophrenia_test.html", result = result)

@app.route("/test/Anorexia Nervosa", methods=["GET","POST"])
def anorexia_nervosa_test():
    result = None
    if request.method == "POST":
        score = 0
        for i in range(1, 27):
            score += int(request.form.get(f"q{i}", 0))
        if score <= 15:
            result = "Minimal symtoms"
        elif 16 <= score <= 30:
            result = "Mild symptoms"
        elif 31 <= score <= 50:
            result = "Moderate symptoms (monitor closely)"
        elif 51 <= score <= 65:
            result = "High symptoms (consider professional evaluation)"
        elif 66 <= score <= 78:
            result = "Very high symptoms (strongly recommended to seek help)"
        return render_template("Anorexia_result.html", result = result, score = score)
    return render_template("Anorexia_test.html", result = result)

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
    app.run(host="0.0.0.0", port=5000)
