var tiles = document.getElementsByClassName('tile')
console.log(tiles);

class DraggableElement{
  constructor(draggbablePaper){
    this.pos1 = 0;
    this.pos2 = 0;
    this.pos3 = 0;
    this.pos4 = 0; 
    this.draggbablePaper = draggbablePaper;
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

  collision(){

    var draggablePaper = this.draggableInfo(this.draggbablePaper.querySelector('#origin').getBoundingClientRect());
    Array.prototype.forEach.call(tiles,(element)=>{
      var elementBoundingBox = element.getBoundingClientRect()
      var tile = this.draggableInfo(elementBoundingBox);

      if(this.checkCollision(draggablePaper,tile)){
        this.draggbablePaper.style.top = elementBoundingBox.top + 'px'
        this.draggbablePaper.style.left = elementBoundingBox.left + 'px'
      }

    })


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
    this.collision();
    document.onmouseup = null;
    document.onmousemove = null;
  }

}

var draggables = document.getElementsByClassName('draggable-paper');

console.log(draggables[0]);
Array.prototype.forEach.call(draggables,(element) => {
  new DraggableElement(element);
});

