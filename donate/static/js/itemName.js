var ul = document.getElementById('bulk'); // Parent

ul.addEventListener('click', function (e) {
    var target = e.target; // Clicked element
    while (target && target.parentNode !== ul) {
        target = target.parentNode; // If the clicked element isn't a direct child
        if(!target) { return; } // If element doesn't exist
    }
    if (target.tagName === 'LI'){
        window.alert("Hello"); // Check if the element is a LI
    }
});