This is Jarvis - a voice assistant with real voice from the Iron man film. For text generation, I use Gemini from Google and after some manipulations with server, it now can be used in Russia.

To use Jarvis you have to install the repository, python and models and create keys.yaml file or you can download .exe file and edit everything in _instances file.

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

<h3>How to create keys.yaml file:</h3>
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

<h3>How to create your own extention (see extentions/hibernate system.yaml as an example):</h3>
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
                <td>keyboard.press</td>
                <td>Presses a button on a keyboard</td>
                <td><code>keyboard.press {key}</code></td>
            </tr>
            <tr>
                <td>keyboard.release</td>
                <td>Releases a button on a keybord</td>
                <td><code>keyboard.release {key}</code></td>
            </tr>
            <tr>
                <td>keyboard.tap</td>
                <td>Presses and releases a button on a keybord</td>
                <td><code>keyboard.tap {key}</code></td>
            </tr>
            <tr>
                <td>keyboard.type</td>
                <td>Types something</td>
                <td><code>keyboard.type {text}</code></td>
            </tr>
            <tr>
                <td>plan</td>
                <td>In any seconds plans any action</td>
                <td><code>plan {time} {action}</code></td>
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
    <li><a href="https://github.com/Vlad21islav/Jarvis/releases/tag/English-small/">small-english-beta-jarvis-version</a></li>
    <li><a href="https://github.com/Vlad21islav/Jarvis/releases/tag/English-Russian-small/">small-english-russian-first-jarvis-version</a></li>
</ul>

<h3>Taken things:</h3>
<ul>
    <li>Icon from <a target="_blank" href="https://icons8.com/icon/41255/jarvis-home-assistant">Icons8</a></li>
</ul>
