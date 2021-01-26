function createStreamAccount() {
    send_email();
    document.getElementById("create").remove();

    div = document.getElementById('main');
    
    subDiv = document.createElement("DIV");
    subDiv.id = 'subDiv';
    div.appendChild(subDiv);

    txt = document.createElement("DIV");
    txt.id = 'textDiv';
    txt.innerHTML = "Plese Enter The Passcode We Just Sent To Your Email Address.";
    subDiv.appendChild(txt);

    input = document.createElement("INPUT");
    input.id = 'passcode-form';
    input.placeholder = "Passcode: ********";
    subDiv.appendChild(input);

    btn = document.createElement("BUTTON");
    btn.id = 'submit-btn';
    btn.innerHTML = 'Submit';
    subDiv.appendChild(btn);

    btn.onclick = () => {
        $.ajax(
            {
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                type: "POST",
                url: "/passcodes",
                data: JSON.stringify({request: "verifyPasscode", passcode: input.value}),
                success: (response) => {
                    if (response.success){
                        window.location = '/live'
                    } else {
                        try {
                            document.getElementById("error").remove();
                        } catch { }
                        error = document.createElement("DIV");
                        error.id = 'error';
                        error.innerHTML = "Worng Passcode!";
                        subDiv.appendChild(error);
                    }
                }
            }
        );
    }
}

function send_email() {
    $.ajax(
        {
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            type: "POST",
            url: "/passcodes",
            data: JSON.stringify({request: "sendEmail"}),
            success: (response) => { }
        }
    );
}