This is Jarvis - a voice assistant with real voice from the Iron man film. For text generation you can choose between Google Gemini and Sber GigaChat.

To use Jarvis you have to install the repository, python and models or you can download .exe file and edit everything in _instances file.

<h3>How to install models:</h3>
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

<h3>Where to find api keys:</h3>
<ul>
    <li>Porcupine: your porcupine api key (you can create it <a href="https://console.picovoice.ai/">here</a>).</li>
    <li>Genai: your gemini api key (you can create it <a href="https://aistudio.google.com/app/api-keys/">here</a>).</li>
    <li>Gigachat: your gigachat Authorization key (you can create it <a href="https://developers.sber.ru/studio/workspaces/">here</a>).</li>
</ul>

<h3>How to create your own extention (see hibernate system as an example):</h3>
<ul>
    <li>Click "Add extention" in Jarvis app and enter any name you want and click on it in extentions list.</li>
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
        <table>
            <tr>
                <th>Command</th>
                <th>Description</th>
                <th>How to use</th>
            </tr>
            <tr>
                <td>sp/run</td>
                <td>Runs a command in terminal</td>
                <td><code>sp/run {windows command}</code></td>
            </tr>
            <tr>
                <td>keyboard.send</td>
                <td>Presses and releases a button or combination of buttons on a keybord</td>
                <td><code>keyboard.send {key}</code></td>
            </tr>
            <tr>
                <td>keyboard.write</td>
                <td>Writes something</td>
                <td><code>keyboard.write {text}</code></td>
            </tr>
            <tr>
                <td>plan</td>
                <td>In any seconds plans any action</td>
                <td><code>plan {time} {action}</code></td>
            </tr>
            <tr>
                <td>serial</td>
                <td>Sends command to a serial port</td>
                <td><code>serial {command}</code></td>
            </tr>
            <tr>
                <td>cencel</td>
                <td>Stops listening vosk</td>
                <td><code>cencel</code></td>
            </tr>
        </table>
    </li>
</ul>

<h3>Jarvis versions:</h3>
<ul>
    <li><a href="https://github.com/Vlad21islav/Jarvis/releases/tag/English-Russian-small/">small-english-russian-first-jarvis-version</a></li>
    <li><a href="https://github.com/Vlad21islav/Jarvis/releases/tag/English-small/">small-english-beta-jarvis-version</a></li>
</ul>

<h3>Taken things:</h3>
<ul>
    <li>Icon from <a target="_blank" href="https://icons8.com/icon/41255/jarvis-home-assistant">Icons8</a></li>
</ul>
