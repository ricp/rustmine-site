(() => {
  'use strict';

  const measurementId = 'G-YGH56KHRGX';
  const pageLocation = new URL(window.location.pathname, 'https://rustmine.org').href;
  const pageTitle = document.title;

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
    allow_google_signals: false,
    allow_ad_personalization_signals: false,
    page_location: pageLocation,
    page_referrer: pageReferrer,
    page_title: pageTitle
  });

  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
  document.head.appendChild(script);
})();
