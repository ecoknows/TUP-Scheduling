function filter(){
    text = document.getElementById('section-filter').value;
    filterables = document.getElementsByClassName('filter');

    if(text.localeCompare('') == 0){
        for(let i = 0; i < filterables.length; i++){
            filterables[i].style.display = 'block';
        }
    }else{
        for(let i = 0; i < filterables.length; i++){
            if(filterables[i].children[0].children[0].innerText.toUpperCase().indexOf(text.toUpperCase()) != -1 || filterables[i].children[0].children[2].innerText.toUpperCase().indexOf(text.toUpperCase()) != -1 || filterables[i].children[0].children[2].children[0].children[0].getAttribute('desc').toUpperCase().indexOf(text.toUpperCase()) != -1){
                filterables[i].style.display = 'block';
                
            }else{
                filterables[i].style.display = 'none';
            }
        }
    }
    //console.log(filterables[0].children[0].children[0].innerText)
}