import { ref } from 'vue';

export function useAlertDialog() {
  const isOpen = ref(false);
  const title = ref('');
  const description = ref('');
  const cancelText = ref('Cancel');
  const confirmText = ref('OK');
  const resolveFn = ref(null);

  function open(_title, _description, _cancelText, _confirmText) {
    title.value = _title;
    description.value = _description;
    cancelText.value = _cancelText;
    confirmText.value = _confirmText;
    isOpen.value = true;

    return new Promise((resolve) => {
      resolveFn.value = resolve;
    });
  }

  function cancel() {
    isOpen.value = false;
    if (resolveFn.value) resolveFn.value(false);
  }

  function confirm() {
    isOpen.value = false;
    if (resolveFn.value) resolveFn.value(true);
  }

  return {
    isOpen,
    title,
    description,
    cancelText,
    confirmText,
    open,
    cancel,
    confirm
  };
}
