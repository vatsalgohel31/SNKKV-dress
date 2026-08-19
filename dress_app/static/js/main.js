/**
 * School Dress Management System - Frontend JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    initEntryForm();
    initPricingMatrix();
    initViewerFilters();
});

/**
 * -------------------------------------------------------------
 * Student Dress Entry Page Logic
 * -------------------------------------------------------------
 */
function initEntryForm() {
    const form = document.getElementById('dressEntryForm');
    if (!form) return;

    const stdSelect = document.getElementById('student_standard');
    const toggleDress = document.getElementById('toggle_has_dress');
    const toggleExtraDress = document.getElementById('toggle_has_extra_dress');
    const toggleDupatta = document.getElementById('toggle_has_dupatta');
    const toggleExtraDupatta = document.getElementById('toggle_has_extra_dupatta');

    const packageCards = document.querySelectorAll('.package-card');
    const packageInput = document.getElementById('package_model_input');

    const priceDisplay = document.getElementById('priceDisplay');
    const calculatedInput = document.getElementById('calculated_total_price');

    // Standard Prices Data (injected via json_script)
    let pricesMap = {};
    const scriptEl = document.getElementById('standard-prices-data');
    if (scriptEl) {
        try {
            pricesMap = JSON.parse(scriptEl.textContent);
        } catch (e) {
            console.error("Error parsing standard-prices-data:", e);
        }
    }

    // Rate elements in UI
    const currentStdLabel = document.getElementById('currentStdLabel');
    const rateDress = document.getElementById('rateDress');
    const rateExtraDress = document.getElementById('rateExtraDress');
    const rateDupatta = document.getElementById('rateDupatta');
    const rateExtraDupatta = document.getElementById('rateExtraDupatta');

    const labelDressPrice = document.getElementById('label_dress_price');
    const labelExtraDressPrice = document.getElementById('label_extra_dress_price');
    const labelDupattaPrice = document.getElementById('label_dupatta_price');
    const labelExtraDupattaPrice = document.getElementById('label_extra_dupatta_price');

    const bDress = document.getElementById('bDress');
    const bExtraDress = document.getElementById('bExtraDress');
    const bDupatta = document.getElementById('bDupatta');
    const bExtraDupatta = document.getElementById('bExtraDupatta');

    const bExtraDressRow = document.getElementById('bExtraDressRow');
    const bDupattaRow = document.getElementById('bDupattaRow');
    const bExtraDupattaRow = document.getElementById('bExtraDupattaRow');

    function getRatesForStd(std) {
        if (pricesMap && pricesMap[std]) {
            return pricesMap[std];
        }
        return { dress: 350, extra_dress: 300, dupatta: 120, extra_dupatta: 100 };
    }

    function updateRatesDisplay() {
        const std = parseInt(stdSelect.value) || 1;
        const rates = getRatesForStd(std);

        if (currentStdLabel) currentStdLabel.textContent = `Std ${std}`;
        if (rateDress) rateDress.textContent = rates.dress;
        if (rateExtraDress) rateExtraDress.textContent = rates.extra_dress;
        if (rateDupatta) rateDupatta.textContent = rates.dupatta;
        if (rateExtraDupatta) rateExtraDupatta.textContent = rates.extra_dupatta;

        if (labelDressPrice) labelDressPrice.textContent = rates.dress;
        if (labelExtraDressPrice) labelExtraDressPrice.textContent = rates.extra_dress;
        if (labelDupattaPrice) labelDupattaPrice.textContent = rates.dupatta;
        if (labelExtraDupattaPrice) labelExtraDupattaPrice.textContent = rates.extra_dupatta;

        if (bDress) bDress.textContent = rates.dress;
        if (bExtraDress) bExtraDress.textContent = rates.extra_dress;
        if (bDupatta) bDupatta.textContent = rates.dupatta;
        if (bExtraDupatta) bExtraDupatta.textContent = rates.extra_dupatta;
    }

    function calculateTotal() {
        const std = parseInt(stdSelect.value) || 1;
        const rates = getRatesForStd(std);

        let total = 0;
        const hasD = toggleDress && toggleDress.checked;
        const hasED = toggleExtraDress && toggleExtraDress.checked;
        const hasDup = toggleDupatta && toggleDupatta.checked;
        const hasEDup = toggleExtraDupatta && toggleExtraDupatta.checked;

        if (hasD) total += rates.dress;
        if (hasED) total += rates.extra_dress;
        if (hasDup) total += rates.dupatta;
        if (hasEDup) total += rates.extra_dupatta;

        if (priceDisplay) priceDisplay.textContent = total.toFixed(2);
        if (calculatedInput) calculatedInput.value = total.toFixed(2);

        // Breakdown row visibility
        if (bExtraDressRow) {
            bExtraDressRow.classList.toggle('hide', !hasED);
        }
        if (bDupattaRow) {
            bDupattaRow.classList.toggle('hide', !hasDup);
        }
        if (bExtraDupattaRow) {
            bExtraDupattaRow.classList.toggle('hide', !hasEDup);
        }

        syncPackageCardHighlight(hasD, hasED, hasDup, hasEDup);
    }

    function syncPackageCardHighlight(hasD, hasED, hasDup, hasEDup) {
        let pkg = 'CUSTOM';
        if (hasD && !hasED && !hasDup && !hasEDup) {
            pkg = '1_DRESS';
        } else if (hasD && !hasED && hasDup && !hasEDup) {
            pkg = '1_DRESS_1_DUPATTA';
        } else if (hasD && hasED && hasDup && !hasEDup) {
            pkg = '1_DRESS_1_EXTRA_1_DUPATTA';
        } else if (hasD && hasED && hasDup && hasEDup) {
            pkg = '1_DRESS_1_EXTRA_1_DUPATTA_1_EXTRA';
        }

        if (packageInput) packageInput.value = pkg;

        packageCards.forEach(card => {
            if (card.dataset.package === pkg) {
                card.classList.add('active');
            } else {
                card.classList.remove('active');
            }
        });
    }

    function applyPackage(pkg) {
        if (pkg === '1_DRESS') {
            if (toggleDress) toggleDress.checked = true;
            if (toggleExtraDress) toggleExtraDress.checked = false;
            if (toggleDupatta) toggleDupatta.checked = false;
            if (toggleExtraDupatta) toggleExtraDupatta.checked = false;
        } else if (pkg === '1_DRESS_1_DUPATTA') {
            if (toggleDress) toggleDress.checked = true;
            if (toggleExtraDress) toggleExtraDress.checked = false;
            if (toggleDupatta) toggleDupatta.checked = true;
            if (toggleExtraDupatta) toggleExtraDupatta.checked = false;
        } else if (pkg === '1_DRESS_1_EXTRA_1_DUPATTA') {
            if (toggleDress) toggleDress.checked = true;
            if (toggleExtraDress) toggleExtraDress.checked = true;
            if (toggleDupatta) toggleDupatta.checked = true;
            if (toggleExtraDupatta) toggleExtraDupatta.checked = false;
        } else if (pkg === '1_DRESS_1_EXTRA_1_DUPATTA_1_EXTRA') {
            if (toggleDress) toggleDress.checked = true;
            if (toggleExtraDress) toggleExtraDress.checked = true;
            if (toggleDupatta) toggleDupatta.checked = true;
            if (toggleExtraDupatta) toggleExtraDupatta.checked = true;
        }
        calculateTotal();
    }

    // Event Listeners
    if (stdSelect) {
        stdSelect.addEventListener('change', () => {
            updateRatesDisplay();
            calculateTotal();
        });
    }

    [toggleDress, toggleExtraDress, toggleDupatta, toggleExtraDupatta].forEach(toggle => {
        if (toggle) {
            toggle.addEventListener('change', calculateTotal);
        }
    });

    packageCards.forEach(card => {
        card.addEventListener('click', () => {
            applyPackage(card.dataset.package);
        });
    });

    // Initial run
    updateRatesDisplay();
    calculateTotal();
}

