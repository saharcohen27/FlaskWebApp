
document.getElementById('desc').addEventListener('click', () => {
    addDesc();
});
        

function addDesc(){
    descDiv = document.getElementById('description');
    descP = document.getElementById('desc');
    try {
        document.getElementById('addDescBtn').style.display = 'none';
    } catch (error) {
        console.log(error);
    }
    descP.style.display = 'none';

    txt = document.createElement("INPUT");
    txt.id = 'txtDesc'
    txt.placeholder = 'Add Description...';
    txt.value = descP.innerHTML;
    descDiv.appendChild(txt);

    btn = document.createElement("BUTTON");
    btn.innerHTML = "Save";
    btn.id='saveDesc'
    descDiv.appendChild(btn);


    btn.onclick = () => {
        if (txt.value) {
            newDesc = {desc: txt.value};
            txt.remove();
            btn.remove();
            $.ajax(
                {
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    type: "POST",
                    url: "/profile",
                    data: JSON.stringify(newDesc),
                    success: (response) => {
                        descP.innerHTML = response.payload.desc;
                        descP.style.display = '';

                    }
                }
            );
        }
    }
}
