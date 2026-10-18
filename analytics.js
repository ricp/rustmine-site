(() => {
  'use strict';

  // Keep off until the GA4 web stream's Enhanced Measurement settings have been verified.
  // In particular, history-based page views and unrelated automatic events must be off.
  const ENABLE_GA4 = false;
  if (!ENABLE_GA4) return;

  const measurementId = 'G-YGH56KHRGX';
  const pageLocation = 'https://rustmine.org/';
  const pageTitle = 'RustMine — Engineering journal';
  document.getElementById('ga4-privacy-off').hidden = true;
  document.getElementById('ga4-privacy-on').hidden = false;
  document.getElementById('ga4-footer-off').hidden = true;
  document.getElementById('ga4-footer-on').hidden = false;

  let pageReferrer = '';
  if (document.referrer) {
    try {
      const referrer = new URL(document.referrer);
      if (referrer.protocol === 'https:' || referrer.protocol === 'http:') pageReferrer = referrer.origin;
    } catch (_) {
      // An invalid referrer is not sent to Analytics.
    }
  }

  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied'
  });
  window.gtag('js', new Date());
  window.gtag('config', measurementId, {
    send_page_view: false,
    allow_google_signals: false,
    allow_ad_personalization_signals: false,
    page_location: pageLocation,
    page_referrer: pageReferrer,
    page_title: pageTitle
  });
  window.gtag('event', 'page_view', {
    page_location: pageLocation,
    page_referrer: pageReferrer,
    page_title: pageTitle
  });

  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
  document.head.appendChild(script);
})();
