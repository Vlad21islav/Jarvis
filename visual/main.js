var output_text = '';

function edit_content(HTML) {
    document.getElementById("content").innerHTML = HTML;
};

function add_content(HTML) {
    document.getElementById("content").innerHTML += HTML;
};

async function translate(text) {
    const result = await window.pywebview.api.translate(text);
    return result;
}

function update_app_theme(theme=NaN) {
    if (!theme) {
        window.pywebview.api.get_config().then(result => {
            if (result["app-theme"]["selected"] == 'Auto') { 
                window.pywebview.api.get_auto_theme().then(result => {
                    !result ? document.body.className='dark-mode' : document.body.className='light-mode';
                });
                return;
            };
            result["app-theme"]["selected"] == 'Dark' ? document.body.className='dark-mode' : document.body.className='light-mode';
        });
        return;
    };
    if (theme == 'Auto') { 
        window.pywebview.api.get_auto_theme().then(result => {
            !result ? document.body.className='dark-mode' : document.body.className='light-mode';
        });
        return;
    };
    theme == 'Dark' ? document.body.className='dark-mode' : document.body.className='light-mode';
};

window.load_extentions = async function() {
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

    window.add_extention = async function() {
        let new_extention = prompt(await translate("Enter the name of the new extension:"));
        if (new_extention) {
            window.pywebview.api.add_extention(new_extention);
        }
        update_extentions();
    }

    window.delete_extention = async function(name) {
        if (confirm(await translate("Are you sure you want to delete") + ` ${name}?`)) {
            window.pywebview.api.delete_extention(name);
        }
        update_extentions();
    };

    async function update_extentions() {
        window.pywebview.api.get_extentions().then(async result => {
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
                <div class="ext-add" onclick="add_extention()">${await translate("+ Add extension")}</div>
            `;
        });
    };
    update_extentions();

    config_input.addEventListener("input", () => {
        let text = config_input.value;
        window.pywebview.api.submit(config_input.name, text);
    });
};

window.load_main = async function() {
    function send_command(text) {
        window.pywebview.api.send_command(text);
    };
    window.handleEnter = function(event, value) {
        if (event.key == 'Enter' && value != "") {
            send_command(value);
            document.getElementById("command_input").value = "";
        };
    };
    window.open_history = function() {
        document.getElementById("history").style.display = "block";
        document.getElementById("history-button").style.display = "none";
        document.getElementById("history-container").style.display = "flex";
        document.getElementById("output").style.left = "calc(20px + 300px / 2)";
        update_history();
    }
    window.hide_history = function() {
        document.getElementById("history").style.display = "none";
        document.getElementById("history-button").style.display = "block";
        document.getElementById("history-container").style.display = "block";
        document.getElementById("output").style.left = "50%";
    }
    window.clear_history = function() {
        window.pywebview.api.submit("resources/history.yaml", "");
        update_history();
    }

    let coils = "";
    var num_coils = 8;
    for (let coil = 0; coil <= num_coils - 1; coil++) {
        coils += `<div class="coil" style="rotate: ${360 / num_coils * coil}deg"></div>`;
    }

    edit_content(`
        <div id="history-container">
            <div>
                <div id="input-div">
                    <input align="center" id="command_input" onkeydown="handleEnter(event, value)" type="input" placeholder="${await translate('Say aloud or enter the command')}">
                    <button id="history-button" onclick="open_history()">${await translate('History')}</button>
                </div>
                <div id="output"><p>${output_text}</p></div>
                <div class="reactor-container arc-cyan">
                    <div class="reactor-container-inner circle abs-center"></div>
                    <div class="tunnel circle abs-center"></div>
                    <div class="core-wrapper circle abs-center"></div>
                    <div class="core-outer circle abs-center"></div>
                    <div class="core-inner circle abs-center"></div>
                    <div class="coil-container">
                        ${coils}
                    </div>
                    <div class="outer-ring-container">
                        <div class="outer-ring"></div>
                    </div>
                </div>
            </div>
            <div id="history">
                <div id="history-buttons">
                    <button onclick="clear_history()" id="clear-history">${await translate('Clear history')}</button>
                    <button onclick="hide_history()" id="hide-history">✕</button>
                </div>
                <hr>
                <div id="history-content"></div>
            </div>
        </div>
    `);
    window.update_output_text = function(text) {
        output = document.getElementById("output");
        output_text = text
        if (output) {
            output.innerHTML = text;
        }
    }
    window.update_history = function() {
        content = document.getElementById("history-content");
        content.innerHTML = "";
        window.pywebview.api.get_yaml_file_content("resources/history.yaml").then(result => {
            result.forEach(opt => {
                content.innerHTML += `
                    <div class="setting-block">
                        <p class="setting-name">${opt["text"]}</p>
                        <p class="setting-description">${opt["role"]}</p>
                    </div>
                `
            });
            content.scrollTop = content.scrollHeight;
        });
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
            window.change_config = async function(key, value) {
                if (key === "app-theme") { update_app_theme(value); }
                else if (key === "language") { await update_buttons(); }
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
};

async function update_buttons() {
    setTimeout(async () => {
        document.getElementById("header").innerHTML = `
            <button onclick="load_main()">${await translate("Main")}</button>
            <button onclick="load_settings()">${await translate("Settings")}</button>
            <button onclick="load_extentions()">${await translate("Extensions")}</button>
            <button onclick="load_language_settings()">${await translate("Language settings")}</button>
            <button onclick="load_api_keys()">${await translate("API keys")}</button>
        `;
    }, 50);
};

window.addEventListener('pywebviewready', () => {
    update_app_theme();
    load_main();
    update_buttons();
});
