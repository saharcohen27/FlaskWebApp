$("#form").submit(e => {
    e.preventDefault();

    email = document.getElementById("email").value;
    uname = document.getElementById("uname").value;
    psw = document.getElementById("psw").value;

    $.ajax(
        {
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            type: "POST",
            url: "/register",
            data: JSON.stringify({email:email, uname:uname, psw:psw}),
            success: (response) => {
                if (!response.success) {
                    var span = document.getElementsByClassName("close")[0];
                    var modal = document.getElementById("myModal");

                    modal.style.display = "block";

                    // When the user clicks on <span> (x), close the modal
                    span.onclick = () => {
                        modal.style.display = "none";
                    }
                } else {
                    window.location = '/login'
                }
            }
        }
    );
});