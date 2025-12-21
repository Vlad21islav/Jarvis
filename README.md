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
    <li>Create file named keys.yaml</li>
    <li>
        Fill it with:
        <ul>
            <li>Porcupine: your porcupine api key (you can create it <a href="https://console.picovoice.ai/">here</a>)</li>
            <li>Genai: your gemini api key (you can create it <a href="https://aistudio.google.com/app/api-keys/">here</a>)</li>
        </ul>
    </li>
</ul>

How to create your own extention (see extentions/hibernate system.yaml as an example):
<ul>
    <li>Create file with any name you want to, but it should have the .yaml extention</li>
    <li>
        Then you have insert some properties:
        <ul>
            <li>actions - Command to execute</li>
            <li>voice/your languge - Words to speek while executing actions</li>
            <li>phrases - Phrases to listen to</li>
        </ul>
    </li>
    <li>
        actions:
        <ul>
            <li>sp/run - Runs a command in terminal. How to use: <code>sp/run {windows command}</code></li>
            <li>keyboard.press - Presses a button on a keyboard. How to use: <code>keyboard.press {key}</code></li>
            <li>keyboard.release - Releases a button on a keybord. How to use: <code>keyboard.release {key}</code></li>
            <li>keyboard.tap - Presses and releases a button on a keybord. How to use: <code>keyboard.tap {key}</code></li>
            <li>keyboard.type - Types something. How to use: <code>keyboard.type {text}</code></li>
            <li>plan - In any seconds plans any action. How to use: <code>plan {action}</code></li>
            <li>cencel - Stops listening vosk. How to use: <code>cencel</code></li>
        </ul>
    </li>
</ul>

Jarvis versions:
<ul>
    <li><a href="https://github.com/Vlad21islav/Jarvis/releases/tag/English-small/">small-english-beta-jarvis-version</a></li>
    <li><a href="https://github.com/Vlad21islav/Jarvis/releases/tag/English-Russian-small/">small-english-russian-first-jarvis-version</a></li>
</ul>
