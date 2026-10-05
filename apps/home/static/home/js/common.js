(function (window, document) {
  function escapeHtml(value) {
    return String(value ?? '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#39;');
  }

  function getCookie(name) {
    if (!document.cookie) return null;

    const cookiePrefix = `${name}=`;
    const cookie = document.cookie
      .split(';')
      .map((item) => item.trim())
      .find((item) => item.startsWith(cookiePrefix));

    return cookie ? decodeURIComponent(cookie.slice(cookiePrefix.length)) : null;
  }

  function getFormErrorMessages(result, fallbackMessage) {
    if (!result.errors) {
      return [result.message || fallbackMessage];
    }

    return Object.values(result.errors)
      .flat()
      .map((error) => error.message || String(error));
  }

  window.PortfolioUtils = Object.freeze({
    escapeHtml,
    getCookie,
    getFormErrorMessages,
  });
})(window, document);
