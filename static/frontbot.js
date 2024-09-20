
function submitFrontBotForm(el){
    console.log("submitForm", el);
    // return false;
}

function init(){
    const alertBtn = document.getElementById('alert-btn');
    const alertModal = document.getElementById('alert-modal');
    const closeBtn = document.getElementById('close-btn');

    // Close modal when "Close" button is clicked
    closeBtn.addEventListener('click', () => {
      alertModal.classList.remove('is-active');
    });
}

init();