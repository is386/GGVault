let auth_url = "http://127.0.0.1:8080/auth"

function authHome() {
    if (!localStorage.ggToken) {
        location.href="/client/index.html";
        return;
    }

    $.ajax({
        url: auth_url,
        type: 'POST',
        dataType: 'json',
        headers: {"Authorization": "Bearer " + localStorage.ggToken},
        complete: function(data) {
            let status = data.status;
            if (status != 200) {
                location.href="/client/index.html";
            }
        }
    });
}

function authLogin() {
    if (!localStorage.ggToken) {
        return;
    }

    $.ajax({
        url: auth_url,
        type: 'POST',
        dataType: 'json',
        headers: {"Authorization": "Bearer " + localStorage.ggToken},
        complete: function(data) {
            let status = data.status;
            if (status == 200) {
                location.href="/client/home.html";
            }
        }
    });
}

function logout() {
    localStorage.removeItem("ggToken");
    location.reload();
}