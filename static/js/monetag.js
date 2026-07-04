/**
 * Meta Tech - Monetag Interstitial Ad Script v3
 * Intercepts FIRST click on ALL links & buttons (once per session)
 * Excludes destructive/admin actions for safety
 */
(function() {
    'use strict';

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

    function isDangerous(el) {
        // Skip destructive/admin actions
        if (el.tagName === 'A') {
            var href = el.getAttribute('href') || '';
            if (href.indexOf('/admin') === 0 ||
                href.indexOf('/delete/') === 0 ||
                href.indexOf('javascript:') === 0 ||
                href === '#' ||
                href.indexOf('#') === 0 ||
                !href) {
                return true;
            }
        }

        // Check class names for danger/delete
        if (el.classList) {
            var classes = el.className || '';
            if (classes.indexOf('btn-danger') !== -1 ||
                classes.indexOf('gallery-delete') !== -1 ||
                classes.indexOf('danger') !== -1 ||
                classes.indexOf('no-monetag') !== -1) {
                return true;
            }
        }

        // Check data attribute
        if (el.getAttribute && el.getAttribute('data-no-monetag') !== null) {
            return true;
        }

        // Check if inside a destructive container
        var parent = el.parentNode;
        while (parent && parent !== document.body) {
            if (parent.classList) {
                var pc = parent.className || '';
                if (pc.indexOf('danger') !== -1 ||
                    pc.indexOf('gallery-delete') !== -1 ||
                    (parent.getAttribute && parent.getAttribute('data-no-monetag') !== null)) {
                    return true;
                }
            }
            parent = parent.parentNode;
        }

        return false;
    }

    function interceptClick(e) {
        var target = e.target;

        // Walk up to find anchor or button
        while (target && target !== document.body) {
            var tag = target.tagName;
            if ((tag === 'A' || tag === 'BUTTON') && target.href !== undefined) {
                // Check for download attribute on links
                if (tag === 'A' && target.getAttribute('download') !== null) {
                    // Allow download but still intercept for Monetag
                }

                // Skip dangerous/admin actions
                if (isDangerous(target)) {
                    return;
                }

                if (isEligible()) {
                    e.preventDefault();
                    e.stopPropagation();
                    e.stopImmediatePropagation();
                    markDone();
                    window.location.href = MONETAG_URL;
                    return false;
                }
                return;
            }
            target = target.parentNode;
        }

        // Also check for buttons inside labels or clickable containers
        target = e.target;
        while (target && target !== document.body) {
            if (target.tagName === 'BUTTON') {
                // Check if this button is dangerous
                if (isDangerous(target)) {
                    return;
                }

                // Skip submit buttons in forms
                if (target.type === 'submit' && target.form) {
                    return;
                }

                if (isEligible()) {
                    e.preventDefault();
                    e.stopPropagation();
                    e.stopImmediatePropagation();
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
