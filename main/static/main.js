function myFunc() {
    old_element = document.getElementById("url_result");
    if (old_element) {
        old_element.remove();
    }
    let url = document.getElementById('url').value;
    postData("/", {
            url: url
        })
        .then(data => addElement(data));
}

function addElement(data) {
    block = document.createElement("div");
    block.id = "url_result";
    if (data.is_success) {
        // create hyperlink element
        let code = document.createElement("a");
        code.href = data.host_name + data.code;
        code.innerText = code.href;
        block.className = "alert alert-success";
        block.appendChild(code);
        // create copy button
        let copy_btn = document.createElement("button")
        copy_btn.type = "button";
        copy_btn.dataset.clipboardText = code.href;
        copy_btn.className = "copyButton btn btn-link"
        copy_btn.innerText = "複製";
        copy_btn.onclick = () => copyEvent(code);
        block.appendChild(copy_btn);
        document.getElementById("form").appendChild(block);
    } else {
        let text = document.createElement("div");
        text.innerText = "這是一個無效的網址";
        block.className = "alert alert-warning";
        block.appendChild(text);
        document.getElementById("form").appendChild(block);
    }
}

function copyEvent(element) {
    window.getSelection().selectAllChildren(element);
    document.execCommand("Copy")
    window.getSelection().removeAllRanges();
}

function postData(url, data) {
    return fetch(url, {
            body: JSON.stringify(data),
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
                'user-agent': 'Mozilla/4.0 MDN Example',
                'content-type': 'application/json'
            },
            method: 'POST',
            mode: 'cors',
            redirect: 'follow',
            referrer: 'no-referrer',
        })
        .then(response => response.json())
}