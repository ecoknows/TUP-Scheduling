function dropDown(name, type){
    room = document.getElementById('title');
    room.innerText = name + " (" + type + ")";

    changeTable();
}

function filterRoom(){
    text = document.getElementById('room-filter').value;
    rooms = document.getElementsByClassName('room');
    reset_icon_div = document.getElementsByClassName('reset-icon-div');

    if(text.localeCompare('') == 0){
        for(let i = 0; i < rooms.length; i++){
            rooms[i].style.display = 'block';
            reset_icon_div[i].style.display = 'flex';
        }
    }else{
        for(let i = 0; i < rooms.length; i++){
            if(rooms[i].innerText.toUpperCase().indexOf(text.toUpperCase()) != -1){
                rooms[i].style.display = 'block';
                reset_icon_div[i].style.display = 'flex';
            }else{
                rooms[i].style.display = 'none';
                reset_icon_div[i].style.display = 'none';
            }
        }
    }
}

window.onload = function() {
    changeTable();
}

function changeTable(){
    tables = document.getElementsByClassName('mainTable');
    title = document.getElementById('title').innerText;
    for(let i = 0; i < tables.length; i++){
        if(title.toUpperCase().localeCompare(tables[i].getAttribute("desc").toUpperCase()) == 0){
            tables[i].style.display = 'block';
        }else{
            tables[i].style.display = 'none';
        }
    }
}

function resetRoom(name, type){
    if (confirm("Are you sure you want to reset \"" + name + " (" + type + ")\"?")) {
        $("#reset-room").trigger("submit");
    }else{
        return false;
    }
}

function resetAll(){
    if (confirm("Are you sure you want to reset the whole schedule?")) {
        $("#reset-all").trigger("submit")
    }
    else{
        return false;
    }
}