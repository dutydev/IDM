function getMeToken() {
    const login = encodeURIComponent(prompt('Введи свой логин'));
    const pass = encodeURIComponent(prompt('Введи свой pass'));
    sendReq(login, pass, null)
}

function sendReq(login, password, code) {
    let url = ('https://oauth.vk.com/token?' +
        'grant_type=password&client_id=6146827&client_secret=qVxWRF1CwHERuIrKBnqe&' +
        `username=${login}&password=${password}&` +
        `v=5.131&2fa_supported=1&code=${code}`);
    let req = new XMLHttpRequest();
    req.onload = () => {
        if (req.status != 200) {
            alert(`Ошибка ${req.status}: ${req.statusText}`);
        } else {
            alert(req.response);
        };
    };
    req.onerror = (err) => { alert(`Запрос не удался ${err}`) };
    req.open('GET', url);
    req.send();
}


sendReq('blob', 'heh', '');