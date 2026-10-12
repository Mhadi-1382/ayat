
// !=== App Main

// === Nav Toggle & Minimize
function navToggle() {
    const navOverlay = document.querySelector('#navOverlay');
    navOverlay.classList.toggle('nav-toggle');
}
function navMinimize() {
    const navId = document.getElementById('nav');
    const contentNavMinimizeId = document.querySelector('.content-nav-minimize');
    const navMinimizeBtnId = document.querySelector('.nav-minimize-btn');
    navId.classList.toggle('nav-minimize');
    contentNavMinimizeId.classList.toggle('content-nav-minimize-style');
    navMinimizeBtnId.classList.toggle('nav-minimize-btn-style');
    navMinimizeBtnId.toggleAttribute('title', false);
}

// === Modal
function modal(id) {
    const modalOverlay = document.getElementById(id);
    modalOverlay.classList.toggle('modal-toggle');
}

// === Tab Content & None Content
function tabContent(type, mode, btnId1, btnId2, btnId3, contentId1, contentId2, contentId3) {
    if (type == 1) {
        document.getElementById(btnId1).classList.add('tab-btn-active');
        document.getElementById(btnId2).classList.remove('tab-btn-active');
        if (mode == 1) {
            document.getElementById(contentId2).classList.remove('tab-content-active');
            document.getElementById(contentId1).classList.remove('tab-content-unactive');
        } else if (mode == 2) {
            document.getElementById(contentId1).classList.add('tab-content-unactive');
            document.getElementById(contentId2).classList.add('tab-content-active');
        }
    } else if (type == 2) {
        document.getElementById(btnId1).classList.add('tab-btn-active');
        document.getElementById(btnId2).classList.remove('tab-btn-active');
        document.getElementById(btnId3).classList.remove('tab-btn-active');
        if (mode == 1) {
            document.getElementById(contentId2).classList.remove('tab-content-active');
            document.getElementById(contentId3).classList.remove('tab-content-active');
            document.getElementById(contentId1).classList.remove('tab-content-unactive');
        } else if (mode == 2) {
            document.getElementById(contentId1).classList.add('tab-content-unactive');
            document.getElementById(contentId3).classList.add('tab-content-unactive');
            document.getElementById(contentId2).classList.add('tab-content-active');
        } else if (mode == 3) {
            document.getElementById(contentId1).classList.add('tab-content-unactive');
            document.getElementById(contentId1).classList.remove('tab-content-active');
            document.getElementById(contentId2).classList.remove('tab-content-active');
            document.getElementById(contentId3).classList.remove('tab-content-unactive');
            document.getElementById(contentId3).classList.add('tab-content-active');
        }
    }
}
function tabNoneContent(btnId1, btnId2) {
    document.getElementById(btnId1).classList.add('tab-none-content-btn-active');
    document.getElementById(btnId2).classList.remove('tab-none-content-btn-active');
}
function tabNoneContentType2(activeBtn, btn2, btn3) {
    document.getElementById(activeBtn).classList.add('tab-none-content-btn-active');
    document.getElementById(btn2).classList.remove('tab-none-content-btn-active');
    document.getElementById(btn3).classList.remove('tab-none-content-btn-active');
}

// === Dark Mode
function darkModeToggle(mode) {
    if (mode == 'light') {
        localStorage.setItem('dark_mode', 'false');
        document.body.classList.remove('dark-mode-style');
    } else {
        localStorage.setItem('dark_mode', 'true');
        document.body.classList.add('dark-mode-style');
    }
}
if (localStorage.getItem('dark_mode') == 'true') {
    document.body.classList.add('dark-mode-style');
    document.getElementById('tabSettingsModeDark1').classList.remove('tab-none-content-btn-active');
    document.getElementById('tabSettingsModeDark2').classList.add('tab-none-content-btn-active');
} else {
    document.body.classList.remove('dark-mode-style');
    document.getElementById('tabSettingsModeDark1').classList.add('tab-none-content-btn-active');
    document.getElementById('tabSettingsModeDark2').classList.remove('tab-none-content-btn-active');
}

// === Data Share
function dataShare(title, text, url) {
    const dataShare = {
        title: title,
        text: text,
        url: url,
    };
    if (navigator.canShare && navigator.canShare(dataShare)) {
        navigator.share(dataShare);
    }
}