/**
 * -------------------------------------------------------------
 * Pricing Master Matrix Page Logic
 * -------------------------------------------------------------
 */
function initPricingMatrix() {
    const rows = document.querySelectorAll('.pricing-row');
    if (!rows || rows.length === 0) return;

    function recalculateRowTotal(row) {
        const std = row.dataset.std;
        const d = parseFloat(document.getElementById(`dress_price_${std}`)?.value) || 0;
        const ed = parseFloat(document.getElementById(`extra_dress_price_${std}`)?.value) || 0;
        const dup = parseFloat(document.getElementById(`dupatta_price_${std}`)?.value) || 0;
        const edup = parseFloat(document.getElementById(`extra_dupatta_price_${std}`)?.value) || 0;

        const sumEl = document.getElementById(`total_sum_${std}`);
        if (sumEl) {
            sumEl.textContent = `₹${(d + ed + dup + edup).toFixed(0)}`;
        }
    }

    rows.forEach(row => {
        recalculateRowTotal(row);
        const inputs = row.querySelectorAll('.std-calc-input');
        inputs.forEach(input => {
            input.addEventListener('input', () => recalculateRowTotal(row));
        });
    });
}

/**
 * -------------------------------------------------------------
 * Viewer Page Filters Logic
 * -------------------------------------------------------------
 */
function initViewerFilters() {
    const filterForm = document.getElementById('viewerFilterForm');
    if (!filterForm) return;

    const autoSubmits = filterForm.querySelectorAll('.auto-submit-select');
    autoSubmits.forEach(select => {
        select.addEventListener('change', () => {
            filterForm.submit();
        });
    });
}
