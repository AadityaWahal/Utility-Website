# Text-to-Speech Website

This project is a simple web application that implements text-to-speech functionality using Python and HTML. Users can input text into a form, and the application will convert the text to speech and provide an audio output.

## Project Structure

```
text-to-speech-website
├── static
│   ├── css
│   │   └── styles.css
├── templates
│   └── index.html
├── app.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd text-to-speech-website
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

3. Enter the text you want to convert to speech and click the "Convert" button.

4. The audio will be generated and played back to you.

## Dependencies

- Flask
- gTTS or pyttsx3 (depending on the implementation)

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes. 

## License

This project is licensed under the MIT License.