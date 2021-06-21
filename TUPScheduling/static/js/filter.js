function filter(){
    text = document.getElementById('section-filter').value;
    filterables = document.getElementsByClassName('filter');

    if(text.localeCompare('') == 0){
        for(let i = 0; i < filterables.length; i++){
            filterables[i].style.display = 'block';
        }
    }else{
        for(let i = 0; i < filterables.length; i++){
            if(filterables[i].children[0].children[1].innerText.toUpperCase().indexOf(text.toUpperCase()) != -1 || filterables[i].children[0].children[3].innerText.toUpperCase().indexOf(text.toUpperCase()) != -1 || filterables[i].children[0].children[3].children[0].children[0].getAttribute('desc').toUpperCase().indexOf(text.toUpperCase()) != -1){
                filterables[i].style.display = 'block';
                
            }else{
                filterables[i].style.display = 'none';
            }
        }
    }
    //console.log(filterables[0].children[0].children[0].innerText)
}

function filterProf(){
    text = document.getElementById('professor-filter').value;
    filterables = document.getElementsByClassName('filter-prof');

    if(text.localeCompare('') == 0){
        for(let i = 0; i < filterables.length; i++){
            filterables[i].style.display = 'block';
        }
    }else{
        for(let i = 0; i < filterables.length; i++){
            if(filterables[i].children[0].children[0].innerText.toUpperCase().indexOf(text.toUpperCase()) != -1 ){
                filterables[i].style.display = 'block';
            }else{
                let flag = 0;
                for(let j = 0; j < filterables[i].children[1].children.length; j++){
                    if(filterables[i].children[1].children[j].children[0].children[2].children[0].children[0].innerText.toUpperCase().indexOf(text.toUpperCase()) != -1 ){
                        filterables[i].style.display = 'block';
                        flag = 1;
                        break;
                    }
                }
                if(flag == 0){
                    filterables[i].style.display = 'none';
                }
            }
        }
    }
}