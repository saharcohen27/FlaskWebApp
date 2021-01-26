function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    profile = {
        email: profile.getEmail(),
        image: profile.getImageUrl(),
        try:1
    };
    $.ajax(
        {
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            type: "POST",
            url: "/login",
            data: JSON.stringify(profile),
            success: (response) => {
                if (response.success == true) {
                    window.location.href = '/';
                } else if (response.success == false) {
                    popup(profile);
                } else {
                    // invalid request
                    signOut();
                }
            }
        }
    );
}

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });
}

function popup(profile) {
    const modal = document.getElementById("myModal");
    const span = document.getElementsByClassName("close")[0];
    const modalContent = document.getElementById("m-content");
    modalContent.innerHTML = '';

    modal.style.display = "block";

    // When the user clicks on <span> (x), close the modal
    span.onclick = () => {
        modal.style.display = "none";
        signOut();
    }
    
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = (event) => {
    if (event.target == modal) {
            modal.style.display = "none";
            signOut();
        }
    }

    popupTitle = document.createElement("h1");
    popupTitle.id = 'popupTitle';
    popupTitle.innerHTML = 'Your Username Is Taken.'
    modalContent.appendChild(popupTitle);

    par = document.createElement("P");
    par.id = 'p-explain'
    par.innerHTML = "Your username is automatically sets to your email address username. <br> \
                    For example: JohnDoe@gmail.com means your username is JohnDoe. <br> \
                    Our system detected there is already an user with this username so we are asking you to change yours. <br> Thanks for the understanding!"
    modalContent.appendChild(par);

    txt = document.createElement("INPUT");
    txt.id = 'username'
    txt.placeholder = 'New Username...';
    modalContent.appendChild(txt);

    btn = document.createElement("BUTTON");
    btn.innerHTML = "Submit";
    btn.id='usernameSubmit'
    modalContent.appendChild(btn);

    errors = document.createElement("div");
    errors.id = 'errors'
    errors.innerHTML = 'Still Taken. Please Try Again.'
    errors.style.display = 'none';
    modalContent.appendChild(errors);

    btn.onclick = () => {
        if (txt.value){
            $.ajax(
                {
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    type: "POST",
                    url: "/login",
                    data: JSON.stringify({username:txt.value, email:profile.email, image:profile.image, try:2}),
                    success: (response) => {
                        // alert(response.authorized)
                        if (response.success) {
                            window.location.href = '/';
                        } else {
                            errors.style.display = "";
                        }
                    }
                }
            );
        }
    }
}