


// Recap
function showPopupRecap() {
    document.getElementById('popup_recap').style.display = 'block';
    document.getElementById('popup-overlay_recap').style.display = 'block';
    setDefaultDates('start-date-recap', 'end-date-recap');   // For recap section
    validateDatesRecap();
}
function closePopupRecap(timer) {
    setTimeout(function() {
        document.getElementById('popup_recap').style.display = 'none';
        document.getElementById('popup-overlay_recap').style.display = 'none';
    }, timer);
}
function validateDatesRecap() {
    const startDate = document.getElementById('start-date-recap').value;
    const endDate = document.getElementById('end-date-recap').value;
    const validateButton = document.getElementById('validate-button-recap');
    
    if (startDate && endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        
        if (start <= end) {
            validateButton.disabled = false;
        } else {
            validateButton.disabled = true;
        }
    } else {
        validateButton.disabled = true;
    }
}
function submitFormRecap() {
    closePopupRecap(500);
    const startDate = document.getElementById('start-date-recap').value;
    const endDate = document.getElementById('end-date-recap').value;
    window.location.href = "/recap/";
}












