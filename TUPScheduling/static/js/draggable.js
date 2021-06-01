// var tiles = document.getElementsByClassName('tile')
// var section_tile = document.getElementsByClassName('section-tile');

function draggable(draggable_name,tile_name,paper_container){
  let tiles = document.getElementsByClassName(tile_name);
  class DraggableElement{
    constructor(draggbablePaper){
      this.pos1 = 0;
      this.pos2 = 0;
      this.pos3 = 0;
      this.pos4 = 0;
      this.paper_hours = 3;
      this.starting_tile_index = null;
      this.draggbablePaper = draggbablePaper;
      this.placementPositionTop =  draggbablePaper.style.top;
      this.placementPositionLeft =  draggbablePaper.style.left;
      this.paperHead = draggbablePaper.querySelector('#paper-head')
      this.dragElement();
    }
  
    dragElement(){
      if(this.paperHead){
        this.paperHead.onmousedown = this.eventMouseDown.bind(this);
      }else{
        this.draggbablePaper.onmousedown = this.eventMouseDown.bind(this);
      }
    }
    
  
    eventMouseDown(e){
      e = e || window.event;
      e.preventDefault();
      // get the mouse cursor position at startup:
      this.pos3 = e.clientX;
      this.pos4 = e.clientY;
      document.onmouseup = this.closeDragElement.bind(this);
      // call a function whenever the cursor moves:
      document.onmousemove = this.elementDrag.bind(this);
    }
    
    elementDrag(e){
      e = e || window.event;
      e.preventDefault();
      // calculate the new cursor position:
      this.pos1 = this.pos3 - e.clientX;
      this.pos2 = this.pos4 - e.clientY;
      this.pos3 = e.clientX;
      this.pos4 = e.clientY;
      // set the element's new position:
      this.draggbablePaper.style.position = 'absolute'
      this.draggbablePaper.style.top = (this.draggbablePaper.offsetTop - this.pos2) + "px";
      this.draggbablePaper.style.left = (this.draggbablePaper.offsetLeft - this.pos1) + "px";
    }
  
    draggableInfo(element){
      return{
        bottom : element.y + element.height,
        left: element.x,
        right: element.x + element.width,
        top: element.y
      }
    }


    resetStartingTile(){
      //RESET STARTING TILE   
      if(this.starting_tile_index != null){
        for(let i = 0; i < this.paper_hours*5; i+=5){
          if(tiles[this.starting_tile_index+i]?.occupied)
            tiles[this.starting_tile_index+i].occupied = null;
        }
        this.starting_tile_index = null;
      }
    }
    
    occupyingLogic(index){
      this.resetStartingTile();
      let x = 0;     
      while(x < this.paper_hours*5){
        tiles[index+x].occupied = true;
        x+=5;
      }
    
      this.starting_tile_index = index; 
    }
  
  
    collision(){
  
      const draggablePaper = this.draggableInfo(this.draggbablePaper.querySelector('#origin').getBoundingClientRect());
      
      let i = 0;
  
      while(i < tiles.length){
        if(!tiles[i].occupied){
          const elementBoundingBox = tiles[i].getBoundingClientRect()
          const tile = this.draggableInfo(elementBoundingBox);
  
          if(this.checkCollision(draggablePaper,tile)){
            
            let container = tiles[i].querySelector('.tile-container');
            container.appendChild(this.draggbablePaper);
            this.draggbablePaper.style.top = null
            this.draggbablePaper.style.left = null

            this.occupyingLogic(i);
  
            return;
          }
          
   
        }
        i++;
      }
      const paperSection = document.getElementById(paper_container);
      const paperContainerBoundingBox = paperSection.getBoundingClientRect()
      const paperContainer = this.draggableInfo(paperContainerBoundingBox);

      if(this.checkCollision(draggablePaper,paperContainer)){
        paperSection.appendChild(this.draggbablePaper);
        this.draggbablePaper.style.top = null
        this.draggbablePaper.style.left = null
        this.draggbablePaper.style.position = null

        this.resetStartingTile();
        return;
      }

      // NOT COLLIDE RESET ALL 
      this.draggbablePaper.style.left = this.placementPositionLeft; 
      this.draggbablePaper.style.top = this.placementPositionTop;
      if(this.starting_tile_index == null){
        this.draggbablePaper.style.position = null
      }
  
  
    }
  
    checkCollision(paper, box){
  
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
    
    closeDragElement(){
      document.onmouseup = null;
      document.onmousemove = null;
      this.collision();
    }
  
  }
  
  var draggables = document.getElementsByClassName(draggable_name);
  
  Array.prototype.forEach.call(draggables,(element) => {
    new DraggableElement(element);
  });
}



// draggable('draggable-paper','tile','section-container');
// draggable('draggable-professor','section-tile','professor-container', false);



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

  
  // console.log((draggableSection.offsetTop - pos2) + "px");
  const elementDrag = e =>{
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;

    // set the element's new position:
    draggableSection.style.position = 'absolute'
    // console.log(draggableOffsetTop, e.clientY,draggableSection.offsetTop-section_container.scrollTop + 10);
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


  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    draggableSection.onmouseup = null;
    draggableSection.onmousemove = null;
    collision()
  }

  draggableSection.onmouseup = closeDragElement
  draggableSection.onmousemove = elementDrag

}