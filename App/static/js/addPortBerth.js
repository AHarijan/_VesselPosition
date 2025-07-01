// document.getElementById("addPort").onclick = function(){
//     var section = document.getElementById("portAdd");
//     var clone = section.cloneNode(true);
//     section.parentNode.insertAfter(clone, section.nextSibling);

//     var inputs = clone.querySelectorAll('input');
//     inputs.forEach(input => input.value = '');
// };

// document.addEventListener('DOMContentLoaded', function() {
//     // Add berth section
//     document.getElementById("addPort").addEventListener("click", function() {
//         const berthSections = document.getElementById("portAdd");
//         const firstSection = document.querySelector(".berth-section");
//         const newSection = firstSection.cloneNode(true);
        
//         // Clear values in the new section
//         const inputs = newSection.querySelectorAll('input');
//         inputs.forEach(input => input.value = '');
        
//         berthSections.appendChild(newSection);
//     });
    
//     // Form submission
//     document.getElementById("portBerthForm").addEventListener("submit", function(e) {
//         // No need for custom handling unless you want to validate
//     });
// });

document.addEventListener('DOMContentLoaded', function() {
    // Add berth section
    document.getElementById("addPort").addEventListener("click", function() {
        const berthSections = document.getElementById("berthSections");
        const firstSection = document.querySelector(".berth-section");
        const newSection = firstSection.cloneNode(true);
        
        // Clear values in the new section
        const inputs = newSection.querySelectorAll('input');
        inputs.forEach(input => input.value = '');
        
        // Add remove button functionality
        const removeBtn = newSection.querySelector(".remove-berth");
        removeBtn.addEventListener("click", function() {
            if (document.querySelectorAll(".berth-section").length > 1) {
                newSection.remove();
            } else {
                alert("You need at least one berth section");
            }
        });
        
        berthSections.appendChild(newSection);
    });

    // Add remove functionality to initial berth section
    document.querySelector(".remove-berth").addEventListener("click", function() {
        if (document.querySelectorAll(".berth-section").length > 1) {
            this.closest(".berth-section").remove();
        } else {
            alert("You need at least one berth section");
        }
    });

    // Form submission handling
    document.getElementById("portBerthForm").addEventListener("submit", function(e) {
        // You can add additional validation here if needed
        console.log("Form submitted");
    });
});