const tiles_section = document.getElementsByClassName('section-tile');
const professor_container = document.getElementById('professor-section-container');

function professor_onmousedown(dragableProfessor){
    let pos1 = 0;
    let pos2 = 0;
    let pos3 = 0;
    let pos4 = 0;
    let event = window.event;
    let paper_hours = 3;


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
      // console.log(draggableOffsetTop, e.clientY,dragableProfessor.offsetTop-professor_container.scrollTop + 10);
      dragableProfessor.style.top = (dragableProfessor.offsetTop  - pos2) + "px";
      dragableProfessor.style.left = (dragableProfessor.offsetLeft - pos1) + "px";
    }
  
    
    
    function occupyingLogic(index){
      tiles_section[index].occupied = true;
      dragableProfessor.tileAssigned = index; 
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
      if (dragableProfessor.tileAssigned != null){ 
          tiles_section[dragableProfessor.tileAssigned].occupied = false;
      }
      let i = 0;
  
      while(i < tiles_section.length){
        if(!tiles_section[i].occupied){
          const elementBoundingBox = tiles_section[i].getBoundingClientRect()
          const tile = convertDraggable(elementBoundingBox);
  
          if(checkCollision(convertedDragable,tile)){
            
            let container = tiles_section[i].querySelector('.tile-container');
            container.appendChild(dragableProfessor);
            dragableProfessor.style.top = null
            dragableProfessor.style.left = null
            if (dragableProfessor.querySelector('#professor-name')) {
                dragableProfessor.querySelector('#professor-name').className = 'text-center'
            }
  
            occupyingLogic(i);
  
            return;
          }
          
   
        }
        i++;
      }
      
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