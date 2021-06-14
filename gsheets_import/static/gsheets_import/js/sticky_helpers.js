

// Function to robustly determine the top offset relative to the body element;
// independent of the DOM tree structure.
export function getAbsOffsetTop(element) {
    let absOffsetTop = 0;
    while(element) {
        absOffsetTop += element.offsetTop;
        element = element.offsetParent;
    }
    return absOffsetTop;
}



// Function to dynamically determine the (browser-specific) height of scrollbars in div elements.
export function getScrollbarHeight() {
    let scrollbarHeight = 0;
    let scrollbarDiv = document.createElement('div');

    // calculate scrollbar height as the difference of the
    // dummy div's offset height and its client height
    scrollbarDiv.style.overflow = 'scroll';
    document.body.appendChild(scrollbarDiv);
    scrollbarHeight = scrollbarDiv.offsetHeight - scrollbarDiv.clientHeight;
    document.body.removeChild(scrollbarDiv);

    return scrollbarHeight;
}
