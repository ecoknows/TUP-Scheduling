function dropDown(name, type){
    room = document.getElementById('title');
    room.innerText = name + " (" + type + ")";

    changeTable();
}

function filterRoom(){
    text = document.getElementById('room-filter').value;
    rooms = document.getElementsByClassName('room');

    if(text.localeCompare('') == 0){
        for(let i = 0; i < rooms.length; i++){
            rooms[i].style.display = 'block';
        }
    }else{
        for(let i = 0; i < rooms.length; i++){
            if(rooms[i].innerText.toUpperCase().indexOf(text.toUpperCase()) != -1){
                rooms[i].style.display = 'block';
                
            }else{
                rooms[i].style.display = 'none';
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