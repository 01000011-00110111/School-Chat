let unread_messages = 0;

const update_appbadge = () => {
    const isInStandaloneMode = () =>
        (window.matchMedia('(display-mode: standalone)').matches) || (window.navigator.standalone) || document.referrer.includes('android-app://');

    if (isInStandaloneMode()) {
        navigator.setAppBadge(unread_messages += 1);
    }
}

const check_focus = () => {
    if (document.hasFocus()) {
        const isInStandaloneMode = () =>
            (window.matchMedia('(display-mode: standalone)').matches) || (window.navigator.standalone) || document.referrer.includes('android-app://');
      
        if (isInStandaloneMode()) {
            navigator.setAppBadge(0);
            unread_messages = 0;
        }
    }
};
setInterval(() => {
    check_focus();
}, 100)

export {update_appbadge, check_focus}