let editor1 = CodeMirror.fromTextArea(document.getElementById('query1'), {
    mode: 'text/x-sql',
    theme: 'monokai',
    lineNumbers: true,
    indentWithTabs: true,
    smartIndent: true,
    matchBrackets: true,
    autofocus: true,
    lineWrapping: true
});

let editor2 = CodeMirror.fromTextArea(document.getElementById('query2'), {
    mode: 'text/x-sql',
    theme: 'monokai',
    lineNumbers: true,
    indentWithTabs: true,
    smartIndent: true,
    matchBrackets: true,
    autofocus: true,
    lineWrapping: true
});

document.getElementById('toggle-menu').addEventListener('click', function () {
    const leftColumn = document.getElementById('left-column');
    const toggleButton = document.getElementById('toggle-menu');
    if (leftColumn.classList.contains('visible-left')) {
        leftColumn.classList.remove('visible-left');
        leftColumn.classList.add('hidden-left');
        toggleButton.innerHTML = '&#x25B6;';
    } else {
        leftColumn.classList.remove('hidden-left');
        leftColumn.classList.add('visible-left');
        toggleButton.innerHTML = '&#x25C0;';
    }
});

async function sendQueries() {
    editor1.save();
    editor2.save();
    const form = document.getElementById('form-queries');
    const formData = new FormData(form);
    const query1 = formData.get('query1');
    const query2 = formData.get('query2');

    const response = await fetch(form.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({first_sql: query1, second_sql: query2})
    });

    const result = await response.json();
    showTopAlert(result.data)
}

async function submitIsolationLevel() {
    const form = document.getElementById('isolation-form');
    const formData = new FormData(form);
    const isolationLevel = formData.get('isolation-operation');

    const response = await fetch(form.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({isolation_level: isolationLevel})
    });

    const result = await response.json();
    showTopAlert(result.data)
}

async function submitLockLevel() {
    const form = document.getElementById('lock-form');
    const formData = new FormData(form);
    const lockLevel = formData.get('lock-operation');

    const response = await fetch(form.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({lock_level: lockLevel})
    });

    const result = await response.json();
    showTopAlert(result.data)
}

async function initDB(sendUrl) {
    const response = await fetch(sendUrl, {
        method: 'GET'
    });
    const result = await response.json();
    showTopAlert(result.data)
}

function showTopAlert(message) {
    const alertElement = document.createElement('div');
    alertElement.classList.add('top-alert');
    alertElement.textContent = message;

    const container = document.getElementById('top-alert-container');
    container.appendChild(alertElement);

    setTimeout(() => {
        container.removeChild(alertElement);
    }, 3000);
}
