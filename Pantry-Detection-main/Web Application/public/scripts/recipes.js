import { getFirestore, collection, onSnapshot, doc, getDoc, setDoc, deleteDoc } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";
import { app } from "./firebase-config.js";

const firestore = getFirestore(app, "recipes");

const collectionPath = "processing_results"; // Assuming "recipes" is your collection name
const destinationCollectionPath = "results_history";
// Create a reference to the collection
const collectionRef = collection(firestore, collectionPath);
let ingredients = null;
let recipes = null;
// Listen for new document additions
const unsubscribe = onSnapshot(collectionRef, (querySnapshot) => {
    querySnapshot.docChanges().forEach((change) => {
        if (change.type == "added") {
            // New document added, fetch its data
            console.log(change.doc.id);
            console.log(change.doc.data().identified_foods); // GRABS JUST THE INGREDIENTS
            ingredients = change.doc.data().identified_foods;
            recipes = change.doc.data().matching_recipes;
            console.log(recipes);
            displayResultsHTML(ingredients,recipes);
            const sourceDocRef = doc(firestore, collectionPath, change.doc.id);
            const destinationDocRef = doc(firestore, destinationCollectionPath, change.doc.id);
            getDoc(sourceDocRef)
             .then((sourceDocSnapshot) => {
                  console.log("Snapshot:", sourceDocSnapshot); // Log the snapshot object
                  if (sourceDocSnapshot.exists()) {
                    // Document exists in the source collection
                    // Get the data
                    const data = sourceDocSnapshot.data();
                    console.log("Document data:", data); // Log the document data
                    
                    // Write the document to the destination collection
                    setDoc(destinationDocRef, data)
                      .then(() => {
                        console.log("Document moved to the destination collection successfully.");
              
                        // Delete the document from the source collection
                        deleteDoc(sourceDocRef)
                          .then(() => {
                            console.log("Document deleted from the source collection.");
                          })
                          .catch((error) => {
                            console.error("Error deleting document from the source collection:", error);
                          });
                      })
                      .catch((error) => {
                        console.error("Error writing document to the destination collection:", error);
                      });
                  } else {
                    // Document doesn't exist in the source collection
                    console.log("Document does not exist in the source collection.");
                  }
                })
                .catch((error) => {
                  console.error("Error getting document from the source collection:", error);
                });
        }
    });
}, (error) => {
    console.error("Error getting documents:", error);
});

function displayResultsHTML(ingredients, recipes){
  const ingredContainer = document.getElementById("ingredients");
  ingredients.forEach(ingredient=> {
    const element = document.createElement("div");
    element.setAttribute("id","ingredient");
    element.textContent = `${ingredient}`;
    console.log(ingredContainer);
    console.log(element);
    ingredContainer.append(element);
  });

  const recipeImgContainer = document.getElementById("recipeImages");
  const recipeContainer = document.getElementById("recipes");
  recipes.forEach(item => {
      // Create container for each recipe
      const recipeWrapper = document.createElement("div");
      recipeWrapper.classList.add("recipe-wrapper");
      // Create element for recipe name
      const nameElement = document.createElement("div");
      nameElement.classList.add("recipe-name");
      nameElement.textContent = item.name;
      const recipeImg = document.createElement("img");
      const directionsWrapper = document.createElement("ol");
      const directionsId = item.name + "directions";
      directionsWrapper.setAttribute("id", directionsId);
      const recipeDocRef = doc(firestore, "recipes", item.name);
      const directions = document.getElementById("directions");
      getDoc(recipeDocRef)
        .then(recipeDocSnapshot =>{
          if(recipeDocSnapshot.exists()) {
            const recipeData = recipeDocSnapshot.data();
            const numSteps = recipeData.numSteps;
            for (let i = 1; i <= numSteps; i++) {
              const stepField = `Step${i}`;
              const step = recipeData[stepField];
              const li = document.createElement("li");
              li.textContent = step;
              li.style.marginBottom = "15px";
              directionsWrapper.append(li);
              directionsWrapper.style.display = "none";
            }
            directions.append(directionsWrapper);
            const imageUrl = recipeData.Image;
            recipeImg.src = imageUrl;
            recipeImg.id = item.name;
            recipeImg.style.display = "none";
            recipeImg.style.width = "300px";
            recipeImg.style.height = "300px";
            recipeImg.style.borderRadius = "5px";
            recipeImg.style.boxShadow = "0px 6px 4px rgba(0, 0, 0, 0.3)";
            recipeImgContainer.append(recipeImg);
          } else {
            console.log("Recipe document not found!");
          }
        }).catch((error) => {
          console.error("Error getting recipe document:", error);
        });
      // Create element for completeness percent
      const percentElement = document.createElement("div");
      percentElement.classList.add("recipe-percent");
      percentElement.textContent = `${item.completeness.toFixed(0)}%`;
      if (item.completeness >= 80 & item.completeness < 90) {
        recipeWrapper.style.border = "2px solid #98ba00";
      } else if (item.completeness >= 70 & item.completeness < 80) {
        recipeWrapper.style.border = "2px solid #cdcd24";
      } else if (item.completeness >= 60 & item.completeness < 70) {
        recipeWrapper.style.border = "2px solid #cd7b24";
      } else if (item.completeness < 60){
        recipeWrapper.style.border = "2px solid #cd2d24";
      } else {
        recipeWrapper.style.border = "2px solid #4ABA00"
      }
      recipeWrapper.addEventListener("click", function() {
        const displayImg = document.getElementById(item.name);
        const displayDirect = document.getElementById(item.name + "directions");
        const annotated = document.getElementById("annotated_frame");
        if (displayImg) {
            if (displayImg.style.display === "none") {
                displayImg.style.display = "flex";
                displayDirect.style.display = "block";
                annotated.style.display = "none";
                console.log("annotated none");
            } else {
                displayImg.style.display = "none";
                displayDirect.style.display = "none";
                //annotated.style.display = "block";
            }
        } else {
            console.error("Element with ID '" + item.name + "' not found.");
        }
    });
    document.addEventListener("click", function(event) {
      if (!recipeWrapper.contains(event.target)) {
          const hideImg = document.getElementById(item.name);
          const hideDirection = document.getElementById(item.name + "directions");
          const annotated = document.getElementById("annotated_frame");
          if (hideImg) {
              hideImg.style.display = "none";
              hideDirection.style.display = "none";
          } else {
              console.error("Element with ID '" + item.name + "' not found.");
          }
      }
  });
      recipeWrapper.style.cursor = "pointer";
      recipeWrapper.style.marginTop = "3px";
      // Append name and percent elements to the recipe wrapper
      recipeWrapper.appendChild(nameElement);
      recipeWrapper.appendChild(percentElement);
      
      // Append the recipe wrapper to the recipe container
      recipeContainer.appendChild(recipeWrapper);
  });

  const hide = document.getElementById("left");
  hide.style.display = "none";
  const results = document.getElementById("right");
  results.style.display = "block";
  const annotate = document.getElementById("annotated_frame");
  annotate.src = "https://storage.cloud.google.com/rummage-annotated/annotated_frame.jpg?authuser=1";
}
