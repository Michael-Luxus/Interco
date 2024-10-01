

// detail
function showPopupDetail() {
    document.getElementById('popup_detail').style.display = 'block';
    document.getElementById('popup-overlay_detail').style.display = 'block';
    setDefaultDates('start-date-detail', 'end-date-detail'); // For detail section
}
function closePopupDetail(timer) {
    setTimeout(function() {
        document.getElementById('popup_detail').style.display = 'none';
        document.getElementById('popup-overlay_detail').style.display = 'none';
    }, timer);
}
function validateDatesDetail() {
    const startDate = document.getElementById('start-date-detail').value;
    const endDate = document.getElementById('end-date-detail').value;
    const validateButton = document.getElementById('validate-button-detail');
    
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
function submitFormDetail() {
    closePopupDetail(500);
    const startDate = document.getElementById('start-date-detail').value;
    const endDate = document.getElementById('end-date-detail').value;
    window.location.href = "/detail/";
}










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



// Tier
function showPopupTier() {
    document.getElementById('popup_tier').style.display = 'block';
    document.getElementById('popup-overlay_tier').style.display = 'block';
}
function closePopupTier() {
    document.getElementById('popup_tier').style.display = 'none';
    document.getElementById('popup-overlay_tier').style.display = 'none';
}

function submitFormTier() {
    // const startDate = document.getElementById('start-date').value;
    // const endDate = document.getElementById('end-date').value;
    window.location.href = 'https://example.com';
}







 // Function to set default start and end dates
 function setDefaultDates(startId, endId) {
    // Get today's date
    const today = new Date();

    // Get the first day of the current month
    const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);

    // Format the dates to 'YYYY-MM-DD'
    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-based
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    // Set the default values for the start and end date fields
    document.getElementById(startId).value = formatDate(firstDayOfMonth);
    document.getElementById(endId).value = formatDate(today);
}





function handleOverlayClick(event) {
    if (event.target.id === 'popup-overlay_detail') {
        closePopupDetail();
    }

    if (event.target.id === 'popup-overlay_recap') {
        closePopupRecap();
    }

    if (event.target.id === 'popup-overlay_tier') {
        closePopupTier();
    }
}