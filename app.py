from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quiz Generator</title>
        <style>
            body {font-family: Arial; text-align: center; padding: 50px; background: #f0f8ff;}
            input {padding: 10px; width: 300px; font-size: 16px;}
            button {padding: 10px 20px; background: blue; color: white; border: none; font-size: 16px; cursor: pointer;}
            button:hover {background: darkblue;}
        </style>
    </head>
    <body>
        <h1>📚 AI Quiz Generator</h1>
        <p>Type any topic and get a quiz instantly!</p>
        <form method="POST" action="/generate">
            <input type="text" name="topic" placeholder="Example: Dogs, Math, History..." required>
            <br><br>
            <button type="submit">Generate Quiz</button>
        </form>
    </body>
    </html>
    '''

@app.route('/generate', methods=['POST'])
def generate():
    topic = request.form['topic']
    
    questions = [
        {"q": f"1. What is {topic}?", 
         "opts": ["A simple definition", "A complicated thing", "A type of animal", "A country"],
         "ans": "A simple definition"},
        {"q": f"2. Why is {topic} important?",
         "opts": ["For fun", "For learning", "For work", "All of the above"],
         "ans": "All of the above"},
        {"q": f"3. Where can you learn about {topic}?",
         "opts": ["School", "Internet", "Books", "All of these"],
         "ans": "All of these"},
        {"q": f"4. Who should study {topic}?",
         "opts": ["Children", "Adults", "Everyone", "No one"],
         "ans": "Everyone"},
        {"q": f"5. Is {topic} useful?",
         "opts": ["Yes", "No", "Maybe", "I don't know"],
         "ans": "Yes"}
    ]
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quiz on {topic}</title>
        <style>
            body {{font-family: Arial; padding: 20px; max-width: 800px; margin: auto; background: #f9f9f9;}}
            .question {{margin: 20px 0; padding: 15px; background: white; border-radius: 10px;}}
            button {{background: green; color: white; padding: 10px 20px; font-size: 16px; border: none; cursor: pointer;}}
            h2 {{color: blue;}}
        </style>
    </head>
    <body>
        <h2>Quiz on: {topic}</h2>
        <form method="POST" action="/score">
    '''
    
    for i, q in enumerate(questions):
        html += f'''
        <div class="question">
            <p><strong>{q['q']}</strong></p>
        '''
        for opt in q['opts']:
            html += f'''
            <label>
                <input type="radio" name="q{i}" value="{opt}"> {opt}
            </label><br>
            '''
        html += '</div>'
    
    html += f'''
        <input type="hidden" name="topic" value="{topic}">
        <button type="submit">Submit Answers</button>
        </form>
    </body>
    </html>
    '''
    return html

@app.route('/score', methods=['POST'])
def score():
    topic = request.form.get('topic', 'your topic')
    score = 0
    for i in range(5):
        if request.form.get(f'q{i}'):
            score += 1
    percentage = (score / 5) * 100
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Your Score</title>
        <style>
            body {{font-family: Arial; text-align: center; padding: 50px; background: #e8f5e9;}}
            .score {{font-size: 48px; color: green;}}
            button {{padding: 10px 20px; background: blue; color: white; border: none; cursor: pointer;}}
        </style>
    </head>
    <body>
        <h1>✅ Quiz Complete!</h1>
        <p>You finished the quiz on: <strong>{topic}</strong></p>
        <div class="score">Your score: {int(percentage)}%</div>
        <p>You got {score} out of 5 questions correct</p>
        <br>
        <a href="/"><button>Take Another Quiz</button></a>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)