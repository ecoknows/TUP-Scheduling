let tiles = document.getElementsByClassName('tile');
let section_container = document.getElementById('section-container');

function show_description(container, text){
  container.innerText = text
}
function remove_description(container, text){
  container.innerText = text
}

function section_onmousedown(draggableSectionPaper, height){
  let pos1 = 0;
  let pos2 = 0;
  let pos3 = 0;
  let pos4 = 0;
  let event = window.event;
  let paper_hours = height;
  let draggableSection = draggableSectionPaper.parentElement
  let filterDiv = draggableSection.parentElement

  event.preventDefault();
  pos3 = event.clientX;
  pos4 = event.clientY;
  
  if(!draggableSection.is_dragged){
    draggableSection.style.top = draggableSection.offsetTop - section_container.scrollTop + 'px'
    draggableSection.is_dragged = true
  }
  
  
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
    draggableSection.style.zIndex = 100;
    draggableSection.style.top = (draggableSection.offsetTop  - pos2) + "px";
    draggableSection.style.left = (draggableSection.offsetLeft - pos1) + "px";
  }

  
  function isOccupied(index){
    let x = index;
    let status = false 
    while(x <= index+(height-1)*6){
      if (tiles[x] == undefined){
        return false
      }
      if(tiles[x]?.occupied == draggableSection || tiles[x]?.occupied == undefined ){
        status = true
      }else{
        return false
      }
      
      x+=6;
    }
    return status;
  }
  function occupyingLogic(index){
    let x = 0;     
    while(x < paper_hours*6){
      tiles[index+x].occupied = draggableSection;
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

    let i = 0;

    while(i < tiles.length){
        const elementBoundingBox = tiles[i].getBoundingClientRect()
        const tile = convertDraggable(elementBoundingBox);
        draggableSection.style.zIndex = 0;

        if(checkCollision(convertedDragable,tile)){
          if(isOccupied(i)){

            let container = tiles[i].querySelector('.tile-container');

            if(!draggableSection.in_main_table){
              draggableSection.parentElement.remove()
              draggableSection.in_main_table=true
            }

            container.appendChild(draggableSection);
            draggableSection.style.top = null;
            draggableSection.style.left = null;

            if (draggableSection.tileAssigned != null){ 
              let x = 0;     
              while(x < paper_hours*6){
                tiles[draggableSection.tileAssigned+x].occupied = undefined;
                x+=6;
              } 
            }
            filterDiv.classList.remove('filter')
            occupyingLogic(i);
            return;
          }
        }
        
      i++;
    }

    draggableSection.style.top = null
    draggableSection.style.left = null
    if(!draggableSection.in_main_table){
      draggableSection.style.position = null
      draggableSection.is_dragged = false
      filterDiv.classList.add('filter')
    }
    const convertedSectionContainer = convertDraggable(section_container.getBoundingClientRect());



    if(checkCollision(convertedDragable,convertedSectionContainer) && draggableSection.in_main_table ){

      if (draggableSection.tileAssigned != null){ 
        let x = 0;     
        while(x < paper_hours*6){
          tiles[draggableSection.tileAssigned+x].occupied = undefined;
          x+=6;
        } 
      }
      let newSectionBody = document.createElement('div');
      newSectionBody.style.width = '100%';
      newSectionBody.style.height = '150px';
      draggableSection.is_dragged = false
      draggableSection.in_main_table = false
      draggableSection.tileAssigned = null;
      draggableSection.style.position = null
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