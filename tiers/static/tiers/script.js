
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


function handleOverlayClick(event) {
    if (event.target.id === 'popup-overlay_tier') {
        closePopupTier();
    }
}