This is Jarvis - a voice assistant with real voice from the Iron man film. For text generation, I use Gemini from Google, but because of this it doesn't work in Russia. 

To use Jarvis you have to install the repository, python and models and create keys.yaml file or you can download .exe file and edit everything in _instances file.

How to install models:
<ul>
    <li>
        To install Piper models you have to (english Jarvis model will be installed by default):
        <ul>
            <li>Install model from the <a href="https://rhasspy.github.io/piper-samples/">site</a> (.onnx and .onnx.json files).</li>
            <li>Create a folder inside 'piper-models' folder with any name you want and put these both files in it.</li>
        </ul>
    </li>
    <li>
        To install Vosk models you have to (english small model will be installed by default):
        <ul>
            <li>Install model from the <a href="https://alphacephei.com/vosk/models/">site</a>.</li>
            <li>Extract file from the zip file and put it inside 'vosk-models' folder.</li>
        </ul>
    </li>
</ul>

How to create keys.yaml file:
<ul>
    <li>create file named keys.yaml</li>
    <li>
        fill it with:
        <ul>
            <li>porcupine: your porcupine api key (you can create it <a href="https://console.picovoice.ai/">here</a>)</li>
            <li>genai: your gemini api key (you can create it <a href="https://aistudio.google.com/app/api-keys/">here</a>)</li>
        </ul>
    </li>
</ul>

How to create your own extention (see extentions/hibernate system.yaml as an example):
<ul>
    <li>Create file with any name you want to, but it should have the .yaml extention</li>
    <li>
        Then you have insert some properties:
        <ul>
            <li>actions - command to execute (now only sp/run (it runs command in terminal) and cancel (it just makes Jarvis stop listening comands) are supported)</li>
            <li>voice/your languge - words to speek while executing actions</li>
            <li>phrases - phrases to listen to</li>
        </ul>
    </li>
</ul>

Jarvis versions:
<ul>
    <li>
        <a href="https://github.com/Vlad21islav/Jarvis/releases/tag/English-small/">small-english-beta-jarvis-version</a>
    </li>
</ul>
