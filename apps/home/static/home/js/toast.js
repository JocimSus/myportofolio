let toastTimeoutId = null;
let popoverHideTimeoutId = null;

/**
 * Toast display function
 * @param {string} title: Toast title
 * @param {string} message: Toast message
 * @param {'normal' | 'success' | 'error'} type: Toast type
 * @param {number} duration: Toast duration in ms
 */
function showToast(title, message, type = 'normal', duration = 3000) {
  const toastComponent = document.getElementById('toast-component');
  const toastTitle = document.getElementById('toast-title');
  const toastMessage = document.getElementById('toast-message');

  if (!toastComponent) return;

  if (toastTimeoutId) clearTimeout(toastTimeoutId);
  if (popoverHideTimeoutId) clearTimeout(popoverHideTimeoutId);

  toastComponent.classList.remove('toast-success', 'toast-error', 'toast-normal');
  const validTypes = ['success', 'error', 'normal'];
  const activeType = validTypes.includes(type) ? type : 'normal';
  toastComponent.classList.add(`toast-${activeType}`);

  if (toastTitle) toastTitle.textContent = title;
  if (toastMessage) toastMessage.textContent = message;

  if (!toastComponent.matches(':popover-open')) {
    toastComponent.showPopover();
    void toastComponent.offsetHeight;
  }

  toastComponent.classList.remove('toast-hidden');
  toastComponent.classList.add('toast-show');

  toastTimeoutId = setTimeout(() => {
    toastComponent.classList.remove('toast-show');
    toastComponent.classList.add('toast-hidden');

    popoverHideTimeoutId = setTimeout(() => {
      if (toastComponent.matches(':popover-open')) {
        toastComponent.hidePopover();
      }
    }, 300);
  }, duration);
}