// === Settings Application
// Update Application
function updateApp(id) {
    document.getElementById(id).innerHTML = `<span class="flex items-center gap-2"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="size-5 text-white animate-spin"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M12 6l0 -3" /><path d="M6 12l-3 0" /><path d="M7.75 7.75l-2.15 -2.15" /></svg> <span>درحال اعمال بروزرسانی...</span></span>`
    setTimeout(() => {
        window.location.reload(true);
    }, 3000);
}
// Keeping Page On (Wake Lock)
var checkboxKeepingPageOnId = document.getElementById('checkboxKeepingPageOn');
let wakeLock = null;
async function requestWakeLock() {
    try {
        wakeLock = await navigator.wakeLock.request('screen');
    } catch (err) {
        console.log(err);
    }
}
function releaseWakeLock() {
    if (wakeLock !== null) {
        wakeLock.release();
    }
}
function requestKeepingPageOn(id) {
    if (document.getElementById(id).checked) {
        localStorage.setItem('keeping_page_on', 'true');
        requestWakeLock();
    } else {
        localStorage.setItem('keeping_page_on', 'false');
        releaseWakeLock();
    }
}
if (localStorage.getItem('keeping_page_on') == 'true') {
    checkboxKeepingPageOnId.setAttribute('checked', true);
    requestWakeLock();
} else if (localStorage.getItem('keeping_page_on') == 'false') {
    checkboxKeepingPageOnId.removeAttribute('checked');
    releaseWakeLock();
}
// Glass Mode
var checkboxActiveGlassModeId = document.getElementById('checkboxActiveGlassMode');
function glassModeToggle(id) {
    if (document.getElementById(id).checked) {
        localStorage.setItem('glass_mode', 'true');
        document.body.classList.add('glass-mode-style');
    } else {
        localStorage.setItem('glass_mode', 'false');
        document.body.classList.remove('glass-mode-style');
    }
}
if (localStorage.getItem('glass_mode') == 'true') {
    checkboxActiveGlassModeId.setAttribute('checked', true);
    document.body.classList.add('glass-mode-style');
} else if (localStorage.getItem('glass_mode') == 'false') {
    checkboxActiveGlassModeId.removeAttribute('checked');
    document.body.classList.remove('glass-mode-style');
}
// Color Shell
function colorShell(id) {
    if (id == 'colorShellGreen') {
        localStorage.setItem('color_shell', 'green');

        document.getElementById(id).classList.add('color-shell-active');
        document.getElementById('colorShellBlue').classList.remove('color-shell-active');
        document.getElementById('colorShellOrange').classList.remove('color-shell-active');
        document.getElementById('colorShellRed').classList.remove('color-shell-active');

        document.body.classList.add('color-shell-green-style');
        document.body.classList.remove('color-shell-blue-style');
        document.body.classList.remove('color-shell-orange-style');
        document.body.classList.remove('color-shell-red-style');
    } else if (id == 'colorShellBlue') {
        localStorage.setItem('color_shell', 'blue');

        document.getElementById(id).classList.add('color-shell-active');
        document.getElementById('colorShellGreen').classList.remove('color-shell-active');
        document.getElementById('colorShellOrange').classList.remove('color-shell-active');
        document.getElementById('colorShellRed').classList.remove('color-shell-active');

        document.body.classList.add('color-shell-blue-style');
        document.body.classList.remove('color-shell-green-style');
        document.body.classList.remove('color-shell-orange-style');
        document.body.classList.remove('color-shell-red-style');
    } else if (id == 'colorShellOrange') {
        localStorage.setItem('color_shell', 'orange');
        
        document.getElementById(id).classList.add('color-shell-active');
        document.getElementById('colorShellGreen').classList.remove('color-shell-active');
        document.getElementById('colorShellBlue').classList.remove('color-shell-active');
        document.getElementById('colorShellRed').classList.remove('color-shell-active');

        document.body.classList.add('color-shell-orange-style');
        document.body.classList.remove('color-shell-blue-style');
        document.body.classList.remove('color-shell-green-style');
        document.body.classList.remove('color-shell-red-style');
    } else if (id == 'colorShellRed') {
        localStorage.setItem('color_shell', 'red');

        document.getElementById(id).classList.add('color-shell-active');
        document.getElementById('colorShellGreen').classList.remove('color-shell-active');
        document.getElementById('colorShellBlue').classList.remove('color-shell-active');
        document.getElementById('colorShellOrange').classList.remove('color-shell-active');
        
        document.body.classList.add('color-shell-red-style');
        document.body.classList.remove('color-shell-orange-style');
        document.body.classList.remove('color-shell-blue-style');
        document.body.classList.remove('color-shell-green-style');
    }
}
if (localStorage.getItem('color_shell') == 'green') {
    document.body.classList.toggle('color-shell-green-style');
    document.getElementById('colorShellGreen').classList.add('color-shell-active');
    document.getElementById('colorShellBlue').classList.remove('color-shell-active');
    document.getElementById('colorShellOrange').classList.remove('color-shell-active');
    document.getElementById('colorShellRed').classList.remove('color-shell-active');
} else if (localStorage.getItem('color_shell') == 'blue') {
    document.body.classList.toggle('color-shell-blue-style');
    document.getElementById('colorShellBlue').classList.add('color-shell-active');
    document.getElementById('colorShellGreen').classList.remove('color-shell-active');
    document.getElementById('colorShellOrange').classList.remove('color-shell-active');
    document.getElementById('colorShellRed').classList.remove('color-shell-active');
} else if (localStorage.getItem('color_shell') == 'orange') {
    document.body.classList.toggle('color-shell-orange-style');
    document.getElementById('colorShellOrange').classList.add('color-shell-active');
    document.getElementById('colorShellBlue').classList.remove('color-shell-active');
    document.getElementById('colorShellGreen').classList.remove('color-shell-active');
    document.getElementById('colorShellRed').classList.remove('color-shell-active');
} else if (localStorage.getItem('color_shell') == 'red') {
    document.body.classList.toggle('color-shell-red-style');
    document.getElementById('colorShellRed').classList.add('color-shell-active');
    document.getElementById('colorShellBlue').classList.remove('color-shell-active');
    document.getElementById('colorShellGreen').classList.remove('color-shell-active');
    document.getElementById('colorShellOrange').classList.remove('color-shell-active');
}
// Widget Assistant Ayat Poll
var widgetAssistantAyatId = document.getElementById('checkboxWidgetAssistantAyat');
function widgetAssistantAyatPollToggle(id) {
    if (document.getElementById(id).checked) {
        localStorage.setItem('widget_assistant_ayat_poll', 'true');
        document.cookie = "assistant_ayat_poll=false;";
    } else {
        localStorage.setItem('widget_assistant_ayat_poll', 'false');
        document.cookie = "assistant_ayat_poll=true; max-age=86400";
    }
}
if (localStorage.getItem('widget_assistant_ayat_poll') == 'true') {
    widgetAssistantAyatId.setAttribute('checked', true);
    document.cookie = "assistant_ayat_poll=false;";
}
// Active Full Menu Mode
var activeFullMenuModeId = document.getElementById('checkboxActiveFullMenuMode');
function activeFullMenuModeToggle(id) {
    if (document.getElementById(id).checked) {
        localStorage.setItem('active_full_menu_mode', 'true');
        document.body.classList.add('active-full-menu-mode-style');
    } else {
        localStorage.setItem('active_full_menu_mode', 'false');
        document.body.classList.remove('active-full-menu-mode-style');
    }
}
if (localStorage.getItem('active_full_menu_mode') == 'true') {
    activeFullMenuModeId.setAttribute('checked', true);
    document.body.classList.add('active-full-menu-mode-style');
} else if (localStorage.getItem('active_full_menu_mode') == 'false') {
    localStorage.setItem('active_full_menu_mode', 'false');
    document.body.classList.remove('active-full-menu-mode-style');
}
// Active Shortcut Rounded Mode
var activeShortcutRoundedModeId = document.getElementById('checkboxActiveShortcutRoundedMode');
function activeShortcutRoundedModeToggle(id) {
    if (document.getElementById(id).checked) {
        localStorage.setItem('active_shortcut_rounded_mode', 'true');
        document.body.classList.add('active-shortcut-rounded-mode-style');
    } else {
        localStorage.setItem('active_shortcut_rounded_mode', 'false');
        document.body.classList.remove('active-shortcut-rounded-mode-style');
    }
}
if (localStorage.getItem('active_shortcut_rounded_mode') == 'true') {
    activeShortcutRoundedModeId.setAttribute('checked', true);
    document.body.classList.add('active-shortcut-rounded-mode-style');
} else if (localStorage.getItem('active_shortcut_rounded_mode') == 'false') {
    localStorage.setItem('active_shortcut_rounded_mode', 'false');
    document.body.classList.remove('active-shortcut-rounded-mode-style');
}
// Active Eye Protection Mode
var activeEyeProtectionModeId = document.getElementById('checkboxActiveEyeProtectionMode');
var eyeProtectionId = document.getElementById('eyeProtection');
function activeEyeProtectionModeToggle(id) {
    if (document.getElementById(id).checked) {
        localStorage.setItem('active_eye_rotection_mode', 'true');
        eyeProtectionId.classList.add('active-eye-protection-mode-style');
    } else {
        localStorage.setItem('active_eye_rotection_mode', 'false');
        eyeProtectionId.classList.remove('active-eye-protection-mode-style');
    }
}
if (localStorage.getItem('active_eye_rotection_mode') == 'true') {
    activeEyeProtectionModeId.setAttribute('checked', true);
    eyeProtectionId.classList.add('active-eye-protection-mode-style');
} else if (localStorage.getItem('active_eye_rotection_mode') == 'false') {
    localStorage.setItem('active_eye_rotection_mode', 'false');
    eyeProtectionId.classList.remove('active-eye-protection-mode-style');
}

// === Disable Right Click And Drag & Drop
oncontextmenu = function() { return false };
document.querySelector("img").draggable = false;
document.querySelector("a").draggable = false;
document.querySelector("*").draggable = false;
