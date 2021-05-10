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



draggable('draggable-paper','tile','section-container');
// draggable('draggable-professor','section-tile','professor-container', false);