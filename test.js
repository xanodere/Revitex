
    function removeAllChildNodes(parent) {
        while (parent.firstChild) {
            parent.removeChild(parent.firstChild);
        }
    }
        window.onload = function(){
       document.getElementsByClassName("select2-selection")[0].addEventListener("click",() => { 
    
          
            
            let options = document.getElementsByClassName("select2-results__option--selectable");
    
    
    
           for(i=0;i<options.length; i++){
               if(options[i].textContent == "Ordre alphabetique"){
                options[i].addEventListener("mousedown", function(e){
                let pere = document.getElementById("contain");
                removeAllChildNodes(pere); 
                
                const request = new Request('/tri/'.concat(e.target.innerHTML))
                fetch(request).then(response => response.json()).then(result => {
                    let tab = [];
                    let jsondefault = JSON.parse(result);
                    for(i=0;i<jsondefault.length;i++){
                        console.log(jsondefault[i]["fields"]["nom"]);
                    
    
                    {% for center in centre %}
                        
                        if("{{center.nom}}" == jsondefault[i]["fields"]["nom"]){
                            pere.insertAdjacentHTML("beforeend", `<div class="col-lg-4 col-md-6 mb-5" id="{{ center.nom }}">
                                                <div class="listing-item  ">
                                                    
                                                    <div class="listing-small-badges-container">
                                                                                            
                                                    </div>
                                                        <img src="{{center.image.url}}" alt="">
    
                                                                            <div class="listing-badge now-closed">Mnt Fermé</div>
                                                                                    
    
                                                    <div class="listing-item-content">
                                                            
                                                        <h3>{{center.get__titre }} 
                                                        <i class="verified-icon"></i>
                                                        </h3>
                                                        <span>{{center.adresse }}</span>
                                                    </div>
                                                    <span class="save like-icon"></span>
                                                    
                                                </div>
                                                </div>`
                            )};
    
                    {% endfor %}
    
                };
                })
    
                
                })
            }
        
         }
        })
    }
    
function tri_master(nom_element){
    window.onload = function(){
        document.getElementsByClassName("select2-selection")[0].addEventListener("click",() => { 
     
           
             
             let options = document.getElementsByClassName("select2-results__option--selectable");
     
     
     
            for(i=0;i<options.length; i++){
                if(options[i].textContent == nom_element){
                 options[i].addEventListener("mousedown", function(e){
                 let pere = document.getElementById("contain");
                 removeAllChildNodes(pere); 
                 
                 const request = new Request('/tri/'.concat(e.target.innerHTML))
                 fetch(request).then(response => response.json()).then(result => {
                     let tab = [];
                     let jsondefault = JSON.parse(result);
                     for(i=0;i<jsondefault.length;i++){
                         console.log(jsondefault[i]["fields"]["nom"]);
                     
     
                     {% for center in centre %}
                         
                         if("{{center.nom}}" == jsondefault[i]["fields"]["nom"]){
                             pere.insertAdjacentHTML("beforeend", `<div class="col-lg-4 col-md-6 mb-5" id="{{ center.nom }}">
                                                 <div class="listing-item  ">
                                                     
                                                     <div class="listing-small-badges-container">
                                                                                             
                                                     </div>
                                                         <img src="{{center.image.url}}" alt="">
     
                                                                             <div class="listing-badge now-closed">Mnt Fermé</div>
                                                                                     
     
                                                     <div class="listing-item-content">
                                                             
                                                         <h3>{{center.get__titre }} 
                                                         <i class="verified-icon"></i>
                                                         </h3>
                                                         <span>{{center.adresse }}</span>
                                                     </div>
                                                     <span class="save like-icon"></span>
                                                     
                                                 </div>
                                                 </div>`
                             )};
     
                     {% endfor %}
     
                 };
                 })
     
                 
                 })
             }
         
          }
         })
     }
}