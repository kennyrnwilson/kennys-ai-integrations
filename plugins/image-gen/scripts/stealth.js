// Stealth init-script for Playwright MCP
// Masks automation signals to reduce bot detection by Google and other services.
// Loaded via --init-script flag before any page scripts execute.

// 1. Remove the webdriver flag — the primary bot detection signal
Object.defineProperty(navigator, 'webdriver', {
  get: () => undefined,
});

// 2. Populate navigator.plugins — real Chrome has plugins, automated Chromium doesn't
Object.defineProperty(navigator, 'plugins', {
  get: () => {
    const plugins = [
      { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format' },
      { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: '' },
      { name: 'Native Client', filename: 'internal-nacl-plugin', description: '' },
    ];
    plugins.length = 3;
    return plugins;
  },
});

// 3. Populate navigator.languages — bot profiles often have empty or single-entry arrays
Object.defineProperty(navigator, 'languages', {
  get: () => ['en-GB', 'en-US', 'en'],
});

// 4. Fix window.chrome — real Chrome has this object, Playwright's Chromium may not
if (!window.chrome) {
  window.chrome = {};
}
if (!window.chrome.runtime) {
  window.chrome.runtime = {
    connect: () => {},
    sendMessage: () => {},
  };
}

// 5. Override permissions.query for notifications — a common fingerprint check
const originalQuery = window.navigator.permissions.query.bind(window.navigator.permissions);
window.navigator.permissions.query = (parameters) => {
  if (parameters.name === 'notifications') {
    return Promise.resolve({ state: Notification.permission });
  }
  return originalQuery(parameters);
};

// 6. Fix missing connection property — headless/automated browsers sometimes lack this
if (!navigator.connection) {
  Object.defineProperty(navigator, 'connection', {
    get: () => ({
      effectiveType: '4g',
      rtt: 50,
      downlink: 10,
      saveData: false,
    }),
  });
}

// 7. Prevent detection via toString checks on overridden functions
// Some sites check if native functions have been tampered with by calling .toString()
const nativeToString = Function.prototype.toString;
const customToString = function () {
  if (this === window.navigator.permissions.query) {
    return 'function query() { [native code] }';
  }
  return nativeToString.call(this);
};
Function.prototype.toString = customToString;
