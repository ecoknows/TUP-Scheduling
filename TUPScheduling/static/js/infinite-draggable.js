
let tiles_section = document.getElementsByClassName('section-tile');
const professorContainer = document.getElementById('professor-container');

class DragProfessor{
    constructor(draggableProfessor){
        this.pos1 = 0;
        this.pos2 = 0;
        this.pos3 = 0;
        this.pos4 = 0;
        this.placementPositionTop = draggableProfessor.style.top;
        this.placementPositionLeft = draggableProfessor.style.left;
        this.draggableProfessor = draggableProfessor
        this.draggableProfessor.onmousedown = this.eventMouseDown.bind(this);
        this.tileAssigned = null;
    }

    eventMouseDown(e){
        e = e || window.event;
        e.preventDefault();
        this.pos3 = e.clientX;
        this.pos4 = e.clientY;
        this.draggableProfessor.style.position = 'absolute'
        document.onmouseup = this.closeDragElement.bind(this);
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
        this.draggableProfessor.style.top = (this.draggableProfessor.offsetTop - this.pos2) + "px";
        this.draggableProfessor.style.left = (this.draggableProfessor.offsetLeft - this.pos1) + "px";
    }
    
    convertDraggable(element){
      return{
        bottom : element.y + element.height,
        left: element.x,
        right: element.x + element.width,
        top: element.y
      }
    }

    occupyingLogic(index) {
        tiles_section[index].occupied = true;
        this.tileAssigned = index;
    }

    
    collision(){
        const draggablePaper = this.convertDraggable(this.draggableProfessor.querySelector('#origin').getBoundingClientRect());
        this.draggableProfessor.style.position = null
        
        if (this.tileAssigned != null){ 
            tiles_section[this.tileAssigned].occupied = false;
        }
        
        let i = 0;

        while (i < tiles_section.length) {
            if (!tiles_section[i].occupied) {
                const elementBoundingBox = tiles_section[i].getBoundingClientRect()
                const tile = this.convertDraggable(elementBoundingBox);

                if (this.checkCollision(draggablePaper, tile)) {

                    let container = tiles_section[i].querySelector('.tile-container');
                    container.appendChild(this.draggableProfessor);
                    this.draggableProfessor.style.top = null
                    this.draggableProfessor.style.left = null

                    if (this.draggableProfessor.querySelector('#professor-name')) {
                        this.draggableProfessor.querySelector('#professor-name').className = null
                    }

                    this.occupyingLogic(i);

                    return;
                }


            }
            i++;
        }

        this.draggableProfessor.remove()
        
    }



    checkCollision(paper, box) {

        if (
            paper.top > box.bottom ||
            paper.right < box.left ||
            paper.bottom < box.top ||
            paper.left > box.right
        ) {
            return false;
        } else {
            return true;
        }

    }


    closeDragElement(){
      document.onmouseup = null;
      document.onmousemove = null;
      this.collision();
    }
    


}


function professor_onmousemove(draggableProfessor){
    let cloneDraggableProfessor = draggableProfessor.querySelector('#draggable-professor').cloneNode(true);
    cloneDraggableProfessor.style.position = 'absolute'
    cloneDraggableProfessor.style.top = draggableProfessor.offsetTop + 'px'
    professorContainer.appendChild(cloneDraggableProfessor)
    new DragProfessor(cloneDraggableProfessor)
}
