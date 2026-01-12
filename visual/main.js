let poller = null

function edit_content(HTML) {
    document.getElementById("content").innerHTML = HTML;
}

function add_content(HTML) {
    document.getElementById("content").innerHTML += HTML;
}

window.load_extentions = function() {
    edit_content(`
        <div id="extention_list"></div>
        <textarea id="config_input"></textarea>
    `);
    config_input = document.getElementById("config_input");
    window.change_textarea = function(file_path) {
        window.pywebview.api.get_file_content(file_path).then(result => {
            config_input.value = result;
            config_input.name = file_path;
        });
    };

    window.add_extention = function() {
        let new_extention = prompt("Введите имя нового расширения (включая .yaml):");
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
            extention_list.innerHTML = "";
            extention_list = document.getElementById("extention_list");
            result.forEach((element, index) => {
                extention_list.innerHTML += `<button onclick="change_textarea('./extentions/${element}')">${element}<button onclick="delete_extention('${element}')">x</button></button>`;
            });
            extention_list.innerHTML += `<button onclick="add_extention()">+</button>`;
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
            <input id="command_input" onkeydown="handleEnter(event, value)" type="input">
        </div>
        <div id="output"></div>
    `);
    if (!poller) {
        poller = setInterval(() => {
            window.pywebview.api.get_last_displayed_text().then(result => {
                let el = document.getElementById("output");
                if (el) {
                    el.innerHTML = result;
                }
            });
        }, 100);
    }
};

window.load_settings = function() {
    edit_content(``);
    function renderSelect(name, config) {
        if (config["type"] == "select") {
            window.change_config = function(key, value) {
                window.pywebview.api.change_config(key, value);
            };
            add_content(`
                <div>
                    <label>${name}</label>
                    <select name="${name}" onchange="change_config(name, value)" id="${name}"></select>
                </div>
            `);
            select = document.getElementById(name);
            config["options"].forEach((opt) => {
                select.innerHTML += `
                    <option value="${opt}" ${opt == config["selected"] ? "selected" : ""}>${opt}</option>
                `;
            });
        } else {
            add_content(`
                <div>
                    <label>${name}</label>
                    <input name="${name}" oninput="change_config(name, value)" type="input" value="${config["value"]}">
                </div>
            `);
        };
        
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
    change_textarea("./translation.yaml");

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
                <div>
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
