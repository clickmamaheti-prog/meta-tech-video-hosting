/**
 * Meta Tech - Monetag Interstitial Ad Script
 * First click → redirect to Monetag → back → second click works
 * Only intercepts navigational links (not JS-triggered buttons)
 */
(function() {
    var MONETAG_URL = 'https://omg10.com/4/11215731';
    var STORAGE_KEY = 'mtg_done';
    var EXPIRY_HOURS = 6;

    function isEligible() {
        try {
            var val = localStorage.getItem(STORAGE_KEY);
            if (!val) return true;
            var ts = parseInt(val, 10);
            if (isNaN(ts)) return true;
            if (Date.now() - ts > EXPIRY_HOURS * 60 * 60 * 1000) return true;
            return false;
        } catch(e) {
            return true;
        }
    }

    function markDone() {
        try {
            localStorage.setItem(STORAGE_KEY, Date.now().toString());
        } catch(e) {}
    }

    function interceptClick(e) {
        var target = e.target;

        // Walk up to find the anchor
        while (target && target !== document.body) {
            if (target.tagName === 'A' && target.href) {
                var href = target.getAttribute('href') || '';

                // Skip admin/delete/javascript/hash-only links
                if (href.indexOf('/admin') === 0 ||
                    href.indexOf('/delete/') === 0 ||
                    href.indexOf('javascript:') === 0 ||
                    href === '#' ||
                    href.indexOf('#') === 0 ||
                    !href) {
                    return;
                }

                // Skip download links (direct file links that open in new tab or download)
                if (target.getAttribute('download') !== null) {
                    return;
                }

                if (isEligible()) {
                    e.preventDefault();
                    e.stopPropagation();
                    markDone();
                    window.location.href = MONETAG_URL;
                    return false;
                }
                return;
            }
            target = target.parentNode;
        }
    }

    document.addEventListener('click', interceptClick, true);
})();
