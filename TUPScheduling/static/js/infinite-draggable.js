const tiles_section = document.getElementsByClassName('section-tile');
const professor_container = document.getElementById('professor-section-container');

function update_schedule(schedule_pk, prof_pk, units){
  $.ajax({
      type: 'POST',
      data: {
        update_schedule: true,
        schedule_pk,
        prof_pk,
        units: units,
        csrfmiddlewaretoken: csrftoken
      },
      success: function (response) {
        
      },
  })
}


function remove_prof_schedule(schedule_pk, prof_pk, units){
  $.ajax({
      type: 'POST',
      data: {
        update_remove_schedule: true,
        schedule_pk,
        prof_pk,
        units: units ? units.value : null,
        csrfmiddlewaretoken: csrftoken
      },
      success: function (response) {
        
      },
  })
}

function professor_onmousedown(dragableProfessor, units){
    let pos1 = 0;
    let pos2 = 0;
    let pos3 = 0;
    let pos4 = 0;
    let event = window.event;
    // let unit = document.getElementById('units');
    
    if (!dragableProfessor.units_container){

      let units_prof = professor_container.querySelector('#prof-'+dragableProfessor.querySelector('#prof_pk').value)
      dragableProfessor.units_container= units_prof
      console.log(units_prof);
    }
    
    dragableProfessor.style.position = 'absolute'

    if(!dragableProfessor.is_placed){
        let replaceDraggableProfessor = dragableProfessor.cloneNode(true);
        replaceDraggableProfessor.style.position = null
        dragableProfessor.parentElement.appendChild(replaceDraggableProfessor)
        dragableProfessor.is_placed = true
    }
    
    event.preventDefault();
    pos3 = event.clientX;
    pos4 = event.clientY;
    
    if(!dragableProfessor.is_dragged){
      dragableProfessor.style.top = dragableProfessor.offsetTop - professor_container.scrollTop + 'px'
      dragableProfessor.is_dragged = true
    } else if(dragableProfessor.is_placed){
        dragableProfessor.style.top = dragableProfessor.offsetTop - section_container.scrollTop + 'px'
    }
    
  
    
    // console.log((dragableProfessor.offsetTop - pos2) + "px");
    const elementDrag = e =>{
      e = e || window.event;
      e.preventDefault();
      // calculate the new cursor position:
      pos1 = pos3 - e.clientX;
      pos2 = pos4 - e.clientY;
      pos3 = e.clientX;
      pos4 = e.clientY;
  
      // set the element's new position:
      dragableProfessor.parentElement.parentElement.parentElement.style.zIndex = 100
      // console.log(draggableOffsetTop, e.clientY,dragableProfessor.offsetTop-professor_container.scrollTop + 10);
      dragableProfessor.style.top = (dragableProfessor.offsetTop  - pos2) + "px";
      dragableProfessor.style.left = (dragableProfessor.offsetLeft - pos1) + "px";
    }
  
    
    
    function occupyingLogic(index){
      tiles_section[index].occupied = true;
      dragableProfessor.tileAssigned = tiles_section[index]; 
    }
  
    
    function checkCollision(paper, box){
    
      if(
        paper.top > box.bottom || 
        paper.right < box.left || 
        paper.bottom < box.top || 
        paper.left > box.right
      ){
        return false;
      }else{
        return true;
      }
  
    }
    
    function convertDraggable(element){
      return{
        bottom : element.y + element.height,
        left: element.x,
        right: element.x + element.width,
        top: element.y
      }
    }
    
    
    function collision(){
      const convertedDragable = convertDraggable(dragableProfessor.querySelector('#origin').getBoundingClientRect());
      dragableProfessor.style.position = null
      dragableProfessor.parentElement.parentElement.parentElement.style.zIndex = 0 
      if (dragableProfessor.tileAssigned != null){ 
        dragableProfessor.tileAssigned.occupied = false;
      }
      let i = 0;
  
      while(i < tiles_section.length){
        if(!tiles_section[i].occupied){
          const elementBoundingBox = tiles_section[i].getBoundingClientRect()
          const tile = convertDraggable(elementBoundingBox);
  
          if(checkCollision(convertedDragable,tile)){

            tile_subject_code = tiles_section[i].querySelector('#subject-code')
            professor_subject_code = dragableProfessor.querySelector('#subject-code')

            if(tile_subject_code){
              if (professor_subject_code.innerHTML != tile_subject_code.innerHTML){
                break;
              }
              professor_subject_code.className = 'hidden'
            }

            let schedule_pk = tiles_section[i].querySelector('#schedule_pk');
            if(schedule_pk){
              update_schedule(
                schedule_pk.value,
                dragableProfessor.querySelector('#prof_pk').value,
                tiles_section[i].querySelector('#subject_units').value
              )
            }

            let new_draggable = dragableProfessor;
            
            if(dragableProfessor.units_container){
              new_unit = parseInt(dragableProfessor.units_container.innerText) + units;
              dragableProfessor.units_container.innerText = new_unit;
            }

            

            new_draggable.setAttribute('placed', 'true');

            let prof_image_container = tiles_section[i].querySelector('.prof-image-container')
            let prof_image = dragableProfessor.querySelector('#prof-image')
            prof_image.style.display = null 
            prof_image.querySelector('#body').className = null
            prof_image_container.appendChild(dragableProfessor)
            
            dragableProfessor.className = null
            dragableProfessor.style= null
            occupyingLogic(i);
  
            return;
          }
        }
        i++;
      }
      

      if(dragableProfessor.tileAssigned){
        let schedule_pk = dragableProfessor.tileAssigned.querySelector('#schedule_pk');
        if(schedule_pk){
          remove_prof_schedule(
            schedule_pk.value,
            dragableProfessor.querySelector('#prof_pk').value,
            dragableProfessor.tileAssigned.querySelector('#subject_units')
          )
        }
        
        if(dragableProfessor.units_container){
          new_unit = parseInt(dragableProfessor.units_container.innerText) - units;
          dragableProfessor.units_container.innerText = new_unit;
        }
      }
      console.log('REMOVEEE!');
      dragableProfessor.remove()
    }
  
    function closeDragElement() {
      // stop moving when mouse button is released:
      document.onmouseup = null;
      document.onmousemove = null;
      collision()
    }
  
    document.onmouseup = closeDragElement
    document.onmousemove = elementDrag
  
}