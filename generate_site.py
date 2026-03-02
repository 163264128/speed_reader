import json

def process_text(text):
    # Split by whitespace (\s) or any common punctuation: . , ! ? ; : " ( ) [ ] { }
    # We deliberately leave out the apostrophe (') so words like "don't" stay intact.
    # The list comprehension at the end filters out any empty strings.
    words = [w for w in re.split(r'[\s.,!?;:"()\[\]{}]+', text) if w]
    processed_words = []
    even_alt = 0  # Toggle for alternating even-length middle letters
    
    for word in words:
        n = len(word)
        if n == 0:
            continue
            
        if n % 2 != 0:
            # Odd length: exact middle
            mid = n // 2
        else:
            # Even length: alternate between n/2 and n/2 + 1 (1-based index)
            # In 0-based Python indexing: (n//2)-1 and (n//2)
            if even_alt == 0:
                mid = (n // 2) - 1
                even_alt = 1
            else:
                mid = n // 2
                even_alt = 0
                
        # Wrap the middle letter in a red span
        formatted_word = f"{word[:mid]}<span style='color: red;'>{word[mid]}</span>{word[mid+1:]}"
        processed_words.append(formatted_word)
        
    return processed_words

def generate_html(processed_words):
    words_json = json.dumps(processed_words)
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Speed Reader</title>
    <style>
        body {{
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            margin: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }}
        #word-display {{
            font-size: 16pt;
            min-height: 24pt;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 2rem;
            letter-spacing: 1px;
        }}
        .controls {{
            display: flex;
            gap: 15px;
            align-items: center;
            font-size: 14pt;
        }}
        button, select {{
            padding: 8px 16px;
            font-size: 12pt;
            cursor: pointer;
            background-color: #333;
            color: white;
            border: 1px solid #555;
            border-radius: 4px;
        }}
        button:hover, select:hover {{
            background-color: #555;
        }}
    </style>
</head>
<body>

    <div id="word-display">Ready?</div>
    
    <div class="controls">
        <button id="play-pause-btn">Play</button>
        <button id="restart-btn">Restart</button>
        
        <label for="wpm">Speed:</label>
        <select id="wpm">
            <option value="200">200 WPM</option>
            <option value="300" selected>300 WPM</option>
            <option value="450">450 WPM</option>
            <option value="600">600 WPM</option>
            <option value="800">800 WPM</option>
        </select>
    </div>

    <script>
        const words = {words_json};
        let currentIndex = 0;
        let isPlaying = false;
        let intervalId = null;
        
        const displayElement = document.getElementById('word-display');
        const playPauseBtn = document.getElementById('play-pause-btn');
        const restartBtn = document.getElementById('restart-btn');
        const wpmSelect = document.getElementById('wpm');
        
        function showNextWord() {{
            if (currentIndex >= words.length) {{
                pause();
                displayElement.innerHTML = "Done!";
                return;
            }}
            displayElement.innerHTML = words[currentIndex];
            currentIndex++;
        }}
        
        function play() {{
            if (currentIndex >= words.length) currentIndex = 0; // reset if at end
            isPlaying = true;
            playPauseBtn.innerText = "Pause";
            
            const wpm = parseInt(wpmSelect.value);
            const msPerWord = 60000 / wpm; // 60,000 ms in a minute
            
            showNextWord(); // Show immediately
            intervalId = setInterval(showNextWord, msPerWord);
        }}
        
        function pause() {{
            isPlaying = false;
            playPauseBtn.innerText = "Play";
            clearInterval(intervalId);
        }}
        
        playPauseBtn.addEventListener('click', () => {{
            if (isPlaying) pause();
            else play();
        }});
        
        restartBtn.addEventListener('click', () => {{
            pause();
            currentIndex = 0;
            displayElement.innerHTML = "Ready?";
        }});
        
        wpmSelect.addEventListener('change', () => {{
            if (isPlaying) {{
                pause();
                play();
            }}
        }});
    </script>
</body>
</html>"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("Successfully generated index.html!")

# --- YOUR TEXT GOES HERE ---
sample_text = """
This is a demonstration of the rapid serial visual presentation system. 
Notice how the middle letters are highlighted in red. 
For words with an even number of letters, the highlight alternates!
"""

if __name__ == "__main__":
    processed = process_text(sample_text)
    generate_html(processed)