var output_text = ''

function edit_content(HTML) {
    document.getElementById("content").innerHTML = HTML;
}

function add_content(HTML) {
    document.getElementById("content").innerHTML += HTML;
}

window.load_extentions = function() {
    edit_content(`
        <div id="extensions-container">
            <div id="extention_list"></div>
            <textarea id="config_input"></textarea>
        </div>
    `);
    config_input = document.getElementById("config_input");
    window.change_textarea = function(file_path) {
        window.pywebview.api.get_file_content(file_path).then(result => {
            config_input.value = result;
            config_input.name = file_path;
        });
    };

    window.add_extention = function() {
        let new_extention = prompt("Введите имя нового расширения:");
        if (new_extention) {
            window.pywebview.api.add_extention(new_extention);
        }
        update_extentions();
    }

    window.delete_extention = function(name) {
        window.pywebview.api.delete_extention(name);
        update_extentions();
    };

    function update_extentions() {
        window.pywebview.api.get_extentions().then(result => {
            extention_list = document.getElementById("extention_list");
            extention_list.innerHTML = "";

            result.forEach(element => {
                extention_list.innerHTML += `
                    <div class="ext-btn">
                        <span onclick="change_textarea('./extentions/${element}/command.yaml')">${element}</span>
                        <button onclick="delete_extention('${element}')">✕</button>
                    </div>
                `;
            });

            extention_list.innerHTML += `
                <div class="ext-add" onclick="add_extention()">+ Add extension</div>
            `;
        });
    };
    update_extentions();

    config_input.addEventListener("input", () => {
        let text = config_input.value;
        window.pywebview.api.submit(config_input.name, text);
    });
};

window.load_main = function() {
    function send_command(text) {
        window.pywebview.api.send_command(text);
    };
    window.handleEnter = function(event, value) {
        if (event.key == 'Enter' && value != "") {
            send_command(value);
            document.getElementById("command_input").value = "";
        };
    };
    edit_content(`
        <div>
            <input align="center" id="command_input" onkeydown="handleEnter(event, value)" type="input" placeholder="Say aloud or enter the command">
        </div>
        <div id="output">${output_text}</div>
        <div class="reactor-container arc-cyan">
            <div class="reactor-container-inner circle abs-center"></div>
            <div class="tunnel circle abs-center"></div>
            <div class="core-wrapper circle abs-center"></div>
            <div class="core-outer circle abs-center"></div>
            <div class="core-inner circle abs-center"></div>
            <div class="coil-container">
                <div class="coil coil-1"></div>
                <div class="coil coil-2"></div>
                <div class="coil coil-3"></div>
                <div class="coil coil-4"></div>
                <div class="coil coil-5"></div>
                <div class="coil coil-6"></div>
                <div class="coil coil-7"></div>
                <div class="coil coil-8"></div>
            </div>
            <div class="outer-ring-container">
                <div class="outer-ring"></div>
            </div>
        </div>
        <button class="change-mode-button" onclick="document.body.className === 'light-mode' ? document.body.className='dark-mode' : document.body.className='light-mode'">◐</button>
    `);
    window.update_output_text = function(text) {
        output = document.getElementById("output");
        output_text = text
        if (output) {
            output.innerHTML = text;
        }
    }
};

window.load_settings = function() {
    edit_content('');
    function renderSelect(name, config) {
        let html = ''
        html += `
            <div class="setting-block">
                <p class="setting-name">${config["name"]}</p>
        `;
        if (config["type"] === "select") {
            window.change_config = function(key, value) {
                window.pywebview.api.change_config(key, value);
            };

            html += `
                <select name="${name}" onchange="change_config(name, value)" id="${name}">
            `;

            const select = document.getElementById(name);
            config["options"].forEach(opt => {
                html += `
                    <option value="${opt}" ${opt === config["selected"] ? "selected" : ""}>${opt}</option>
                `;
            });

            html += `</select>`;

        } else {
            html += `
                <input name="${name}" oninput="change_config(name, value)" type="input" value="${config["value"]}">
            `;
        };
        html += `
                <p class="setting-description">${config["description"]}</p>
            </div>
        `;
        add_content(html);
    };

    window.pywebview.api.get_config().then(result => {
        Object.entries(result).forEach(([key, value]) => {
            renderSelect(key, value);
        });
    });
};

window.load_language_settings = function() {
    edit_content(`
        <textarea id="config_input"></textarea>
    `);
    config_input = document.getElementById("config_input");
    window.change_textarea = function(file_path) {
        window.pywebview.api.get_file_content(file_path).then(result => {
            config_input.value = result;
            config_input.name = file_path;
        });
    };
    change_textarea("./resources/translation.yaml");

    config_input.addEventListener("input", () => {
        let text = config_input.value;
        window.pywebview.api.submit(config_input.name, text);
    });
};

window.load_api_keys = function() {
    window.change_keys = function(key, value) {
        window.pywebview.api.change_keys(key, value);
    }
    edit_content(``);
    window.pywebview.api.get_keys().then(result => {
        Object.entries(result).forEach(([key, value]) => {
            add_content(`
                <div class="setting-block">
                    <label>${key}</label>
                    <input name="${key}" oninput="change_keys(name, value)" type="input" value="${value}">
                </div>
            `);
        });
    });
}

window.addEventListener('pywebviewready', () => {
    load_main();
});
