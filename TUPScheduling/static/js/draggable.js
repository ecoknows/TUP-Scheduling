let tiles = document.getElementsByClassName('tile');
let section_container = document.getElementById('section-container');

function section_onmousedown( draggableSectionPaper){
  let pos1 = 0;
  let pos2 = 0;
  let pos3 = 0;
  let pos4 = 0;
  let event = window.event;
  let paper_hours = 3;
  let draggableSection = draggableSectionPaper.parentElement

  event.preventDefault();
  pos3 = event.clientX;
  pos4 = event.clientY;
  
  if(!draggableSection.is_dragged){
    draggableSection.style.top = draggableSection.offsetTop - section_container.scrollTop + 'px'
    draggableSection.is_dragged = true
  }
  
  console.log('asdsafasdsa');

  
  // console.log((draggableSection.offsetTop - pos2) + "px");
  const elementDrag = e =>{
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;

    draggableSection.style.position = 'absolute'
    draggableSection.style.top = (draggableSection.offsetTop  - pos2) + "px";
    draggableSection.style.left = (draggableSection.offsetLeft - pos1) + "px";
  }

  
  
  function occupyingLogic(index){
    let x = 0;     
    while(x < paper_hours*6){
      tiles[index+x].occupied = true;
      x+=6;
    }
  
    draggableSection.tileAssigned = index; 
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
  
    const convertedDragable = convertDraggable(draggableSection.querySelector('#origin').getBoundingClientRect());
    
    if (draggableSection.tileAssigned != null){ 
      let x = 0;     
      while(x < paper_hours*6){
        tiles[draggableSection.tileAssigned+x].occupied = false;
        x+=6;
      } 
    }
    let i = 0;

    while(i < tiles.length){
      if(!tiles[i].occupied){
        const elementBoundingBox = tiles[i].getBoundingClientRect()
        const tile = convertDraggable(elementBoundingBox);

        if(checkCollision(convertedDragable,tile)){
          
          let container = tiles[i].querySelector('.tile-container');

          if(!draggableSection.in_main_table){
            draggableSection.parentElement.remove()
            draggableSection.in_main_table=true
          }


          container.appendChild(draggableSection);
          draggableSection.style.top = null
          draggableSection.style.left = null

          occupyingLogic(i);

          return;
        }
        
 
      }
      i++;
    }

    draggableSection.style.top = null
    draggableSection.style.left = null
    if(checkCollision(convertedDragable,section_container)){
      let newSectionBody = document.createElement('div');
      newSectionBody.style.width = '100%';
      newSectionBody.style.height = '150px';
      draggableSection.style.position = null
      draggableSection.is_dragged = false
      draggableSection.in_main_table = false
      draggableSection.tileAssigned = null;
      newSectionBody.appendChild(draggableSection);
      section_container.querySelector('#section-wrapper').appendChild(newSectionBody);
    }
    


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